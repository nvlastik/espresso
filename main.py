from PyQt5 import uic  # Импортируем uic
import sqlite3
from PyQt5.Qt import *



class Table(QMainWindow):
    def __init__(self,):
        super().__init__()
        uic.loadUi('main.ui', self)  # Загружаем дизайн
        self.model = QStandardItemModel()
        self.table.setModel(self.model)
        self.con = sqlite3.connect("coffee.sqlite")  # БД
        self.cur = self.con.cursor()
        self.load_data()

    def closeEvent(self, event):
        self.con.close()  # закрытие БД при завершении работы

    def load_data(self):
        ob = {o[0]: o[1] for o in self.cur.execute("SELECT * FROM roasting").fetchall()}  # степени обжарки
        zap = self.cur.execute("SELECT * FROM coffee").fetchall()
        vsv = [(i[0], i[1], ob[i[2]], "В зернах" if i[3] else "Молотый", i[4], f"{i[5]} г.", f"{i[6]} руб.") for i in zap]  # подготовка к выводу
        self.model.setHorizontalHeaderLabels(["id", "Название", "Степень обжарки", "Вид", "Описание", "Вес", "Цена"])
        for i in range(len(vsv)):  # вывод данных
            for j in range(len(vsv[i])):
                item = QStandardItem(str(vsv[i][j]))
                self.model.setItem(i, j, item)

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)  # делаем красиво
        self.table.horizontalHeader().setMinimumSectionSize(0)


if __name__ == "__main__":
    app = QApplication([])
    w = Table()
    w.show()
    app.exec_()