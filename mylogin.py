# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_login_win(object):
    def setupUi(self, login_win):
        login_win.setObjectName("login_win")
        login_win.setWindowModality(QtCore.Qt.ApplicationModal)
        login_win.resize(409, 271)
        login_win.setMinimumSize(QtCore.QSize(409, 271))
        login_win.setMaximumSize(QtCore.QSize(409, 271))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/gallery/lock.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        login_win.setWindowIcon(icon)
        login_win.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.inc_psd_lbl = QtWidgets.QLabel(login_win)
        self.inc_psd_lbl.setGeometry(QtCore.QRect(190, 190, 221, 21))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.inc_psd_lbl.setFont(font)
        self.inc_psd_lbl.setStyleSheet("color: rgb(255, 0, 0);")
        self.inc_psd_lbl.setText("")
        self.inc_psd_lbl.setObjectName("inc_psd_lbl")
        self.username_login = QtWidgets.QLineEdit(login_win)
        self.username_login.setGeometry(QtCore.QRect(220, 100, 171, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.username_login.setFont(font)
        self.username_login.setStyleSheet("border: none;")
        self.username_login.setObjectName("username_login")
        self.psd_login = QtWidgets.QLineEdit(login_win)
        self.psd_login.setGeometry(QtCore.QRect(220, 150, 171, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.psd_login.setFont(font)
        self.psd_login.setStyleSheet("border: none")
        self.psd_login.setEchoMode(QtWidgets.QLineEdit.Password)
        self.psd_login.setObjectName("psd_login")
        self.login_btn = QtWidgets.QPushButton(login_win)
        self.login_btn.setGeometry(QtCore.QRect(320, 230, 81, 31))
        self.login_btn.setStyleSheet("background-color: rgb(0, 170, 0);")
        self.login_btn.setObjectName("login_btn")
        self.label = QtWidgets.QLabel(login_win)
        self.label.setGeometry(QtCore.QRect(10, 30, 201, 221))
        self.label.setStyleSheet("image: url(:/gallery/face.png);")
        self.label.setText("")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(login_win)
        self.label_2.setGeometry(QtCore.QRect(230, 0, 151, 91))
        self.label_2.setStyleSheet("image: url(:/gallery/masewa.jpg);")
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.cancel_log = QtWidgets.QPushButton(login_win)
        self.cancel_log.setGeometry(QtCore.QRect(210, 230, 81, 31))
        self.cancel_log.setStyleSheet("background-color: rgb(255, 0, 0);")
        self.cancel_log.setObjectName("cancel_log")
        self.username_login.raise_()
        self.psd_login.raise_()
        self.login_btn.raise_()
        self.label.raise_()
        self.label_2.raise_()
        self.cancel_log.raise_()
        self.inc_psd_lbl.raise_()

        self.retranslateUi(login_win)
        self.cancel_log.clicked.connect(login_win.close)
        QtCore.QMetaObject.connectSlotsByName(login_win)

    def retranslateUi(self, login_win):
        _translate = QtCore.QCoreApplication.translate
        login_win.setWindowTitle(_translate("login_win", "Login"))
        self.username_login.setPlaceholderText(_translate("login_win", "Username"))
        self.psd_login.setPlaceholderText(_translate("login_win", "Password"))
        self.login_btn.setText(_translate("login_win", "Login"))
        self.cancel_log.setText(_translate("login_win", "Cancel"))
import icons_rc
