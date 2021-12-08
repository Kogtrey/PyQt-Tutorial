from PyQt5.QtWidgets import QApplication
from MainWindow import MainWindow
import sys

app = QApplication(sys.argv)
window = MainWindow()
sys.exit(app.exec_())
