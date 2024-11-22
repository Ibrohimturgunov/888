import sqlite3
import pymysql
import os
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QMessageBox

from PyQt5.QtSql import QSqlDatabase, QSqlQueryModel
from PyQt5.QtCore import QAbstractTableModel, Qt


class MyTableModel(QAbstractTableModel):
    def __init__(self, data):
        super(MyTableModel, self).__init__()
        self._data = data

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._data[0]) if self._data else 0

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]

class App(QMainWindow):
    def __init__(self):

        super().__init__()
        uic.loadUi('sql.ui', self)

        self.msg = QMessageBox()
        self.btn_1.clicked.connect(self.ulanish)
        self.qidirish.textChanged.connect(self.textchanged)
        self.btn_2.clicked.connect(self.sorovlar)

    def sorovlar(self):
        conn = sqlite3.connect(self.base_name.text())
        cursor = conn.cursor()
        quary = self.SQL_sorov.text()

        cursor.execute(quary)
        result = cursor.fetchall()
        s=""
        if not result:
            self.tex_out.setText("Hech qanday ma'lumot topilmadi")
        else:
            for row in result:
                s += str(row)+"\n"
            self.tex_out.setText(s)

        conn.commit()

    def textchanged(self):
        jad_name =  self.jadval_name.text()
        s = self.qidirish.text()

        self.conn = sqlite3.connect(self.base_name.text())
        self.cursor = self.conn.cursor()

        quary = ("SELECT * from "+jad_name+
                 " where name LIKE '%"+s+"%' or surname LIKE '%"+s+"%'")

        self.cursor.execute(quary)
        result = self.cursor.fetchall()
        if not result:
            self.tex_out.setText("")
        else:
            for row in result:
                self.tex_out.setText(str(row))

        self.conn.commit()

    def ulanish(self):
        name =  self.ulan_tur.text() #input('Ulanish turini tanlang: masalan(sqlite3, pymysql): ')
        if name == 'sqlite3':
            baza_nomi = self.base_name.text() #input('Bazani nomini kiriting: ')
            if os.path.exists(baza_nomi):
                self.show_message("Baza mavjudligini tekshirish",f" '{baza_nomi}' nomli baza mavjud.")

                try:
                    self.conn = sqlite3.connect(baza_nomi)
                    self.cursor = self.conn.cursor()
                    self.conn.commit()
                    self.show_message("Xabar","Bazaga ulanildi!!!!")

                except sqlite3.SQLITE_ERROR as e:
                    self.show_message("Xatolik",f"Error: {e}")
                finally:
                    self.conn.close()
            else:
                self.show_message("Baza mavjudligini tekshirish", f" '{baza_nomi}' nomli baza mavjud emas!!!.")

        if name == 'pymysql':
            self.showdialog()

    def show_message(self, title, text):
        # Xabar oynasining sarlavhasi va matnini o'rnatish
        self.msg.setWindowTitle(title)
        self.msg.setText(text)

        # Xabar oynasini ko'rsatish
        self.msg.exec_()

    def showdialog(self):
        # Yangi dialog oynasi yaratish
        self.dialog = QDialog(self)
        uic.loadUi('design.ui', self.dialog)  # Dialog interfeysini yuklash
        self.dialog.btn_1.clicked.connect(self.phpMyadmin)

        self.dialog.show()  # Dialogni ko'rsatish

    def phpMyadmin(self):
        try:
            host = self.dialog.host_name.text()
            port = int(self.dialog.port_name.text()) #int(input('Port raqami: masala(3306)'))  # 3306,
            user = self.dialog.user_name.text()  #input('user: masalan(root)')  # "root",
            passwd = self.dialog.password_name.text()  #input('Parol: ')  # "root",
            database = self.dialog.database_name.text() #input('Bazani nomini kiriting: ')  # "alfraganus"
            connection = pymysql.connect(
                host=host,  # "localhost",
                port=port,  # 3306,
                user=user,  # "root",
                passwd=passwd,  # "root",
                database=database  # "alfraganus"
            )
            cursor = connection.cursor()
            jad_nomi = self.dialog.table_name.text()
            cursor.execute(f"SELECT * FROM {jad_nomi}")
            data = cursor.fetchall()

            # Modelni o'rnatish
            self.model = MyTableModel(data)
            self.dialog.tableView.setModel(self.model)

            cursor.close()
            connection.close()

        except Exception as e:
            QMessageBox.critical(self, "Xato", f"Ma'lumotlar bazasiga ulanishda xato: {str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())
