from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from database import con
from datetime import date
from PyQt5.uic import loadUiType
from mysales import Ui_sales_win


class Sales(QWidget, Ui_sales_win):
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
        con.connection()

        self.show_products()
        self.get_unit_price()
        self.get_total()

        self.prod_name_combo.currentTextChanged.connect(self.get_unit_price)
        self.spinBox.valueChanged.connect(self.get_total)
        self.handle_buttons()

    def handle_buttons(self):
        self.send_sales_btn.clicked.connect(self.save_sale)

    def show_products(self):
        con.db_cur.execute(
            "SELECT prod_name FROM products")
        data = con.db_cur.fetchall()

        for product in data:
            self.prod_name_combo.addItem(product[0])

    def get_unit_price(self):
        prod = self.prod_name_combo.currentText()

        sql = '''SELECT * FROM products WHERE prod_name = %s'''
        con.db_cur.execute(sql, [prod])
        data = con.db_cur.fetchone()

        self.unit_price_lbl.setNum(data[3])
        self.get_total()

    def get_total(self):
        one = self.spinBox.value()
        prod = self.prod_name_combo.currentText()

        sql = '''SELECT * FROM products WHERE prod_name = %s'''
        con.db_cur.execute(sql, [prod])
        data = con.db_cur.fetchone()

        total = one * data[3]

        self.total_price_lbl.setNum(total)

    def save_sale(self):
        name = self.prod_name_combo.currentText()
        unit_cost = self.unit_price_lbl.text()
        quantity = self.spinBox.value()
        total = self.total_price_lbl.text()
        today = date.today()

        sql = '''SELECT * FROM products WHERE prod_name = %s'''
        con.db_cur.execute(sql, [name])
        data = con.db_cur.fetchone()

        left = data[2] - quantity

        if left < 1:
            QMessageBox.critical(self, 'Restock', 'This Product is out of stock.',
                                    QMessageBox.Ok)
            self.close()

        elif left < 10:
            QMessageBox.information(self, 'Restock', 'The quantity is below 10. Please Re-stock',
                                    QMessageBox.Ok)

        else:
            sql = '''SELECT * FROM sales WHERE prod_name = %s AND date_sold = %s'''
            con.db_cur.execute(sql, [name, today])

            if con.db_cur.fetchone() is None:
                con.db_cur.execute('''
                    INSERT INTO sales (prod_name, unit_cost, qty_sold, total, date_sold, remaining)
                    VALUES(%s, %s, %s, %s, %s, %s)''', (name, unit_cost, quantity, total, today, left))

                con.db_cur.execute('commit')

                con.db_cur.execute('''
                    UPDATE products SET quantity = %s WHERE prod_name = %s
                    ''', (left, name))

                con.db_cur.execute('commit')

            else:
                sql = '''SELECT * FROM sales WHERE prod_name = %s AND date_sold = %s'''
                con.db_cur.execute(sql, [name, today])
                data = con.db_cur.fetchone()

                rem = data[6] - quantity
                new_total = data[2] * (data[3] + quantity)

                # update the sales table if the product had been sold the same day
                con.db_cur.execute('''
                    UPDATE sales SET qty_sold = %s, total = %s, remaining = %s WHERE prod_name = %s and date_sold = %s
                    ''', (data[3] + quantity, new_total, rem, name, today))

                con.db_cur.execute('commit')

                # update the products table
                con.db_cur.execute('''
                    UPDATE products SET quantity = %s WHERE prod_name = %s
                    ''', (rem, name))

        self.close()





