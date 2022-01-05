from PyQt5.QtWidgets import QDialog
from PyQt5 import uic
import sqlite3


class MyForm(QDialog):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi("addEditCoffeeForm.ui", self)
        self.initUI()
        if args:
            self.edit_coffee(*args)
        self.save_btn.clicked.connect(self.save_coffee)
        self.back_btn.clicked.connect(self.back)

    def initUI(self):
        self.setFixedSize(self.size())
        self.roast_box.addItems(["слабая", "средняя", "сильная"])
        self.type_box.addItems(["молотый", "в зернах"])
        self.con = sqlite3.connect("coffee.db")
        self.cur = self.con.cursor()

    def edit_coffee(self, *args):
        self.name_line.setText(args[0])
        self.taste_line.setText(args[3])
        self.cost_line.setText(args[4])
        self.value_line.setText(args[5])
        self.roast_box.setCurrentText(args[1])
        self.type_box.setCurrentText(args[2])

    def save_coffee(self):
        res = [
            self.name_line.text(), self.roast_box.itemText(self.roast_box.currentIndex()),
            self.type_box.itemText(self.type_box.currentIndex()),
            self.taste_line.text(), self.cost_line.text(), self.value_line.text()
        ]
        flag = self.cur.execute(f"select * from coffee where name == '{res[0]}'").fetchone()
        if flag:
            self.cur.execute(f"update coffee set [roast degree] = '{res[1]}', type = '{res[2]}', " +
                             f"[taste description] = '{res[3]}', cost = {res[4]}," +
                             f" value = {res[5]} where name == '{res[0]}'")
            self.con.commit()
        else:
            self.cur.execute(
                f"insert into coffee values ('{res[0]}', '{res[1]}', '{res[2]}', '{res[3]}', {res[4]}, {res[5]})"
            )
            self.con.commit()
        self.close()

    def back(self):
        self.close()

