# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'finalize.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QDialog, QFrame,
    QLabel, QLineEdit, QListView, QListWidget,
    QListWidgetItem, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(260, 400)
        Dialog.setAcceptDrops(True)
        icon = QIcon()
        icon.addFile(u"../logo.ico", QSize(), QIcon.Mode.Normal, QIcon.State.On)
        Dialog.setWindowIcon(icon)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_Drag_Drop = QLabel(Dialog)
        self.label_Drag_Drop.setObjectName(u"label_Drag_Drop")

        self.verticalLayout.addWidget(self.label_Drag_Drop)

        self.listWidget = QListWidget(Dialog)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setAcceptDrops(True)
        self.listWidget.setLayoutDirection(Qt.LeftToRight)
        self.listWidget.setDragEnabled(True)
        self.listWidget.setDragDropMode(QAbstractItemView.NoDragDrop)
        self.listWidget.setAlternatingRowColors(True)
        self.listWidget.setSelectionMode(QAbstractItemView.MultiSelection)
        self.listWidget.setLayoutMode(QListView.Batched)
        self.listWidget.setSortingEnabled(True)

        self.verticalLayout.addWidget(self.listWidget)

        self.line = QFrame(Dialog)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.label_Output_Folder = QLabel(Dialog)
        self.label_Output_Folder.setObjectName(u"label_Output_Folder")
        self.label_Output_Folder.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout.addWidget(self.label_Output_Folder)

        self.lineEdit_Output_Folder = QLineEdit(Dialog)
        self.lineEdit_Output_Folder.setObjectName(u"lineEdit_Output_Folder")
        self.lineEdit_Output_Folder.setEnabled(True)
        self.lineEdit_Output_Folder.setReadOnly(True)

        self.verticalLayout.addWidget(self.lineEdit_Output_Folder)

        self.pushButton_Select_Output_Folder = QPushButton(Dialog)
        self.pushButton_Select_Output_Folder.setObjectName(u"pushButton_Select_Output_Folder")

        self.verticalLayout.addWidget(self.pushButton_Select_Output_Folder)

        self.line_2 = QFrame(Dialog)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line_2)

        self.pushButton_Send_Data = QPushButton(Dialog)
        self.pushButton_Send_Data.setObjectName(u"pushButton_Send_Data")

        self.verticalLayout.addWidget(self.pushButton_Send_Data)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label_Drag_Drop.setText(QCoreApplication.translate("Dialog", u"Drag & Drop your final sessions below", None))
        self.label_Output_Folder.setText(QCoreApplication.translate("Dialog", u"Output Folder", None))
        self.pushButton_Select_Output_Folder.setText(QCoreApplication.translate("Dialog", u"Select Output Folder", None))
        self.pushButton_Send_Data.setText(QCoreApplication.translate("Dialog", u"Send Data", None))
    # retranslateUi

