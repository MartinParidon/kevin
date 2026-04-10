# -*- coding: utf-8 -*-
import shutil
import socket
from datetime import datetime
import pandas as pd
import config_params
import gui_config_creator
from common import *
import config_creator_texts as texts


class config_creator(QtWidgets.QDialog, gui_config_creator.Ui_Dialog):
    def __init__(self):
        super(config_creator, self).__init__()
        self.setupUi(self)
        self.update_captions()
        self.project_dir = ""
        self.cfg_dict = dict.fromkeys(config_params.glob_cfg_necessary_keys)
        self.pushButton_set_project_dir.clicked.connect(self.on_pushButton_set_project_dir_clicked)
        self.pushButton_set_db_path.clicked.connect(self.on_pushButton_set_db_path_clicked)
        self.pushButton_set_rows_path.clicked.connect(self.on_pushButton_set_rows_path_clicked)
        self.pushButton_set_template_path.clicked.connect(self.on_pushButton_set_template_path_clicked)
        self.checkBox_use_sheet_names.toggled.connect(self.on_checkBox_use_sheet_names_toggled)
        self.pushButton_Save.clicked.connect(self.on_pushButton_Save_clicked)
        self.pushButton_Cancel.clicked.connect(self.close)

    def update_captions(self):
        self.setWindowTitle(texts.update_captions_window_title[Settings().language])
        for widget in self.findChildren(QtWidgets.QWidget):
            if widget.objectName() in texts.update_captions_prompts[Settings().language]:
                if isinstance(widget, QtWidgets.QLineEdit):
                    widget.setPlaceholderText(texts.update_captions_prompts[Settings().language][widget.objectName()])
                elif isinstance(widget, QtWidgets.QCheckBox):
                    widget.setText(texts.update_captions_prompts[Settings().language][widget.objectName()])
                elif isinstance(widget, QtWidgets.QPlainTextEdit):
                    widget.setPlaceholderText(texts.update_captions_prompts[Settings().language][widget.objectName()])
                elif isinstance(widget, QtWidgets.QPushButton):
                    widget.setText(texts.update_captions_prompts[Settings().language][widget.objectName()])
                elif isinstance(widget, QtWidgets.QLabel):
                    widget.setText(texts.update_captions_prompts[Settings().language][widget.objectName()])
                elif isinstance(widget, QtWidgets.QGroupBox):
                    widget.setTitle(texts.update_captions_prompts[Settings().language][widget.objectName()])

    def on_pushButton_set_project_dir_clicked(self):
        project_dir_candidate = QtWidgets.QFileDialog.getExistingDirectory(self, texts.on_pushButton_set_project_dir_clicked_dialog_title[Settings().language],
                                                                           os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'))
        if any(os.path.isfile(os.path.join(root, f)) for root, dirs, files in os.walk(project_dir_candidate) for f in files):
            show_msgbox(texts.on_pushButton_set_project_dir_clicked_msgbox_title[Settings().language],
                        texts.on_pushButton_set_project_dir_clicked_msgbox_text[Settings().language])
        else:
            self.project_dir = project_dir_candidate
            self.lineEdit_project_dir.setText(self.project_dir)

    def on_pushButton_set_db_path_clicked(self):
        self.cfg_dict['db_path_origin'] = QtWidgets.QFileDialog.getOpenFileName(self, texts.on_pushButton_set_db_path_clicked_dialog_title[Settings().language],
                                                                                os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'),
                                                                                texts.on_pushButton_set_db_path_clicked_dialog_text[Settings().language])[0]
        self.lineEdit_db_path.setText(self.cfg_dict['db_path_origin'])

    def on_pushButton_set_rows_path_clicked(self):
        self.cfg_dict['rows_path_origin'] = QtWidgets.QFileDialog.getOpenFileName(self, texts.on_pushButton_set_rows_path_clicked_dialog_title[Settings().language],
                                                                                  os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'),
                                                                                  texts.on_pushButton_set_rows_path_clicked_dialog_text[Settings().language])[0]
        self.lineEdit_rows_path.setText(self.cfg_dict['rows_path_origin'])

    def on_pushButton_set_template_path_clicked(self):
        self.cfg_dict['template_path_origin'] = QtWidgets.QFileDialog.getOpenFileName(self, texts.on_pushButton_set_template_path_clicked_dialog_title[Settings().language],
                                                                                      os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'),
                                                                                      texts.on_pushButton_set_template_path_clicked_dialog_text[Settings().language])[0]
        self.lineEdit_template_path.setText(self.cfg_dict['template_path_origin'])

    def on_checkBox_use_sheet_names_toggled(self):
        if self.checkBox_use_sheet_names.isChecked():
            self.checkBox_write_to_single_field.setChecked(False)
            self.checkBox_write_to_single_field.setEnabled(False)
            self.plainTextEdit_field_names_payload.setEnabled(False)
        else:
            self.checkBox_write_to_single_field.setEnabled(True)
            self.plainTextEdit_field_names_payload.setEnabled(True)

    def on_pushButton_Save_clicked(self):
        if self.does_config_appear_to_be_valid():
            self.gather_remaining_config()
            self.copy_config_files()
            self.save_config()
            show_msgbox(texts.on_pushButton_Save_clicked_success_msgbox_title[Settings().language],
                        texts.on_pushButton_Save_clicked_success_msgbox_text[Settings().language])
            self.close()
        else:
            show_msgbox(texts.on_pushButton_Save_clicked_failure_msgbox_title[Settings().language],
                        texts.on_pushButton_Save_clicked_failure_msgbox_text[Settings().language])

    def does_config_appear_to_be_valid(self):
        if self.are_all_paths_given() and \
           self.is_fields_logic_consistent() and \
           self.is_template_consistent() and \
           self.is_database_consistent():
            return True

    def are_all_paths_given(self):
        if all([self.project_dir, self.cfg_dict['db_path_origin'], self.cfg_dict['rows_path_origin'],
                self.cfg_dict['template_path_origin']]):
            return True
        else:
            show_msgbox(texts.are_all_paths_given_msgbox_title[Settings().language],
                        texts.are_all_paths_given_msgbox_text[Settings().language])
            return False

    def is_fields_logic_consistent(self):
        if self.checkBox_use_sheet_names.isChecked():
            return True
        else:
            num_given_fields = len(self.plainTextEdit_field_names_payload.toPlainText().splitlines())
            if self.checkBox_write_to_single_field.isChecked():
                if num_given_fields == 1:
                    return True
                else:
                    show_msgbox(texts.is_fields_logic_consistent_field_names_inconsistent_msgbox_title[Settings().language],
                                texts.is_fields_logic_consistent_field_names_inconsistent_msgbox_text[Settings().language])
                    return False
            else:
                if num_given_fields > 1:
                    return True
                else:
                    show_msgbox(texts.is_fields_logic_consistent_num_given_fields_inconsistent_msgbox_title[Settings().language],
                                texts.is_fields_logic_consistent_num_given_fields_inconsistent_msgbox_text[Settings().language])
                    return False

    def is_template_consistent(self):
        _, _, field_replacements, _, _, succeeded = read_rows_data(self.cfg_dict['rows_path_origin'])
        if succeeded:
            names_to_match = list(field_replacements.keys())
            if self.checkBox_use_sheet_names.isChecked():
                try:
                    names_to_match.extend(pd.ExcelFile(self.cfg_dict['db_path_origin']).sheet_names)
                except Exception as e:
                    show_msgbox(texts.is_template_consistent_error_opening_db_msgbox_title[Settings().language],
                                texts.is_template_consistent_error_opening_db_msgbox_text[Settings().language].replace('_exception', str(e)))
                    return False
            else:
                names_to_match.extend(self.plainTextEdit_field_names_payload.toPlainText().splitlines())
            if is_list_in_template_form_names(self.cfg_dict['template_path_origin'], names_to_match):
                return True
            else:
                show_msgbox(texts.is_template_consistent_field_names_inconsistent_msgbox_title[Settings().language],
                            texts.is_template_consistent_field_names_inconsistent_msgbox_text[Settings().language])
                return False
        else:
            show_msgbox(texts.is_template_consistent_error_reading_rows_msgbox_title[Settings().language],
                        texts.is_template_consistent_error_reading_rows_msgbox_text[Settings().language])
            return False

    def is_database_consistent(self):
        try:
            db = pd.read_excel(self.cfg_dict['db_path_origin'], engine='openpyxl')
            if db.shape[0] >= 1 and db.shape[1] >= 1:
                return True
            else:
                show_msgbox(texts.is_database_consistent_bad_shape_msgbox_title[Settings().language],
                            texts.is_database_consistent_bad_shape_msgbox_text[Settings().language])
                return False
        except Exception as e:
            show_msgbox(texts.new_config_is_database_consistent_error_opening_db_msgbox_title[Settings().language],
                        texts.new_config_is_database_consistent_error_opening_db_msgbox_text[Settings().language].replace('_exception', str(e)))
            return False

    def gather_remaining_config(self):
        self.cfg_dict['language'] = Settings().language
        self.cfg_dict['write_to_single_field'] = self.checkBox_write_to_single_field.isChecked()
        self.cfg_dict['field_names_payload'] = self.plainTextEdit_field_names_payload.toPlainText().splitlines()
        self.cfg_dict['use_sheet_names'] = self.checkBox_use_sheet_names.isChecked()
        self.cfg_dict['version'] = config_params.glob_cfg_version_string
        self.cfg_dict['created_by'] = os.getlogin()
        self.cfg_dict['created_on'] = socket.gethostname()
        self.cfg_dict['created_at'] = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        self.cfg_dict['review_editable'] = self.checkBox_review_editable.isChecked()

    def copy_config_files(self):
        shutil.copyfile(self.cfg_dict['db_path_origin'], self.project_dir + '/db.xlsx')
        shutil.copyfile(self.cfg_dict['rows_path_origin'], self.project_dir + '/rows.xlsx')
        shutil.copyfile(self.cfg_dict['template_path_origin'], self.project_dir + '/template' + os.path.splitext(self.cfg_dict['template_path_origin'])[-1])

    def save_config(self):
        file_path = self.project_dir + '/' + glob_cfg_config_filename
        with open(file_path, 'w') as f:
            json.dump(self.cfg_dict, f, indent=4, ensure_ascii=False)
        os.chmod(file_path, 0o400)
