import gui_config
from config_creator import *
from finalize import *
import config_texts as texts
import sys


class config(QtWidgets.QDialog, gui_config.Ui_Dialog):
    def __init__(self):
        super(config, self).__init__()
        self.setupUi(self)
        self.change_language(Settings().language)
        self.selected_file_path = ""
        self.comboBox_init()
        self.comboBox.currentIndexChanged.connect(self.on_comboBox_currentIndexChanged)
        self.pushButton_load_config.clicked.connect(self.on_pushButton_load_config_clicked)
        self.pushButton_new_config.clicked.connect(self.on_pushButton_new_config_clicked)
        self.pushButton_finalize.clicked.connect(self.on_pushButton_finalize_clicked)

    def comboBox_init(self):
        if Settings().language == 'eng':
            self.comboBox.setCurrentIndex(0)
        elif Settings().language == 'ger':
            self.comboBox.setCurrentIndex(1)
        elif Settings().language == 'esp':
            self.comboBox.setCurrentIndex(2)
        elif Settings().language == 'rus':
            self.comboBox.setCurrentIndex(3)

    def on_comboBox_currentIndexChanged(self):
        if self.comboBox.currentIndex() == 0:
            self.change_language('eng')
        elif self.comboBox.currentIndex() == 1:
            self.change_language('ger')
        elif self.comboBox.currentIndex() == 2:
            self.change_language('esp')
        elif self.comboBox.currentIndex() == 3:
            self.change_language('rus')

    def change_language(self, language):
        Settings().language = language
        self.pushButton_new_config.setText(texts.change_language_new_config_text[language])
        self.pushButton_load_config.setText(texts.change_language_load_config_text[language])
        self.pushButton_finalize.setText(texts.change_language_finalize_text[language])
        self.update()

    def closeEvent(self, event):
        self.update_settings()
        self.reject()

    def update_settings(self):
        config_dict = dict()
        config_dict['language'] = Settings().language


    def on_pushButton_load_config_clicked(self):
        if getattr(sys, 'frozen', False):
            executable_path = os.path.dirname(sys.executable)
        else:
            executable_path = os.path.dirname(os.path.abspath(__file__))
        self.selected_file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, texts.on_pushButton_load_config_clicked_dialog_title[Settings().language],
                                                                           executable_path,
                                                                           "(*.session *.json)",
                                                                           texts.on_pushButton_load_config_clicked_dialog_text[Settings().language])
        if self.selected_file_path:
            self.update_settings()
            self.accept()

    def on_pushButton_new_config_clicked(self):
        new_config_window = config_creator()
        new_config_window.exec()

    def on_pushButton_finalize_clicked(self):
        finalize_window = finalize()
        finalize_window.exec()
