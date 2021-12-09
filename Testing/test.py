import sys

from PyQt5.QtSql import *
from PyQt5.QtWidgets import *

con = QSqlDatabase.addDatabase('QSQLITE')
con.setDatabaseName("contacts.sqlite")

app = QApplication(sys.argv)

if not con.open():
    QMessageBox.critical(
        None,
        "App Name - Error!",
        f"Database Error: {con.lastError().databaseText()}"
    )
    sys.exit(1)

win = QLabel("Connection Successfully opened!")
win.setWindowTitle("App Name")
win.resize(200,100)
win.show()
sys.exit(app.exec_())

