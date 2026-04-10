# -*- coding: utf-8 -*-
import sys
from dataclasses import dataclass, field
from PySide6 import QtCore
from functools import partial
import numpy as np
import random
from common import *
import gui_main_window
from review import review
import os
import main_window_texts as texts
from config_params import *
import pandas as pd
import common
from datetime import datetime
from finalize import finalize


@dataclass
class user_set_state:
    cfg_dict: dict = field(default_factory=dict)
    combobox_indices: list = field(default_factory=list)
    texts: list = field(default_factory=list)
    random_indices: list = field(default_factory=list)
    review_statuses: list = field(default_factory=list)


class MainWindow(QtWidgets.QMainWindow, gui_main_window.Ui_MainWindow):
    def __init__(self, project_dir, cfg_dict, session_state):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        # Row and Col vals
        self.row_values = {}
        self.field_replacements = {}
        self.string_in_field_replacements = {}
        self.placeholder_options = {}
        self.placeholders = {}
        self.col_values = []
        self.num_rows = 0
        self.num_cols = 0

        # Widgets and Widget Containers
        self.review_windows = {}
        self.comboBoxes = []

        # Data
        self.db = {}

        # Configs
        self.project_dir = ''
        self.state = None
        self.write_fct = None
        self.easteregg_timer = None
        self.review_editable = False
        self.dirty = False

        self.init_function(project_dir, session_state, cfg_dict)

    def closeEvent(self, event):
        if self.dirty:
            reply = show_msgbox_Yes_No_Cancel(texts.closeEvent_msgbox_title[Settings().language],
                                              texts.closeEvent_msgbox_text[Settings().language])
            if reply == QtWidgets.QMessageBox.Yes:
                self.save_session()
            elif reply == QtWidgets.QMessageBox.Cancel:
                event.ignore()
                return
        self.close_sub_windows()
        super().closeEvent(event)

    # ************************** Initialization START **************************

    def init_function(self, project_dir, session_state, cfg_dict):
        # When you click the easteregg button twice in a row, the easteregg is triggered
        self.easteregg_timer = QtCore.QTimer()
        self.easteregg_timer.setSingleShot(True)

        # Set title of main window
        self.set_window_title(project_dir)

        # Cfgs
        self.project_dir = project_dir
        self.review_editable = cfg_dict['review_editable']

        # Read data from files
        self.read_data_from_files(self.project_dir)

        # Retrieve state from session state, if applicable
        if session_state:
            self.state = session_state
        else:
            self.state = self.init_session_anew(cfg_dict)

        # Make all the widgets and adjust size
        self.make_columns()
        self.make_rows()
        self.adjustSize()

        if session_state:
            self.init_session_from_file(session_state)

    def read_data_from_files(self, project_dir):
        self.db = pd.read_excel(os.path.join(project_dir, 'db.xlsx'), sheet_name=None)
        for entry_key in self.db.keys():
            self.db[entry_key].columns = self.db[entry_key].columns.astype(str)
        col_values_before_check = list(self.db.keys())
        if len(col_values_before_check) > glob_cfg_max_num_cols:
            show_msgbox(texts.read_data_from_files_msgbox_title[Settings().language],
                        texts.read_data_from_files_msgbox_text[Settings().language].replace('_num_sheets', str(glob_cfg_max_num_cols)).replace('_num_ignored', str(len(col_values_before_check) - glob_cfg_max_num_cols)))
        self.col_values = col_values_before_check[0:min(glob_cfg_max_num_cols, len(col_values_before_check))]
        self.row_values, self.string_in_field_replacements, self.field_replacements, self.placeholder_options, self.placeholders, succeeded = read_rows_data(os.path.join(project_dir, 'rows.xlsx'))
        if not succeeded:
            sys.exit(1)

    def make_columns(self):
        self.add_send_mail_pushButton()
        self.add_column_plainTextEdits()
        self.add_save_session_pushButton()
        self.add_easteregg_pushButton()

    def add_send_mail_pushButton(self):
        btn = QtWidgets.QPushButton()
        btn.setText(texts.add_send_mail_pushButton_label[Settings().language])
        btn.setFixedWidth(glob_cfg_row_header_width)
        btn.setFixedHeight(glob_cfg_col_header_height)
        btn.clicked.connect(send_mail)
        self.gridLayout_selection.addWidget(btn, 0, 0, 1, 1)

    def add_column_plainTextEdits(self):
        for idx, col_value in enumerate(self.col_values):
            edit = QtWidgets.QPlainTextEdit()
            edit.setReadOnly(True)
            edit.setPlainText(col_value)
            edit.setFixedHeight(glob_cfg_col_header_height)
            self.gridLayout_selection.addWidget(edit, 0, idx + 1, 1, 1)
        self.num_cols = len(self.col_values)

    def add_save_session_pushButton(self):
        btn = QtWidgets.QPushButton()
        btn.setText(texts.add_save_session_pushButton_label[Settings().language])
        btn.setFixedHeight(glob_cfg_col_header_height)
        btn.clicked.connect(self.on_save_session_pushButton_clicked)
        self.gridLayout_selection.addWidget(btn, 0, self.num_cols + 1, 1, 1)

    def add_easteregg_pushButton(self):
        btn = QtWidgets.QPushButton()
        btn.setText('\u2193 Status \u2193')
        btn.setFixedHeight(glob_cfg_col_header_height)
        btn.clicked.connect(self.on_easteregg_pushButton_clicked)
        self.gridLayout_selection.addWidget(btn, 0, self.num_cols + 2, 1, 1)

    def make_rows(self):
        i_row = 0
        for i_row, row_value in enumerate(self.row_values):
            self.add_name_lineEdit(i_row)
            self.add_comboBoxes(i_row)
            self.add_review_pushButton(i_row)
            self.add_status_lineEdit(i_row)
        self.num_rows = i_row + 1

    def add_name_lineEdit(self, i_row):
        name_lineEdit = QtWidgets.QLineEdit(QtWidgets.QWidget(self.centralwidget))
        name_lineEdit.setText(self.row_values[i_row])
        name_lineEdit.setFixedWidth(glob_cfg_row_header_width)
        name_lineEdit.setReadOnly(True)
        self.gridLayout_selection.addWidget(name_lineEdit, i_row + 1, 0, 1, 1)

    def add_comboBoxes(self, i_row):
        comboBoxes = []
        for i_col, sheet_name in enumerate(self.col_values):  # Sheet names = column values
            rows = list(self.db[sheet_name].keys())
            rows = [str(row) for row in rows]
            comboBox = {sheet_name: QtWidgets.QComboBox(QtWidgets.QWidget(self.centralwidget))}
            comboBox[sheet_name].addItem('')
            comboBox[sheet_name].addItems(rows)
            comboBox[sheet_name].currentIndexChanged.connect(self.set_dirty)
            comboBox[sheet_name].currentIndexChanged.connect(lambda _: self.set_review_status_started(i_row))
            comboBoxes.append(comboBox[sheet_name])
            self.gridLayout_selection.addWidget(comboBox[sheet_name], i_row + 1, i_col + 1, 1, 1)
        self.comboBoxes.append(comboBoxes)

    def set_dirty(self):
        self.dirty = True

    def add_review_pushButton(self, i_row):
        review_pushButton = QtWidgets.QPushButton(QtWidgets.QWidget(self.centralwidget))
        review_pushButton.setText(texts.add_review_pushButton_label[Settings().language])
        review_pushButton.clicked.connect(partial(self.on_review_pushButton_clicked, i_row))
        self.gridLayout_selection.addWidget(review_pushButton, i_row + 1, self.num_cols + 1, 1, 1)

    def add_status_lineEdit(self, i_row):
        review_lineEdit = QtWidgets.QLineEdit(QtWidgets.QWidget(self.centralwidget))
        review_lineEdit.setEnabled(False)
        review_lineEdit.adjustSize()
        review_lineEdit.setStyleSheet("background-color: red;")
        self.gridLayout_selection.addWidget(review_lineEdit, i_row + 1, self.num_cols + 2, 1, 1)

    def init_session_from_file(self, session_state):
        for i_row in range(len(session_state.combobox_indices)):
            current_cbb_dict = session_state.combobox_indices[i_row]
            current_cbb = self.comboBoxes[i_row]
            if current_cbb_dict:
                for i_col in range(len(current_cbb)):
                    current_cbb[i_col].blockSignals(True)
                    current_cbb[i_col].setCurrentIndex(current_cbb_dict[i_col])
                    current_cbb[i_col].blockSignals(False)
                    if session_state.review_statuses[i_row] == review_status.started:
                        self.set_review_status_started(i_row)
                    elif session_state.review_statuses[i_row] == review_status.finished:
                        self.set_review_status_finished(i_row)

    def init_session_anew(self, cfg_dict):
        state = user_set_state()
        state.cfg_dict = cfg_dict
        state.cfg_dict['version'] = glob_cfg_version_string
        for idx in range(len(self.row_values)):
            state.combobox_indices.append({})
            state.texts.append({})
            state.random_indices.append({})
            state.review_statuses.append(review_status.not_yet_started)
        return state

    def set_window_title(self, project_dir):
        window_title_str = texts.set_window_title_caption[Settings().language] \
            .replace('_version_string', glob_cfg_version_string) \
            .replace('_project_dir', project_dir) \
            .replace('_language', Settings().language)
        self.setWindowTitle(window_title_str)

    def close_sub_windows(self):
        for i_row in range(self.num_rows):
            if i_row in self.review_windows.keys():
                self.review_windows[i_row].close()

    # ************************** Initialization END **************************

    # ************************** Pushbutton Functions START ******************

    def save_final_session(self, session_dir):
        final_dir = session_dir + datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + '_' + os.environ[
            'COMPUTERNAME'] + "_" + os.getlogin() + ".final"
        if joblib.dump(self.state, final_dir, compress=3):
            reply = show_msgbox_Yes_No(
                texts.on_save_session_pushButton_clicked_final_created_msgbox_title[Settings().language],
                texts.on_save_session_pushButton_clicked_final_created_msgbox_text[Settings().language])
            if reply == QtWidgets.QMessageBox.Yes:
                finalize_window = finalize(final_dir)
                finalize_window.exec()

    def save_session(self):
        session_dir = self.project_dir + "/sessions/"
        os.makedirs(session_dir, exist_ok=True)
        for i_row in range(self.num_rows):
            for i_col in range(self.num_cols):
                self.state.combobox_indices[i_row][i_col] = self.comboBoxes[i_row][i_col].currentIndex()
        if joblib.dump(self.state, session_dir + datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + '_' + os.environ['COMPUTERNAME'] + "_" + os.getlogin() + ".session", compress=3):
            show_msgbox(texts.on_save_session_pushButton_clicked_msgbox_title[Settings().language],
                        texts.on_save_session_pushButton_clicked_msgbox_text[Settings().language])
            self.dirty = False
        if all([review_status_ == review_status.finished for review_status_ in self.state.review_statuses]):
            if len([x for x in os.listdir(session_dir) if x.endswith('.final')]) > 0:
                reply = show_msgbox_Yes_No(texts.on_save_session_pushButton_clicked_final_already_exists_msgbox_title[Settings().language],
                                           texts.on_save_session_pushButton_clicked_final_already_exists_msgbox_text[Settings().language])
                if reply == QtWidgets.QMessageBox.Yes:
                    # delete existing final file in list comprehension
                    [os.remove(os.path.join(session_dir, x)) for x in os.listdir(session_dir) if x.endswith('.final')]
                    self.save_final_session(session_dir)
            else:
                self.save_final_session(session_dir)

    def on_save_session_pushButton_clicked(self):
        self.save_session()

    def on_easteregg_pushButton_clicked(self):
        if self.easteregg_timer.remainingTime() == -1:
            self.easteregg_timer.start(250)
        else:
            show_msgbox(texts.on_easteregg_pushButton_clicked_msgbox_title[Settings().language],
                        texts.on_easteregg_pushButton_clicked_msgbox_text[Settings().language])
            self.easteregg_timer.stop()

    # ************************** Pushbutton Functions END ********************

    # ************************** Review Window Functions START ***************

    def on_review_pushButton_clicked(self, i_row):
        if self.state.texts[i_row] and not self.did_any_dropdown_index_change(i_row):
            text_dict = self.state.texts[i_row]
        else:
            text_dict = self.get_text_dict_from_comboboxes(i_row)
            self.state.combobox_indices[i_row] = [self.comboBoxes[i_row][i_col].currentIndex() for i_col in range(self.num_cols)]
            self.state.texts[i_row] = text_dict
        self.set_review_status_started(i_row)
        self.add_review_window(i_row, text_dict)
        self.review_windows[i_row].show()

    def were_all_dropdowns_for_row_selected(self, i_row):
        for i_col in range(self.num_cols):
            if self.comboBoxes[i_row][i_col].currentIndex() == 0:
                return False
        return True

    def did_any_dropdown_index_change(self, i_row):
        for i_col in range(self.num_cols):
            if self.state.combobox_indices[i_row][i_col] != self.comboBoxes[i_row][i_col].currentIndex():
                return True
        return False

    def get_text_dict_from_comboboxes(self, i_row):
        text_dict = {}
        for i_col, col_val in enumerate(self.col_values):
            current_text = self.comboBoxes[i_row][i_col].currentText()
            if current_text == '':
                text_dict[i_col] = ''
            else:
                alternatives_list_incl_nans = list(self.db[col_val][current_text])
                alternatives_list = [x for x in alternatives_list_incl_nans if not (pd.isnull(x))]
                self.state.random_indices[i_row][i_col] = random.randint(0, len(alternatives_list) - 1)
                text_dict[i_col] = self.db[col_val].iloc[self.state.random_indices[i_row][i_col], self.comboBoxes[i_row][i_col].currentIndex() - 1]
                text_dict[i_col] = self.replace_placeholders(text_dict[i_col], i_row)
        return text_dict

    def add_review_window(self, i_row, text_dict):
        self.review_windows[i_row] = review()
        for i_col in range(self.num_cols):
            self.add_plaintextEdit_to_review_window(i_row, i_col, text_dict)
            self.add_shuffle_pushButton_to_review_window(i_row, i_col)
        self.add_save_pushbutton_to_review_window(i_row)

    def add_plaintextEdit_to_review_window(self, i_row, i_col, text_dict):
        self.review_windows[i_row].label_name.setText(self.row_values[i_row])
        self.review_windows[i_row].plainTextEdits[i_col] = QtWidgets.QPlainTextEdit()
        self.review_windows[i_row].plainTextEdits[i_col].setPlainText(text_dict[i_col])
        self.review_windows[i_row].gridLayout.addWidget(self.review_windows[i_row].plainTextEdits[i_col], i_col + 1, 0, 1, 1)
        if self.review_editable:
            self.review_windows[i_row].plainTextEdits[i_col].setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
        else:
            self.review_windows[i_row].plainTextEdits[i_col].setTextInteractionFlags(QtCore.Qt.NoTextInteraction)

    def add_shuffle_pushButton_to_review_window(self, i_row, i_col):
        self.review_windows[i_row].shuffle_pushButtons[i_col] = QtWidgets.QPushButton()
        self.review_windows[i_row].shuffle_pushButtons[i_col].setText(texts.add_shuffle_pushButton_to_review_window_pushButton_label[Settings().language])
        self.review_windows[i_row].shuffle_pushButtons[i_col].clicked.connect(partial(self.on_shuffle_pushButton_clicked, i_row, i_col, self.col_values[i_col]))
        self.review_windows[i_row].gridLayout.addWidget(self.review_windows[i_row].shuffle_pushButtons[i_col], i_col + 1, 1, 1, 1)

    def add_save_pushbutton_to_review_window(self, i_row):
        self.review_windows[i_row].save_review_pushButton = QtWidgets.QPushButton()
        self.review_windows[i_row].save_review_pushButton.setText(texts.add_save_pushbutton_to_review_window_pushButton_label[Settings().language])
        self.review_windows[i_row].save_review_pushButton.clicked.connect(partial(self.on_save_review_pushButton_clicked, i_row))
        self.review_windows[i_row].gridLayout.addWidget(self.review_windows[i_row].save_review_pushButton, self.num_cols + 1, 0, 1, 1)

    def on_shuffle_pushButton_clicked(self, i_row, i_col, col_val):
        current_text = self.comboBoxes[i_row][i_col].currentText()
        if current_text == '':
            return
        alternatives_list_incl_nans = list(self.db[col_val][current_text])
        alternatives_list = [x for x in alternatives_list_incl_nans if not (pd.isnull(x))]
        if len(alternatives_list) > 1:
            rdm_idx = self.state.random_indices[i_row][i_col]
            while_exit_counter = 0
            while rdm_idx == self.state.random_indices[i_row][i_col] and while_exit_counter < 10:
                rdm_idx = random.randint(0, len(alternatives_list) - 1)
                while_exit_counter = while_exit_counter + 1
        else:
            rdm_idx = 0
        new_text = self.db[col_val].iloc[rdm_idx, self.comboBoxes[i_row][i_col].currentIndex() - 1]
        new_text = self.replace_placeholders(new_text, i_row)
        self.review_windows[i_row].plainTextEdits[i_col].setPlainText(new_text)
        self.state.texts[i_row][i_col] = new_text
        self.state.random_indices[i_row][i_col] = rdm_idx

    def on_save_review_pushButton_clicked(self, i_row):
        for key, value in self.review_windows[i_row].plainTextEdits.items():
            self.state.texts[i_row][key] = value.toPlainText()
        self.set_review_status_finished(i_row)
        self.set_dirty()
        self.review_windows[i_row].close()

    def replace_placeholders(self, text, i_row):
        for placeholder_key, placeholder_values in self.placeholder_options.items():
            for key, value in zip(next(iter(placeholder_values.values())).values(), placeholder_values[self.placeholders[placeholder_key][i_row]].values()):
                text = text.replace(key, value)
        for string_in_field_replacement_key, string_in_field_replacement_value in self.string_in_field_replacements.items():
            text = text.replace(string_in_field_replacement_key, string_in_field_replacement_value[i_row])
        return text

    # ************************** Review Window Functions END ****************

    # ************************** Status Functions START **********************

    def set_review_status_started(self, i_row):
        self.state.review_statuses[i_row] = review_status.started
        self.paint_status_at_position(i_row + 1, self.num_cols + 2, 'yellow')

    def set_review_status_finished(self, i_row):
        self.state.review_statuses[i_row] = review_status.finished
        self.paint_status_at_position(i_row + 1, self.num_cols + 2, 'green')

    def paint_status_at_position(self, i_row, i_col, color):
        self.gridLayout_selection.itemAtPosition(i_row, i_col).widget().setStyleSheet("background-color: " + color + ";")

    # ************************** Status Functions END ************************
