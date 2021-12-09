from PyQt5.QtCore import *
from PyQt5.QtSql import QSql, QSqlDatabase, QSqlTableModel
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from pathlib import Path


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Valheim Server Management")
        self.resize(800,600)

class ServerTableView(QTableView):

    def __init__(self):
        super(QTableView, self).__init__()

        self.model = QSqlTableModel(self)
        self.model.setTable("servers")
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.setHeaderData(0, Qt.Horizontal, "ID")
        self.model.setHeaderData(1, Qt.Horizontal, "Name")
        self.model.setHeaderData(2, Qt.Horizontal, "World")
        self.model.setHeaderData(3, Qt.Horizontal, "Port")
        self.model.setHeaderData(4, Qt.Horizontal, "Password")
        self.model.setHeaderData(5, Qt.Horizontal, "Server File Location")

        self.model.select()

        self.setModel(self.model)
        self.resizeColumnsToContents()