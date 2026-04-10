# -*- coding: utf-8 -*-
from common import *
from config import config
from main_window import MainWindow
import click
from click_option_group import optgroup, MutuallyExclusiveOptionGroup
import glob
import os
import main_texts as texts
from config_params import *
import pandas as pd
import numpy as np
import sys
import cProfile
import pstats


def start_profiler():
    profiler = cProfile.Profile()
    profiler.enable()
    return profiler


def stop_profiler(profiler):
    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('cumulative')
    stats.print_stats()
    return stats


@click.command()
@click.option('--projectdir', '-p', help='Explicit config mode: specify a project directory', type=click.Path(exists=True))
@click.help_option('-h', '--help')
def main(projectdir):
    # profiler = start_profiler()
    app = QtWidgets.QApplication(sys.argv)
    set_language_from_settings_file()
    project_dir, session_state, config_found = get_project_dir(projectdir)
    if config_found:
        cfg_dict, succeeded = load_cfg(project_dir + '/' + glob_cfg_config_filename)
        if succeeded:
            msgbox_title_conf_dict, msgbox_text_conf_dict, error_list = cfg_pre_check(project_dir, cfg_dict)
            if len(error_list) == 0:
                mainwindow = MainWindow(project_dir, cfg_dict, session_state)
                mainwindow.show()
                # stop_profiler(profiler)
                sys.exit(app.exec())
            else:
                show_msgbox(msgbox_title_conf_dict, msgbox_text_conf_dict + '\n' + str(error_list))
        else:
            show_msgbox(texts.main_msgbox_load_cfg_title[Settings().language],
                        texts.main_msgbox_load_cfg_text[Settings().language])


def set_language_from_settings_file():
    language_temp = get_setting_from_file('language')
    if language_temp and language_temp in glob_cfg_supported_languages:
        Settings().language = language_temp
    else:
        Settings().language = 'eng'


def get_project_dir(project_dir_in):
    if project_dir_in:
        if os.path.isdir(project_dir_in):
            project_dir = project_dir_in.replace('\\', '/')
            session_state = None
            succeeded = True
        else:
            show_msgbox(texts.get_project_dir_not_found_title[Settings().language],
                        texts.get_project_dir_not_found_text[Settings().language])
            project_dir = None
            session_state = None
            succeeded = False
    else:
        project_dir, session_state, succeeded = get_config()
    return project_dir, session_state, succeeded


def get_config():
    project_dir = None
    session_state = None
    succeeded = False
    cfg_window = config()
    cfg_window.exec()
    if cfg_window.result():
        cfg_file_ext = os.path.splitext(cfg_window.selected_file_path)[1]
        if cfg_file_ext == '.json':
            project_dir = os.path.dirname(cfg_window.selected_file_path)
            succeeded = True
        elif cfg_file_ext == ".session":
            project_dir, session_state, succeeded = load_session(cfg_window.selected_file_path)
        else:
            show_msgbox(texts.get_config_ext_title[Settings().language], texts.get_config_ext_text[Settings().language])
    return project_dir, session_state, succeeded


def cfg_pre_check(project_dir, cfg_dict):
    error_list = []
    msgbox_title = texts.cfg_pre_check_msgbox_title[Settings().language]
    msgbox_text = {}
    for nec_key in glob_cfg_necessary_keys:
        if nec_key not in cfg_dict.keys() or cfg_dict[nec_key] is None:
            msgbox_text = texts.cfg_pre_check_msgbox_nec_keys_text[Settings().language]
            if 1 not in error_list:        # 1 means that some necessary key is missing
                error_list.append(1)
    db_path = os.path.join(project_dir, 'db.xlsx')
    rows_path = os.path.join(project_dir, 'rows.xlsx')
    if not os.path.isfile(db_path):
        msgbox_text = texts.cfg_pre_check_msgbox_db_not_found_text[Settings().language]
        error_list.append(1)
    if not os.path.isfile(rows_path):
        msgbox_text = texts.cfg_pre_check_msgbox_rows_not_found_text[Settings().language]
        error_list.append(2)
    if len(glob.glob(os.path.join(project_dir, 'template.*'))) > 0:
        template_path = glob.glob(os.path.join(project_dir, 'template.*'))[0]
        if os.path.isfile(db_path):
            _, _, field_replacements, _, _, succeeded = read_rows_data(rows_path)
            if succeeded:
                names_to_match = list(field_replacements.keys())
                if cfg_dict['use_sheet_names']:
                    [names_to_match.append(sheet_name) for sheet_name in pd.ExcelFile(db_path).sheet_names]
                    if not is_list_in_template_form_names(template_path, names_to_match):
                        msgbox_text = texts.cfg_pre_check_msgbox_field_names_mismatch_text[Settings().language]
                        error_list.append(3)
            else:
                error_list.append(4)
        # else case handled a few lines above
    else:
        msgbox_text = texts.cfg_pre_check_msgbox_template_not_found_text[Settings().language]
        error_list.append(5)
    # TODO Check if name field in config fits to the template
    return msgbox_title, msgbox_text, error_list


if __name__ == '__main__':
    main()
