from PySide6 import QtWidgets
import json
import common_texts as texts
from config_params import *
import os
import joblib
import win32com.client
from pathlib import Path
import fillpdf2
import pandas as pd
from packaging import version
import numpy as np


class review_status:
    not_yet_started = 1
    started = 2
    finished = 3


class Settings:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Settings, cls).__new__(cls)
            cls._instance.language = 'eng'
        return cls._instance


def show_msgbox(title, text):
    messageBox = QtWidgets.QMessageBox()
    messageBox.setWindowTitle(title)
    messageBox.setText(text)
    messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
    messageBox.setButtonText(QtWidgets.QMessageBox.Ok, texts.messageBoxOkText[Settings().language])
    messageBox.exec()


def show_msgbox_Ok_Cancel(title, text):
    messageBox = QtWidgets.QMessageBox()
    messageBox.setWindowTitle(title)
    messageBox.setText(text)
    messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
    messageBox.setButtonText(QtWidgets.QMessageBox.Ok, texts.messageBoxOkText[Settings().language])
    messageBox.setButtonText(QtWidgets.QMessageBox.Cancel, texts.messageBoxCancelText[Settings().language])
    return messageBox.exec()


def show_msgbox_Yes_No(title, text):
    messageBox = QtWidgets.QMessageBox()
    messageBox.setWindowTitle(title)
    messageBox.setText(text)
    messageBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
    messageBox.setButtonText(QtWidgets.QMessageBox.Yes, texts.messageBoxYesText[Settings().language])
    messageBox.setButtonText(QtWidgets.QMessageBox.No, texts.messageBoxNoText[Settings().language])
    return messageBox.exec()


def show_msgbox_Yes_No_Cancel(title, text):
    messageBox = QtWidgets.QMessageBox()
    messageBox.setWindowTitle(title)
    messageBox.setText(text)
    messageBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel)
    messageBox.setButtonText(QtWidgets.QMessageBox.Yes, texts.messageBoxYesText[Settings().language])
    messageBox.setButtonText(QtWidgets.QMessageBox.No, texts.messageBoxNoText[Settings().language])
    messageBox.setButtonText(QtWidgets.QMessageBox.Cancel, texts.messageBoxCancelText[Settings().language])
    return messageBox.exec()


def get_uuid():
    obj = win32com.client.GetObject("winmgmts:root\\cimv2")
    products = obj.ExecQuery("SELECT UUID FROM Win32_ComputerSystemProduct")
    return next(iter(products)).UUID


def load_session(session_filepath):
    project_dir = None
    session_state = None
    succeeded = False
    try:
        project_dir_loaded = os.path.split(os.path.dirname(session_filepath))[0]
        session_state_loaded = joblib.load(session_filepath)
        cfg_path = project_dir_loaded + '/' + glob_cfg_config_filename
        if not os.path.exists(cfg_path):
            show_msgbox(texts.load_session_msgbox1_title[Settings().language],
                        texts.load_session_msgbox1_text[Settings().language])
        else:
            project_dir = project_dir_loaded
            session_state = session_state_loaded
            succeeded = True
            cfg, succeeded = load_cfg(cfg_path)
            if succeeded:
                if version.parse(session_state_loaded.cfg_dict['version']) < version.parse(glob_cfg_minimum_supported_version):
                    show_msgbox(texts.load_session_msgbox5_title[Settings().language],
                                texts.load_session_msgbox5_text[Settings().language].replace('_session_filepath', os.path.split(session_filepath)[1]).replace('_version_session', session_state_loaded.cfg_dict['version']).replace('_version_minimum', glob_cfg_minimum_supported_version))
                    succeeded = False
            else:
                show_msgbox(texts.load_session_msgbox3_title[Settings().language],
                            texts.load_session_msgbox3_text[Settings().language].replace('_cfg_path', cfg_path.split('/')[-1]))
    except Exception as e:
        show_msgbox(texts.load_session_msgbox4_title[Settings().language],
                    texts.load_session_msgbox4_text[Settings().language].replace('_exception', str(e)))
    return project_dir, session_state, succeeded


