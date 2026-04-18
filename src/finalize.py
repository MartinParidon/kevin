import gui_finalize
from common import *
from PySide6.QtCore import Qt
import shutil
from win32com.client import Dispatch
from datetime import datetime
from pathlib import Path
import fillpdf2
import glob
import pandas as pd
import finalize_texts as texts


class finalize(QtWidgets.QDialog, gui_finalize.Ui_Dialog):
    def __init__(self, path_to_final=None):
        super(finalize, self).__init__()
        self.setupUi(self)
        self.out_dir = ''
        self.language = Settings().language
        self.listWidget.addItem(path_to_final)
        self.listWidget.setDragEnabled(True)
        self.listWidget.setDropIndicatorShown(True)
        self.listWidget.setAcceptDrops(True)
        self.listWidget.setDefaultDropAction(Qt.MoveAction)
        self.setWindowTitle(texts.finalize_window_title[self.language])
        self.label_Drag_Drop.setText(texts.finalize_label_Drag_Drop[self.language])
        self.label_Output_Folder.setText(texts.finalize_label_Output_Folder[self.language])
        self.pushButton_Select_Output_Folder.setText(texts.finalize_pushButton_Select_Output_Folder[self.language])
        self.pushButton_Send_Data.setText(texts.finalize_pushButton_Send_Data[self.language])
        self.pushButton_Select_Output_Folder.clicked.connect(self.on_pushButton_Select_Output_Folder_clicked)
        self.pushButton_Send_Data.clicked.connect(self.on_pushButton_Finalize_clicked)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            for item in self.listWidget.selectedItems():
                self.listWidget.takeItem(self.listWidget.row(item))

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            for path in event.mimeData().urls():
                path_to_item = path.toLocalFile()
                if os.path.isdir(path.toLocalFile()):
                    for root, dirs, files in os.walk(path_to_item):
                        root = root.replace('\\', '/')
                        for file in files:
                            self.add_to_listWidget(root + '/' + file, ['.final'])
                else:
                    self.add_to_listWidget(path_to_item, ['.session', '.final', '.xlsx'])

    def on_pushButton_Select_Output_Folder_clicked(self):
        self.out_dir = QtWidgets.QFileDialog.getExistingDirectory(self, texts.on_pushButton_Select_Output_Folder_clicked_title[self.language], os.path.expanduser('~'), QtWidgets.QFileDialog.ShowDirsOnly)
        self.lineEdit_Output_Folder.setText(self.out_dir)

    def on_pushButton_Finalize_clicked(self):
        paths_to_sessions_or_stationary_data = [str(self.listWidget.item(i).text()) for i in range(self.listWidget.count())]
        if not self.out_dir:
            show_msgbox(texts.on_pushButton_Finalize_clicked_no_out_dir_title[self.language],
                        texts.on_pushButton_Finalize_clicked_no_out_dir_text[self.language])
            return
        else:
            success = True
            for path in paths_to_sessions_or_stationary_data:
                success = success and lock_dir_and_write_data(path, self.out_dir, self.language)
            if success:
                show_msgbox(texts.on_pushButton_Finalize_clicked_completed_title[self.language],
                            texts.on_pushButton_Finalize_clicked_completed_text[self.language])

    def add_to_listWidget(self, path_to_item, ext_list):
        item_list = [str(self.listWidget.item(i).text()) for i in range(self.listWidget.count())]
        ext = os.path.splitext(path_to_item)[1]
        if path_to_item not in item_list and ext in ext_list:
            self.listWidget.addItem(path_to_item)


def lock_dir_and_write_data(path_to_input_file, out_dir, language):
    ret = False
    if os.path.isdir(out_dir) and os.access(out_dir, os.W_OK):
        locked_filename = get_locked_filename_if_exists(out_dir)
        if not locked_filename:
            locked_filepath = make_locked_file(out_dir)
            if path_to_input_file.endswith('.xlsx'):
                high_level_write_fct = write_xlsx_output
            elif path_to_input_file.endswith('.session') or path_to_input_file.endswith('.final'):
                high_level_write_fct = write_session_output
            else:
                return
            if high_level_write_fct(path_to_input_file, out_dir, language):
                unlocked_filepath = locked_filepath.replace('.locked', '.unlocked')
                os.rename(locked_filepath, unlocked_filepath)
                ret = True
            else:
                show_msgbox(texts.send_data_to_template_write_failed_title[language],
                            texts.send_data_to_template_write_failed_text[language])
        else:
            locked_data = os.path.splitext(locked_filename)[0].split('_')
            show_msgbox(texts.send_data_to_template_msgbox2_title[language],
                        texts.send_data_to_template_msgbox2_text[language].replace('_timestamp',
                                                                                   locked_data[0]).replace(
                            '_computername', locked_data[1]).replace('_username', locked_data[2]))
    else:
        show_msgbox(texts.send_data_to_template_outdir_issue_title[language],
                    texts.send_data_to_template_outdir_issue_text[language].replace('_out_dir', out_dir))
    return ret


