from typing import ContextManager, Text
from PyQt5.QtCore import *
from PyQt5.QtSql import QSql, QSqlDatabase, QSqlTableModel
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from pathlib import Path
from Core.ServerManager import *

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Valheim Server Management")
        self.resize(800,600)

        self.content = QWidget(self)
        self.content_layout = QHBoxLayout()
        self.content_layout.addWidget(ServerTableView())
        self.content_layout.addWidget(NewServerForm())

        self.content.setLayout(self.content_layout)

        self.setCentralWidget(self.content)


class ServerTableView(QTableView):

    def __init__(self):
        super(QTableView, self).__init__()

        self.setModel(ServerModel())
        self.resizeColumnsToContents()

class NewServerForm(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()

        self.server_data = dict()

        self.lname, self.newServer_name = QLabel("Name"), QLineEdit()
        self.lworld,self.newServer_world = QLabel("World"), QLineEdit()

        self.lport, self.newServer_port = QLabel("Port"), QSpinBox()
        self.newServer_port.setRange(2456,9999)

        self.lpassword, self.newServer_password = QLabel("Password"), QLineEdit()
        self.ldir, self.newServer_dir = QLabel("Server Folder Location"), QLineEdit()
        self.lbackups, self.newServer_backups = QLabel("Backups?"), QCheckBox()
        self.lbackups_dir, self.newServer_backups_dir = QLabel("Backups Folder Location"), QLineEdit()
        self.lbackups_purge_age, self.newServer_backups_purge_age = QLabel("Purge Backups older than (days): "), QSpinBox()

        self.vbox = QFormLayout()
        self.vbox.addRow(self.lname, self.newServer_name)
        self.vbox.addRow(self.lworld, self.newServer_world)
        self.vbox.addRow(self.lport, self.newServer_port)
        self.vbox.addRow(self.lpassword, self.newServer_password)
        self.vbox.addRow(self.ldir, self.newServer_dir)
        self.vbox.addRow(self.lbackups, self.newServer_backups)
        self.vbox.addRow(self.lbackups_dir, self.newServer_backups_dir)
        self.vbox.addRow(self.lbackups_purge_age, self.newServer_backups_purge_age)


        self.newServer_name.textEdited.connect(lambda name: self.collectServerData("name",name))
        self.newServer_world.textEdited.connect(lambda world: self.collectServerData("world",world))
        self.newServer_port.valueChanged.connect(lambda port: self.collectServerData("port", port))
        self.newServer_password.textEdited.connect(lambda password: self.collectServerData("password", password))
        self.newServer_dir.textEdited.connect(lambda dir: self.collectServerData("dir", dir))
        self.newServer_backups.stateChanged.connect(lambda backups: self.collectServerData("backups", backups))
        self.newServer_backups_dir.textEdited.connect(lambda backups_dir: self.collectServerData("backups_dir", backups_dir))
        self.newServer_backups_purge_age.valueChanged.connect(lambda purge_age: self.collectServerData("backups_purge_age", purge_age))

        
        self.addServerButton = QPushButton("Submit")
        self.addServerButton.clicked.connect(self.addServer)

        self.vbox.addRow(self.addServerButton)

        self.setLayout(self.vbox)

    def collectServerData(self, property, data):
        self.server_data[property] = data
        print(f"{property}: {data}")

    def addServer(self):
        # TODO: Validate form before submission
        addServer(self.server_data)
        ServerModel().select()
        print(self.server_data)