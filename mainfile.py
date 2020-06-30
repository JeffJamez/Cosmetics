from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from datetime import date
import login as log
import sales as s
import users as u
from database import con
from xlrd import *
from xlsxwriter import *
from mymasewa import Ui_MainWindow


class MainApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        con.connection()

        self.MainTab.tabBar().setVisible(False)

        self.open_sales_tab()
        self.show_categories()

        self.handle_buttons()
        self.show_all_products()
        self.show_all_sales()

    def handle_buttons(self):
        # =============  buttons to open tabs ===============
        self.sales_btn.clicked.connect(self.open_sales_tab)
        self.products_btn.clicked.connect(self.open_products_tab)
        self.users_btn.clicked.connect(self.open_users_tab)
        self.suppliers_btn.clicked.connect(self.open_suppliers_tab)

        # =============  sales tab buttons =================
        self.add_sales_btn.clicked.connect(self.open_sales_window)
        self.refresh_btn.clicked.connect(self.show_all_sales)
        self.export_btn.clicked.connect(self.export_sales)

        # =============  products tab buttons ===============
        self.save_prod_btn.clicked.connect(self.add_new_product)
        self.new_categ_btn.clicked.connect(self.add_new_category)
        self.search_prod_btn.clicked.connect(self.search_product)

        self.cancel_prod_btn.clicked.connect(self.cancel_prod_entry)
        self.save_prod_edit_btn.clicked.connect(self.update_product)
        self.delete_prod_btn.clicked.connect(self.delete_product)
        self.categories_btn.clicked.connect(self.activate)

        # ============ Users Tab Buttons ==============
        self.add_user_btn.clicked.connect(self.add_new_user)
        self.cancel_user_btn.clicked.connect(self.cancel_user_entry)
        self.login_edit_btn.clicked.connect(self.log_user)
        self.save_user_edit_btn.clicked.connect(self.edit_user)
        self.cancel_user_edit_btn.clicked.connect(self.cancel_user_edit)
        self.all_users_btn.clicked.connect(self.show_users)

        # ============  supplier tab buttons ============
        self.add_supl_btn.clicked.connect(self.add_spplier)
        self.search_supl_btn.clicked.connect(self.search_supplier)
        self.save_supl_edit_btn.clicked.connect(self.edit_supplier)
        self.delete_supl_btn.clicked.connect(self.delete_supplier)
        self.cancel_supl_btn.clicked.connect(self.cancel_supl_entry)

    # =============  Functions to open tabs ===============
    def open_sales_tab(self):
        self.MainTab.setCurrentIndex(0)

    def open_products_tab(self):
        self.MainTab.setCurrentIndex(1)
        self.products_tab.setCurrentIndex(0)
        self.show_all_sales()


    def open_users_tab(self):
        self.MainTab.setCurrentIndex(2)

    def open_suppliers_tab(self):
        self.MainTab.setCurrentIndex(3)
        self.see_all_suppliers()

# ========= Sales Tab Operations ===========
    def show_all_sales(self):
        con.db_cur.execute('''
                SELECT prod_name, unit_cost, qty_sold, total, date_sold, remaining FROM sales ORDER BY date_sold DESC
                 ''')

        data = con.db_cur.fetchall()
        self.sales_table.setRowCount(0)

        for row, form in enumerate(data):
            self.sales_table.insertRow(row)
            for column, item in enumerate(form):
             self.sales_table.setItem(row, column, QTableWidgetItem(str(item)))

        self.show_all_products()

    def open_sales_window(self):
        self.sales = s.Sales()
        self.sales.show()

    def export_sales(self):
        con.db_cur.execute('''
                     SELECT prod_name, unit_cost, qty_sold, total, date_sold, remaining FROM sales
                           ''')

        data = con.db_cur.fetchall()
        wb = Workbook('C:/Users/user/Desktop/All Sales.xlsx')
        sheet1 = wb.add_worksheet()
        sheet1.write(0, 0, 'Product\'s Name')
        sheet1.write(0, 1, 'Unit Cost')
        sheet1.write(0, 2, 'Quantity Sold')
        sheet1.write(0, 3, 'Total Cost')
        sheet1.write(0, 4, 'Date Sold')
        sheet1.write(0, 5, 'Remaining')

        row_number = 1
        for row in data:
            column_number = 0
            for item in row:
                sheet1.write(row_number, column_number, str(item))
                column_number += 1
            row_number += 1

        wb.close()
        self.statusBar().showMessage('File Has Been Exported To Desktop')