def get_locked_filename_if_exists(out_dir):
    for filename in os.listdir(out_dir):
        if filename.endswith('.locked'):
            return filename
    return None


def make_locked_file(out_dir):
    new_locked_filename = datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + '_' + os.environ['COMPUTERNAME'] + '_' + os.getlogin() + '.locked'
    new_locked_filepath = os.path.join(out_dir, new_locked_filename)
    unlocked_files = [f for f in os.listdir(out_dir) if f.endswith('.unlocked')]
    if unlocked_files:
        unlocked_filepath = os.path.join(out_dir, unlocked_files[0])
        os.rename(unlocked_filepath, new_locked_filepath)
    else:
        with open(new_locked_filepath, 'w'):
            pass
    return new_locked_filepath


def get_col_values(project_dir, language):
    db = pd.read_excel(os.path.join(project_dir, 'db.xlsx'), sheet_name=None)
    for entry_key in db.keys():
        db[entry_key].columns = db[entry_key].columns.astype(str)
    col_values_before_check = list(db.keys())
    if len(col_values_before_check) > glob_cfg_max_num_cols:
        show_msgbox(texts.get_col_and_row_values_title2[language],
                    texts.get_col_and_row_values_text2[language].replace('_num_sheets',
                                                                              str(glob_cfg_max_num_cols)).replace(
                        '_num_ignored', str(len(col_values_before_check) - glob_cfg_max_num_cols)))
    col_values = col_values_before_check[0:min(glob_cfg_max_num_cols, len(col_values_before_check))]
    return col_values


def get_existing_output_files(out_dir):
    docx_files = []
    pdf_files = []
    for filename in os.listdir(out_dir):
        if filename.endswith('.docx'):
            docx_files.append(os.path.join(out_dir, filename))
        elif filename.endswith('.pdf'):
            pdf_files.append(os.path.join(out_dir, filename))
    if docx_files and pdf_files:
        return None, False
    file_paths = docx_files if docx_files else pdf_files
    if docx_files:
        is_word = True
    else:
        is_word = False
    return file_paths, is_word


def write_xlsx_output(path_to_xlsx, out_dir, language):
    df = pd.read_excel(path_to_xlsx, header=None).astype(str)
    out_dict = dict(zip(df.iloc[:, 0], df.iloc[:, 1]))
    file_paths, is_word = get_existing_output_files(out_dir)
    if file_paths is not None:
        word = None
        try:
            if is_word:
                try:
                    word = Dispatch("Word.Application")
                except Exception as e:
                    show_msgbox(texts.send_data_to_template_word_issue_title[language],
                                texts.send_data_to_template_word_issue_text[language].replace('_exception', str(e)))
                    if word is not None:  # Just to be extra sure...
                        word.Application.Quit(-1)
                    return False
            success = True
            for file_path in file_paths:
                success = success and write_single_file_for_xlsx(file_path, out_dict, is_word, word)
        except Exception as e:
            show_msgbox(texts.send_data_to_template_write_issue_title[language],
                        texts.send_data_to_template_write_issue_text[language].replace('_exception', str(e)))
            return False
        if is_word:
            word.Application.Quit(-1)
        return success
    else:
        return False


def write_single_file_for_xlsx(file_path, out_dict, is_word, word):
    try:
        if is_word:
            success, exception = write_text_to_docx(file_path, out_dict, word)
        else:
            success, exception = write_text_to_pdf(file_path, out_dict)
        return success
    except Exception as e:
        return False


