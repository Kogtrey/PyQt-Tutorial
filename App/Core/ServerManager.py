from functools import singledispatch
import sys
from PyQt5 import QtWidgets

from PyQt5.QtCore import *
from PyQt5.QtSql import *
from PyQt5.QtWidgets import *

from Util.Decorators import *

@singleton
class ServerModel(QSqlTableModel):
    def __init__(self):
        super(QSqlTableModel, self).__init__()

        self.setTable("servers")
        self.setHeaderData(0, Qt.Horizontal, "ID")
        self.setHeaderData(1, Qt.Horizontal, "Name")
        self.setHeaderData(2, Qt.Horizontal, "World")
        self.setHeaderData(3, Qt.Horizontal, "Port")
        self.setHeaderData(4, Qt.Horizontal, "Password")
        self.setHeaderData(5, Qt.Horizontal, "Server File Location")
        self.select()


def addServer(data) -> bool:
    insertServerQuery = QSqlQuery()
    insertServerQuery.prepare(
        """
        INSERT INTO servers (
            name,
            world,
            port,
            password,
            dir,
            backups,
            backups_dir,
            backups_purge_age
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
    )
    insertServerQuery.addBindValue(data["name"])
    insertServerQuery.addBindValue(data["world"])
    insertServerQuery.addBindValue(data["port"])
    insertServerQuery.addBindValue(data["password"])
    insertServerQuery.addBindValue(data["dir"])
    # 0 = False, 2 = True
    insertServerQuery.addBindValue(data["backups"])
    insertServerQuery.addBindValue(data["backups_dir"])
    insertServerQuery.addBindValue(data["backups_purge_age"])

    if not insertServerQuery.exec_():
        QMessageBox.critical(
            None,
            "Valheim Server Manager - Error!",
            f"Database Error: {insertServerQuery.lastError().databaseText()}"
        )
        return False
    return True