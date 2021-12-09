import sys

from PyQt5.QtCore import *
from PyQt5.QtSql import *
from PyQt5.QtWidgets import *

class Contacts(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("QTableView Example")
        self.resize(415, 200)

        self.model = QSqlTableModel(self)
        self.model.setTable("contacts")
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.setHeaderData(0, Qt.Horizontal, "ID")
        self.model.setHeaderData(1, Qt.Horizontal, "Name")
        self.model.setHeaderData(2, Qt.Horizontal, "Job")
        self.model.setHeaderData(3, Qt.Horizontal, "Email")
        self.model.select()

        self.view = QTableView()
        self.view.setModel(self.model)
        self.view.resizeColumnsToContents()
        self.setCentralWidget(self.view)


def createConnection():
    con = QSqlDatabase.addDatabase("QSQLITE")
    con.setDatabaseName("contacts.db")
    if not con.open():
        QMessageBox.critical(
            None,
            "QTableView Example - Error!",
            f"Database Error: {con.lastError().databaseText()}"
        )
        return False
    return True

app = QApplication(sys.argv)
if not createConnection():
    sys.exit(1)

win = Contacts()
win.show()
sys.exit(app.exec_())