def write_session_output(path_to_session, out_dir, language):
    project_dir, session_state, succeeded = load_session(path_to_session)
    if succeeded:
        template_path = glob.glob(os.path.join(project_dir, 'template.*'))[0]
        doc_type = os.path.splitext(template_path)[1]
        if doc_type == '.docx':
            write_fct = write_text_to_docx
        elif doc_type == '.pdf':
            write_fct = write_text_to_pdf
        else:
            show_msgbox(texts.send_data_to_template_doc_type_issue_title[language],
                        texts.send_data_to_template_doc_type_issue_text[language].replace('_doc_type', doc_type))
            return False
        num_rows = len(session_state.texts)
        if num_rows > 0:
            word = None
            try:
                if doc_type == '.docx':
                    try:
                        word = Dispatch("Word.Application")
                    except Exception as e:
                        show_msgbox(texts.send_data_to_template_word_issue_title[language],
                                    texts.send_data_to_template_word_issue_text[language].replace('_exception', str(e)))
                        if word is not None:  # Just to be extra sure...
                            word.Application.Quit(-1)
                        return False
                success = True
                for i_row in range(num_rows):
                    if session_state.review_statuses[i_row] == review_status.finished:
                        success = success and write_single_file_for_session(session_state, word, i_row, project_dir, session_state, template_path, out_dir, doc_type, write_fct, language)
                    else:
                        success = False
            except Exception as e:
                show_msgbox(texts.send_data_to_template_write_issue_title[language],
                            texts.send_data_to_template_write_issue_text[language].replace('_exception', str(e)))
                return False
            if word is not None:
                word.Application.Quit(-1)
            return success
        else:
            return False
    else:
        return False


def write_single_file_for_session(session_state, word, i_row, project_dir, state, template_path, out_dir, doc_type, write_fct, language):
    col_values = get_col_values(project_dir, language)
    row_values, _, field_replacements, _, _, succeeded = read_rows_data(os.path.join(project_dir, 'rows.xlsx'))
    if not succeeded:
        show_msgbox(texts.write_single_file_for_session_title1[language],
                    texts.write_single_file_for_session_text1[language])
        return False
    out_dict = make_out_dict(session_state, i_row, col_values, state, field_replacements)
    out_path = out_dir + '/' + row_values[i_row] + doc_type
    success_cpy, e_cpy = copy_template(out_path, template_path)
    if success_cpy:
        success_write, e_write = write_fct(out_path, out_dict, word)
        if not success_write:
            show_msgbox(texts.write_single_file_for_session_title2[language],
                        texts.write_single_file_for_session_text2[language].replace('_exception', str(e_write)))
            return False
        else:
            return True
    else:
        show_msgbox(texts.write_single_file_for_session_title2[language],
                    texts.write_single_file_for_session_text2[language].replace('_exception', str(e_cpy)))
        return False


def copy_template(out_path, template_path):
    if not os.path.isfile(out_path):
        try:
            shutil.copyfile(template_path, out_path)
        except Exception as e:
            return False, e
    return True, None


def make_out_dict(session_state, i_row, col_values, state, field_replacements):
    if session_state.cfg_dict['use_sheet_names']:
        out_dict = {col_values[i_col]: text for (i_col, text) in state.texts[i_row].items()}
    elif not session_state.cfg_dict['write_to_single_field']:
        out_dict = {session_state.cfg_dict['field_names_payload'][i_col]: text for (i_col, text) in state.texts[i_row].items()}
    else:
        values = [text for text in state.texts[i_row].values() if text != '']
        out_dict = {session_state.cfg_dict['field_names_payload'][0]: ' '.join(values)}
    for key, val in field_replacements.items():
        out_dict[key] = val[i_row]
    return out_dict


def write_text_to_docx(out_path, out_dict, word):
    doc = word.Documents.Open(str(Path(out_path)))
    controls = {}
    try:
        for story in doc.StoryRanges:
            for control in story.ContentControls:
                controls[control.Title] = control
        for key, value in zip(list(out_dict.keys()), list(out_dict.values())):
            controls[key].Range.Text = value
        # doc.SaveAs2(out_path, FileFormat=12)
        # doc.Close()???
        return True, None
    except Exception as e:
        return False, e


def write_text_to_pdf(out_path, out_dict, word=None):
    try:
        fillpdf2.write_fillable_pdf(out_path, out_path, out_dict, flatten=False)
        return True, None
    except Exception as e:
        return False, e