def load_cfg(cfg_path_to_load):
    with open(cfg_path_to_load, 'r') as f:
        try:
            cfg = json.load(f)
            succeeded = True
        except Exception as e:
            show_msgbox(texts.load_cfg_msgbox_title[Settings().language],
                        texts.load_cfg_msgbox_text[Settings().language].replace('_exception', str(e)))
            cfg = None
            succeeded = True
    return cfg, succeeded


def send_mail():
    subject = texts.send_mail_subject[Settings().language].replace('_version_string', glob_cfg_version_string)
    command = f'START mailto:{glob_cfg_issue_mail_address}?subject={subject}^&body='
    try:
        os.system(command)
    except Exception as e:
        show_msgbox(texts.send_mail_msgbox_title_exception_title[Settings().language],
                    texts.send_mail_msgbox_title_exception_text[Settings().language].replace('_exception', str(e)))


def get_setting_from_file(setting):
    if os.path.exists(glob_cfg_settings_file_path):
        with open(glob_cfg_settings_file_path, 'r') as f:
            try:
                settings_dict = json.load(f)
                if setting in settings_dict.keys():
                    return settings_dict[setting]
                else:
                    return None
            except Exception:
                return None
    else:
        return None


def write_settings_to_file(settings_dict):
    os.makedirs(os.path.dirname(glob_cfg_settings_file_path), exist_ok=True)
    try:
        with open(glob_cfg_settings_file_path, 'w') as f:
            json.dump(settings_dict, f)
    except Exception:
        pass

def is_list_in_template_form_names(template_path, names_to_match):
    field_names_tpl = []
    ext = os.path.splitext(template_path)[1]
    try:
        if ext == '.docx':
            word = win32com.client.Dispatch("Word.Application")
            doc = word.Documents.Open(str(Path(os.path.abspath(template_path))))
            for story in doc.StoryRanges:
                for control in story.ContentControls:
                    field_names_tpl.append(control.Title)
            word.Application.Quit(-1)
        elif ext == '.pdf':
            field_names_tpl = list(fillpdf2.get_form_fields(template_path).keys())
        if not all([name_to_match in field_names_tpl for name_to_match in names_to_match]):
            return False
        else:
            return True
    except Exception as e:
        show_msgbox(texts.is_list_in_template_form_names_msgbox_title[Settings().language],
                    texts.is_list_in_template_form_names_msgbox_text[Settings().language].replace('_exception', str(e)))
        return False


def read_rows_data(path_to_rows_file):
    succeeded = True
    all_sheets = pd.read_excel(path_to_rows_file, sheet_name=None, dtype=str)
    cleaned_sheets = {
        sheet_name: df.replace(np.nan, "").to_dict()
        for sheet_name, df in all_sheets.items()
    }
    rows_raw = next(iter(cleaned_sheets.values()))
    string_in_field_replacements = {}
    field_replacements = {}
    placeholder_options = {}
    placeholders = {}
    row_values = next(iter(rows_raw.values()))
    del rows_raw[next(iter(rows_raw))]
    for key in rows_raw.keys():
        if key[0] == '_' and key[1] == '_':
            field_replacements[key.replace("__", "")] = rows_raw[key]
        elif key[0] == '_' and key[-1] == '_':
            string_in_field_replacements[key] = rows_raw[key]
        elif key in cleaned_sheets.keys():
            for individual_option in list(rows_raw[key].values()):
                if individual_option not in list(cleaned_sheets[key].keys())[1:]:
                    succeeded = False
                    show_msgbox(texts.read_rows_data_msgbox_title1[Settings().language],
                                texts.read_rows_data_msgbox_text1[Settings().language].replace('_individual_option', individual_option).replace('_key', key))
                    break
            placeholder_options[key] = cleaned_sheets[key]
            placeholders[key] = rows_raw[key]
        else:
            succeeded = False
            show_msgbox(texts.read_rows_data_msgbox_title2[Settings().language],
                        texts.read_rows_data_msgbox_text2[Settings().language].replace('_key', key))
            break
    return row_values, string_in_field_replacements, field_replacements, placeholder_options, placeholders, succeeded
