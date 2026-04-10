import gui_review
from common import *

review_window_title = {'eng': 'Review Texts',
                       'ger': 'Texte Prüfen',
                       'esp': 'Revisar textos',
                       'rus': 'Проверить тексты'}


class review(QtWidgets.QDialog, gui_review.Ui_Dialog):
    def __init__(self):
        super(review, self).__init__()
        self.setupUi(self)
        self.setWindowTitle(review_window_title[Settings().language])
        self.labels = {}
        self.plainTextEdits = {}
        self.shuffle_pushButtons = {}
