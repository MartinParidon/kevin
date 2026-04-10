# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'config.ui'
##
## Created by: Qt User Interface Compiler version 6.11.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(232, 127)
        icon = QIcon()
        icon.addFile(u"../logo.ico", QSize(), QIcon.Mode.Normal, QIcon.State.On)
        Dialog.setWindowIcon(icon)
        self.verticalLayout_2 = QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.comboBox = QComboBox(Dialog)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")

        self.verticalLayout.addWidget(self.comboBox)

        self.pushButton_new_config = QPushButton(Dialog)
        self.pushButton_new_config.setObjectName(u"pushButton_new_config")

        self.verticalLayout.addWidget(self.pushButton_new_config)

        self.pushButton_load_config = QPushButton(Dialog)
        self.pushButton_load_config.setObjectName(u"pushButton_load_config")

        self.verticalLayout.addWidget(self.pushButton_load_config)

        self.pushButton_finalize = QPushButton(Dialog)
        self.pushButton_finalize.setObjectName(u"pushButton_finalize")

        self.verticalLayout.addWidget(self.pushButton_finalize)


        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Configure", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("Dialog", u"English", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("Dialog", u"Deutsch", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("Dialog", u"Espa\u00f1ol", None))
        self.comboBox.setItemText(3, QCoreApplication.translate("Dialog", u"P\u0443\u0441\u0441\u043a\u0438\u0439", None))

        self.pushButton_new_config.setText(QCoreApplication.translate("Dialog", u"Make New Config", None))
        self.pushButton_load_config.setText(QCoreApplication.translate("Dialog", u"Load Config or Session", None))
        self.pushButton_finalize.setText(QCoreApplication.translate("Dialog", u"Finalize", None))
    # retranslateUi

