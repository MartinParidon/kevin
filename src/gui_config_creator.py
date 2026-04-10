# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'config_creator.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDialog, QFrame,
    QLabel, QLineEdit, QPlainTextEdit, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(271, 629)
        icon = QIcon()
        icon.addFile(u"../logo.ico", QSize(), QIcon.Mode.Normal, QIcon.State.On)
        Dialog.setWindowIcon(icon)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_Paths = QLabel(Dialog)
        self.label_Paths.setObjectName(u"label_Paths")
        font = QFont()
        font.setBold(True)
        self.label_Paths.setFont(font)

        self.verticalLayout.addWidget(self.label_Paths)

        self.lineEdit_project_dir = QLineEdit(Dialog)
        self.lineEdit_project_dir.setObjectName(u"lineEdit_project_dir")
        self.lineEdit_project_dir.setReadOnly(True)

        self.verticalLayout.addWidget(self.lineEdit_project_dir)

        self.pushButton_set_project_dir = QPushButton(Dialog)
        self.pushButton_set_project_dir.setObjectName(u"pushButton_set_project_dir")

        self.verticalLayout.addWidget(self.pushButton_set_project_dir)

        self.lineEdit_db_path = QLineEdit(Dialog)
        self.lineEdit_db_path.setObjectName(u"lineEdit_db_path")
        self.lineEdit_db_path.setReadOnly(True)

        self.verticalLayout.addWidget(self.lineEdit_db_path)

        self.pushButton_set_db_path = QPushButton(Dialog)
        self.pushButton_set_db_path.setObjectName(u"pushButton_set_db_path")

        self.verticalLayout.addWidget(self.pushButton_set_db_path)

        self.lineEdit_rows_path = QLineEdit(Dialog)
        self.lineEdit_rows_path.setObjectName(u"lineEdit_rows_path")
        self.lineEdit_rows_path.setReadOnly(True)

        self.verticalLayout.addWidget(self.lineEdit_rows_path)

        self.pushButton_set_rows_path = QPushButton(Dialog)
        self.pushButton_set_rows_path.setObjectName(u"pushButton_set_rows_path")

        self.verticalLayout.addWidget(self.pushButton_set_rows_path)

        self.lineEdit_template_path = QLineEdit(Dialog)
        self.lineEdit_template_path.setObjectName(u"lineEdit_template_path")
        self.lineEdit_template_path.setReadOnly(False)

        self.verticalLayout.addWidget(self.lineEdit_template_path)

        self.pushButton_set_template_path = QPushButton(Dialog)
        self.pushButton_set_template_path.setObjectName(u"pushButton_set_template_path")

        self.verticalLayout.addWidget(self.pushButton_set_template_path)

        self.line_after_Paths = QFrame(Dialog)
        self.line_after_Paths.setObjectName(u"line_after_Paths")
        self.line_after_Paths.setFrameShape(QFrame.Shape.HLine)
        self.line_after_Paths.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line_after_Paths)

        self.label_Fields = QLabel(Dialog)
        self.label_Fields.setObjectName(u"label_Fields")
        self.label_Fields.setFont(font)

        self.verticalLayout.addWidget(self.label_Fields)

        self.checkBox_use_sheet_names = QCheckBox(Dialog)
        self.checkBox_use_sheet_names.setObjectName(u"checkBox_use_sheet_names")

        self.verticalLayout.addWidget(self.checkBox_use_sheet_names)

        self.checkBox_write_to_single_field = QCheckBox(Dialog)
        self.checkBox_write_to_single_field.setObjectName(u"checkBox_write_to_single_field")

        self.verticalLayout.addWidget(self.checkBox_write_to_single_field)

        self.plainTextEdit_field_names_payload = QPlainTextEdit(Dialog)
        self.plainTextEdit_field_names_payload.setObjectName(u"plainTextEdit_field_names_payload")
        self.plainTextEdit_field_names_payload.setEnabled(True)

        self.verticalLayout.addWidget(self.plainTextEdit_field_names_payload)

        self.line = QFrame(Dialog)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.checkBox_review_editable = QCheckBox(Dialog)
        self.checkBox_review_editable.setObjectName(u"checkBox_review_editable")

        self.verticalLayout.addWidget(self.checkBox_review_editable)

        self.line_2 = QFrame(Dialog)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line_2)

        self.label_Save = QLabel(Dialog)
        self.label_Save.setObjectName(u"label_Save")
        self.label_Save.setFont(font)

        self.verticalLayout.addWidget(self.label_Save)

        self.pushButton_Save = QPushButton(Dialog)
        self.pushButton_Save.setObjectName(u"pushButton_Save")

        self.verticalLayout.addWidget(self.pushButton_Save)

        self.pushButton_Cancel = QPushButton(Dialog)
        self.pushButton_Cancel.setObjectName(u"pushButton_Cancel")

        self.verticalLayout.addWidget(self.pushButton_Cancel)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label_Paths.setText(QCoreApplication.translate("Dialog", u"Paths", None))
        self.lineEdit_project_dir.setPlaceholderText(QCoreApplication.translate("Dialog", u"Project Directory", None))
        self.pushButton_set_project_dir.setText(QCoreApplication.translate("Dialog", u"Set Project Directory", None))
        self.lineEdit_db_path.setPlaceholderText(QCoreApplication.translate("Dialog", u"Database File Path", None))
        self.pushButton_set_db_path.setText(QCoreApplication.translate("Dialog", u"Set Database File Path", None))
        self.lineEdit_rows_path.setPlaceholderText(QCoreApplication.translate("Dialog", u"Rows File Path", None))
        self.pushButton_set_rows_path.setText(QCoreApplication.translate("Dialog", u"Set Rows File Path", None))
        self.lineEdit_template_path.setText("")
        self.lineEdit_template_path.setPlaceholderText(QCoreApplication.translate("Dialog", u"Template File Path", None))
        self.pushButton_set_template_path.setText(QCoreApplication.translate("Dialog", u"Set Template File Path", None))
        self.label_Fields.setText(QCoreApplication.translate("Dialog", u"Fields", None))
        self.checkBox_use_sheet_names.setText(QCoreApplication.translate("Dialog", u"Use Sheet names from Database File", None))
        self.checkBox_write_to_single_field.setText(QCoreApplication.translate("Dialog", u"Write Output to single Form Field", None))
        self.plainTextEdit_field_names_payload.setPlaceholderText(QCoreApplication.translate("Dialog", u"Name(s) of Form Field(s) in Template File", None))
        self.checkBox_review_editable.setText(QCoreApplication.translate("Dialog", u"Make reviews editable", None))
        self.label_Save.setText(QCoreApplication.translate("Dialog", u"Save", None))
        self.pushButton_Save.setText(QCoreApplication.translate("Dialog", u"Save", None))
        self.pushButton_Cancel.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
    # retranslateUi

