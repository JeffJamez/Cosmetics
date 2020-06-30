# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'users.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(377, 356)
        Form.setMinimumSize(QtCore.QSize(377, 356))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/gallery/users.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.users_table = QtWidgets.QTableWidget(Form)
        self.users_table.setObjectName("users_table")
        self.users_table.setColumnCount(3)
        self.users_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.users_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.users_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.users_table.setHorizontalHeaderItem(2, item)
        self.gridLayout.addWidget(self.users_table, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Existing Users"))
        item = self.users_table.horizontalHeaderItem(0)
        item.setText(_translate("Form", "User\'s Name"))
        item = self.users_table.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Email"))
        item = self.users_table.horizontalHeaderItem(2)
        item.setText(_translate("Form", "Date Joined"))
import icons_rc