# ========= Products Tab Operations ===========
    def show_all_products(self):
        con.db_cur.execute('''
                       SELECT prod_name, quantity, price, category, date, supplier_name FROM products
                        ''')

        data = con.db_cur.fetchall()
        self.products_table.setRowCount(0)

        for row, form in enumerate(data):
            self.products_table.insertRow(row)
            for column, item in enumerate(form):
                self.products_table.setItem(row, column, QTableWidgetItem(str(item)))

    def add_new_product(self):
        name = self.p_name_entry.text()
        category = self.categ_combo.currentText()
        price = self.p_price_entry.text()
        qty = self.p_qnty_entry.text()
        supl_name = self.p_supl_entry.text()
        today = date.today()

        if name != '' and qty != '' and price != '':
            try:
                qty = int(qty)
                price = int(price)

            except:
                QMessageBox.information(self, 'Invalid Entry', 'Price and Quantity must be Number',
                                    QMessageBox.Ok)

            else:
                sql = '''SELECT * FROM products WHERE prod_name=%s'''
                con.db_cur.execute(sql, [name])

                if con.db_cur.fetchone() is None:
                    con.db_cur.execute('''
                                INSERT INTO products(prod_name, quantity, price, date, category, supplier_name)
                                values (%s, %s, %s, %s, %s, %s)
                                ''', (name, qty, price, today, category, supl_name))
                    con.db_cur.execute("commit")
                    self.statusBar().showMessage('New Product Added')

                    self.p_name_entry.setText('')
                    self.categ_combo.setCurrentIndex(0)
                    self.p_supl_entry.setText('')
                    self.p_price_entry.setText('')
                    self.p_qnty_entry.setText('')

                    self.show_all_products()
                else:
                    QMessageBox.information(self, 'Already Exists', 'A product with that name already exixts',
                                            QMessageBox.Ok)

        else:
            QMessageBox.information(self, 'Empty Field', 'Please fill in all the fields',
                                    QMessageBox.Ok)

    def cancel_prod_entry(self):
        self.p_name_entry.setText('')
        self.categ_combo.setCurrentIndex(0)
        self.p_price_entry.setText('')
        self.p_qnty_entry.setText('')
        self.p_supl_entry.setText('')

    def show_categories(self):
        con.db_cur.execute(
            "SELECT category_name FROM categories")
        data = con.db_cur.fetchall()

        self.categ_combo.clear()
        for category in data:
            self.categ_combo.addItem(category[0])
            self.categ_combo2.addItem(category[0])

    def add_new_category(self):
        new_categ = self.add_categ_entry.text()
        con.db_cur.execute(
            "insert into categories(category_name) values( %s)", (new_categ,))
        con.db_cur.execute("commit")
        self.add_categ_entry.setText('')

        self.new_categ_btn.setEnabled(False)
        self.add_categ_entry.setEnabled(False)
        self.show_categories()

    def activate(self):
        self.new_categ_btn.setEnabled(True)
        self.add_categ_entry.setEnabled(True)

    def search_product(self):
        name = self.search_prod_entry.text()

        sql = '''SELECT * FROM products WHERE prod_name =%s'''
        con.db_cur.execute(sql, [name])
        data = con.db_cur.fetchone()

        if data is not None:
            self.p_name_entry_2.setText(data[1])
            self.p_qnty_entry2.setText(str(data[2]))
            self.p_price_entry_2.setText(str(data[3]))
            self.p_supl_entry2.setText(data[5])
            self.categ_combo2.setCurrentText(data[6])

        else:
            QMessageBox.critical(self, 'Not Found', 'There is no product with this name',
                                    QMessageBox.Ok)

    def update_product(self):
        name = self.search_prod_entry.text()

        p_name = self.p_name_entry_2.text()
        price = self.p_price_entry_2.text()
        qnty = self.p_qnty_entry2.text()
        supl = self.p_supl_entry2.text()
        categ = self.categ_combo2.currentText()

        try:
            qnty = int(qnty)
            price = int(price)

        except:
            QMessageBox.information(self, 'Invalid Entry', 'Price and quantity must be numbers',
                                    QMessageBox.Ok)

        else:
            con.db_cur.execute('''
                   UPDATE products SET prod_name=%s, quantity=%s, price=%s, supplier_name=%s, category=%s WHERE prod_name=%s
                   ''', (p_name, qnty, price, supl, categ, name))
            con.db_cur.execute('commit')
            self.statusBar().showMessage('Product Updated')

            self.search_prod_entry.setText('')
            self.p_name_entry_2.setText('')
            self.p_price_entry_2.setText('')
            self.p_qnty_entry2.setText('')
            self.p_supl_entry2.setText('')
            self.categ_combo2.setCurrentIndex(0)

            self.show_all_products()

    def delete_product(self):
        name = self.search_prod_entry.text()

        if name == '':
            QMessageBox.information(self, 'Delete Product', 'No Product Selected',
                                    QMessageBox.Ok)
        else:

            warning = QMessageBox.warning(self, 'Delete Product', 'Are you sure you want to delete this Product?',
                                      QMessageBox.Yes | QMessageBox.No)

            if warning == QMessageBox.Yes:
                sql = '''DELETE FROM products WHERE prod_name = %s'''
                con.db_cur.execute(sql, [name])
                con.db_cur.execute('commit')
                self.statusBar().showMessage('Product Deleted')

                self.search_prod_entry.setText('')
                self.p_name_entry_2.setText('')
                self.p_price_entry_2.setText('')
                self.p_qnty_entry2.setText('')
                self.p_supl_entry2.setText('')
                self.categ_combo2.setCurrentIndex(0)

                self.show_all_products()

