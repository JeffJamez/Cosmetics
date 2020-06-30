import mysql.connector as mysql


class Connect:
    def connection(self):
        self.con = mysql.connect(host="localhost", user="root",
                                 password="", database="masewa")
        self.db_cur = self.con.cursor()


con = Connect()