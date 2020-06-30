from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from database import con
from myusers import Ui_Form


class Users(QWidget, Ui_Form):
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
        con.connection()
        self.show_users()

    def show_users(self):
        con.db_cur.execute('''SELECT username, email, date_joined FROM users ''')
        data = con.db_cur.fetchall()
        self.users_table.setRowCount(0)

        for row, form in enumerate(data):
            self.users_table.insertRow(row)
            for column, item in enumerate(form):
                self.users_table.setItem(row, column, QTableWidgetItem(str(item)))