# ========== Users Tab Operations =========
    def show_users(self):
        self.see = u.Users()
        self.see.show()

    def add_new_user(self):
        username = self.add_uname.text()
        email = self.add_email.text()
        password = self.add_psd.text()
        password2 = self.add_psd2.text()
        today = date.today()

        sql = '''SELECT * FROM users WHERE username = %s'''
        con.db_cur.execute(sql, [username])

        if con.db_cur.fetchone() is not None:
            QMessageBox.critical(self, 'Choose another name', 'That username has already been taken',
                                    QMessageBox.Ok)

        elif username == '' or email == '':
            QMessageBox.information(self, 'Empty Fields', 'Please fill in all the fields',
                                 QMessageBox.Ok)

        elif '@' and '.com' not in email:
            QMessageBox.critical(self, 'Invalid Entry', 'Your e-mail format is invalid',
                                 QMessageBox.Ok)

        elif len(password) < 6:
            QMessageBox.critical(self, 'Short Password', 'Your password must be at least 6 Characters',
                                    QMessageBox.Ok)

        elif password == password2:
            con.db_cur.execute('''
                    INSERT INTO users (username, email, password, date_joined)
                    VALUES (%s, %s, %s, %s)
                    ''', (username, email, password, today))
            con.db_cur.execute('commit')
            self.statusBar().showMessage('New User Added')

            self.add_uname.setText('')
            self.add_email.setText('')
            self.add_psd.setText('')
            self.add_psd2.setText('')

        else:
            self.inv_psd_lbl.setText("Passwords Don't Match")

    def cancel_user_entry(self):
        self.add_uname.setText('')
        self.add_email.setText('')
        self.add_psd.setText('')
        self.add_psd2.setText('')

    def log_user(self):
        username = self.uname_entry.text()
        password = self.psd_entry.text()

        sql = '''SELECT * FROM users WHERE username = %s and password = %s'''
        con.db_cur.execute(sql, [username, password])
        data = con.db_cur.fetchone()

        if data is not None:
            self.edit_user_box.setEnabled(True)

            self.edit_uname.setText(data[1])
            self.edit_email.setText(data[2])
            self.edit_psd.setText(data[3])

        else:
            QMessageBox.critical(self, 'Wrong', 'Your username or password is wrong',
                                 QMessageBox.Ok)

    def edit_user(self):
        original_name = self.uname_entry.text()
        username = self.edit_uname.text()
        email = self.edit_email.text()
        password = self.edit_psd.text()
        password2 = self.edit_psd2.text()

        if username == '' or email == '':
            QMessageBox.information(self, 'Invalid Entry', 'Make sure you fill in all the fields',
                                 QMessageBox.Ok)

        elif len(password) < 6:
            QMessageBox.critical(self, 'Short Password', 'Your password must be at least 6 Characters',
                                 QMessageBox.Ok)

        elif password == password2:
            con.db_cur.execute(''' 
                        UPDATE users SET username = %s, email = %s, password = %s WHERE username = %s
                    ''', (username, email, password, original_name))
            con.db_cur.execute('commit')

            self.edit_uname.setText('')
            self.edit_email.setText('')
            self.edit_psd.setText('')
            self.edit_psd2.setText('')

            self.uname_entry.setText('')
            self.psd_entry.setText('')
            self.edit_user_box.setEnabled(False)

            self.statusBar().showMessage('User Details Updated')

        else:
            QMessageBox.critical(self, 'Incorrect', 'Your password Don\'t match',
                                 QMessageBox.Ok)

    def cancel_user_edit(self):
        self.edit_uname.setText('')
        self.edit_email.setText('')
        self.edit_psd.setText('')
        self.edit_psd2.setText('')

        self.uname_entry.setText('')
        self.psd_entry.setText('')
        self.edit_user_box.setEnabled(False)

