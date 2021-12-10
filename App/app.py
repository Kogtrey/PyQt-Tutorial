import sys

from PyQt5.QtCore import *
from PyQt5.QtSql import *
from PyQt5.QtWidgets import *

from UI.components import *
from Data import db

app = QApplication(sys.argv)

if not db.exists():
    if not db.init_db():
        sys.exit(1)

if not db.createConnection():
    sys.exit(1)

window = MainWindow()

window.show()

sys.exit(app.exec_())
