from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from database import con
import mainfile as m
from mylogin import Ui_login_win


class Login(QWidget, Ui_login_win):
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
        con.connection()

        self.login_btn.clicked.connect(self.handle_login)

    def handle_login(self):
        username = self.username_login.text()
        password = self.psd_login.text()

        sql = '''SELECT * FROM users WHERE username = %s AND password = %s'''
        con.db_cur.execute(sql, [username, password])

        if con.db_cur.fetchone() is not None:
            self.correct = m.MainApp()
            self.close()
            self.correct.showMaximized()

        else:
            self.inc_psd_lbl.setText('Username or password is incorrect')


