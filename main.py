import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem
from PyQt5.QtCore import Qt
from PyQt5 import uic
import sqlite3


def log_uncought_exeptions(ex_cls, ex, tb):
    text = '{}: {}:\n'.format(ex_cls._name_, ex)
    import traceback
    text += "".join(traceback.format_tb(tb))

    print(text)
    QMessageBox.critical(None, 'Error', text)
    quit()


sys.excepthook = log_uncought_exeptions


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.con = sqlite3.connect("coffee.db")
        self.cur = self.con.cursor()
        self.initUI()

    def initUI(self):
        self.setFixedSize(self.size())
        res = self.cur.execute("select * from coffee").fetchall()
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setRowCount(len(res))
        self.tableWidget.setHorizontalHeaderLabels(
            ["Название сорта", "Степень обжарки", "Тип", "Описание вкуса", "Цена", "Объем упаковки"]
        )
        for i in range(len(res)):
            self.tableWidget.horizontalHeaderItem(i).setTextAlignment(Qt.AlignHCenter)
            for j in range(len(res[i])):
                item = QTableWidgetItem(str(res[i][j]), Qt.ItemIsEnabled)
                item.setTextAlignment(Qt.AlignHCenter)
                self.tableWidget.setItem(i, j, item)
        self.tableWidget.resizeColumnsToContents()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())