# =========== suppliers tab operations ================
    def see_all_suppliers(self):
        con.db_cur.execute('''
           SELECT supl_name, supl_email, supl_cont FROM suppliers
            ''')

        data = con.db_cur.fetchall()
        self.supl_table.setRowCount(0)

        for row, form in enumerate(data):
            self.supl_table.insertRow(row)
            for column, item in enumerate(form):
                self.supl_table.setItem(row, column, QTableWidgetItem(str(item)))

    def add_spplier(self):
        name = self.supl_name_entry.text()
        email = self.supl_email_entry.text()
        cont = self.supl_cont_entry.text()

        sql = '''SELECT supl_name FROM suppliers WHERE supl_name = %s'''
        con.db_cur.execute(sql, [name])

        if con.db_cur.fetchone() is not None:
            QMessageBox.critical(self, 'Choose another name', 'A supplier with that name already exists',
                                 QMessageBox.Ok)

        elif name == '':
            QMessageBox.information(self, 'Empty Field', 'A supplier must have a name',
                                 QMessageBox.Ok)

        elif email != '' and '@' and '.com' not in email:
            QMessageBox.critical(self, 'Invalid', 'Your Email format is invalid',
                                     QMessageBox.Ok)

        elif cont != '' and len(cont) < 10:
            QMessageBox.critical(self, 'Invalid Entry', 'Contact too short',
                                 QMessageBox.Ok)
        else:
            con.db_cur.execute('''
                INSERT INTO  suppliers(supl_name, supl_email, supl_cont) 
                VALUES (%s, %s, %s)''', (name, email, cont))

            con.db_cur.execute('commit')

            self.supl_name_entry.setText('')
            self.supl_email_entry.setText('')
            self.supl_cont_entry.setText('')

            self.see_all_suppliers()
            self.statusBar().showMessage('A new supplier has been added')

    def cancel_supl_entry(self):
        self.supl_name_entry.setText('')
        self.supl_email_entry.setText('')
        self.supl_cont_entry.setText('')

    def search_supplier(self):
        name = self.search_supl.text()

        sql = '''SELECT * FROM suppliers WHERE supl_name =%s'''
        con.db_cur.execute(sql, [name])
        data = con.db_cur.fetchone()

        if data is not None:
            self.save_supl_edit_btn.setEnabled(True)
            self.delete_supl_btn.setEnabled(True)

            self.supl_name_edit.setText(data[1])
            self.supl_email_edit.setText(data[2])
            self.supl_cont_edit.setText(str(data[3]))

        else:
            QMessageBox.critical(self, 'Not Found', 'There is no supplier with this name',
                                    QMessageBox.Ok)

    def edit_supplier(self):
        org_name = self.search_supl.text()
        name = self.supl_name_edit.text()
        email = self.supl_email_edit.text()
        cont = self.supl_cont_edit.text()

        if cont != '' and len(cont) < 10:
            QMessageBox.critical(self, 'Invalid Entry', 'Contact too short',
                                    QMessageBox.Ok)

        elif email != '' and '@' and '.com':
            QMessageBox.critical(self, 'Invalid Entry', 'Your Email format is invalid',
                                 QMessageBox.Ok)

        else:
            con.db_cur.execute('''
                UPDATE suppliers SET supl_name = %s, supl_email = %s, supl_cont=%s WHERE supl_name=%s 
                ''', (name, email, cont, org_name))
            con.db_cur.execute('commit')

            self.supl_name_edit.setText('')
            self.supl_email_edit.setText('')
            self.supl_cont_edit.setText('')
            self.search_supl.setText('')

            self.see_all_suppliers()

            self.save_supl_edit_btn.setEnabled(False)
            self.delete_supl_btn.setEnabled(False)
            self.statusBar().showMessage('Supplier\'s Changes saved')

    def delete_supplier(self):
        name = self.search_supl.text()

        if name == '':
            QMessageBox.information(self, 'Delete Supplier', 'No Supplier Selected',
                                    QMessageBox.Ok)

        else:
            warning = QMessageBox.warning(self, 'Delete Supplier', 'Are you sure you want to delete this Supplier?',
                                          QMessageBox.Yes | QMessageBox.No)

            if warning == QMessageBox.Yes:
                sql = '''DELETE FROM suppliers WHERE supl_name = %s'''
                con.db_cur.execute(sql, [name])
                con.db_cur.execute('commit')
                self.statusBar().showMessage('Supplier Deleted')

                self.search_supl.setText('')
                self.search_supl.setText('')
                self.supl_name_edit.setText('')
                self.supl_email_edit.setText('')
                self.supl_cont_edit.setText('')

                self.save_supl_edit_btn.setEnabled(False)
                self.delete_supl_btn.setEnabled(False)
                self.see_all_suppliers()


def main():
    app = QApplication(sys.argv)
    window = log.Login()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()