from typing import ContextManager, Text
from PyQt5.QtCore import *
from PyQt5.QtSql import QSql, QSqlDatabase, QSqlTableModel
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from pathlib import Path
from Core import ServerManager  as sm


class MainWindow(QMainWindow):
    """
    Main window of the application. Holds all components used within the app
    """
    def __init__(self):
        super(MainWindow, self).__init__()

        # Configure Window Settings:
        self.setWindowTitle("Valheim Server Management")
        self.resize(800,600)

        # Create window components:
        ## Toolbar:
        toolbar = QToolBar("Server Management Toolbar")
        action_newServer = QAction("New Server", self)
        action_newServer.setStatusTip("Add a server to manage")
        toolbar.addAction(action_newServer)
        ## Content:
        self.content = QWidget(self)
        self.content_layout = QHBoxLayout()
        self.content_layout.addWidget(ServerTableView())
        
        # Connect actions:
        action_newServer.triggered.connect(self.newServerDialog)
        
        # Add components:
        ## Toolbar:
        self.addToolBar(toolbar)
        ## Content:
        self.content.setLayout(self.content_layout)
        self.setCentralWidget(self.content)

    def newServerDialog(self, s):
        """
        Creates a dialog to collect information for a new server
        """
        dlg = NewServerDialog(self)
        dlg.setWindowTitle("New Server")
        dlg.exec_()

class NewServerDialog(QDialog):
    """
    Dialog class for adding a new server
    """
    def __init__(self, parent=None):
        super(QDialog, self).__init__(parent)
        self.setWindowTitle("New Server")

        # Create dialogue components:
        self.form = ServerForm()
        QBtn = QDialogButtonBox.Save | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)

        # Connect buttons: 
        self.buttonBox.accepted.connect(self.accepted)
        self.buttonBox.rejected.connect(self.reject)

        # Set dialog layout:
        self.content_layout = QVBoxLayout()
        self.content_layout.addWidget(self.form)
        self.content_layout.addWidget(self.buttonBox)
        self.setLayout(self.content_layout)

    def accepted(self):
        """
        Calls the forms addServer method and accepts if returns true
        """
        if self.form.addServer():
            self.accept()

class ServerTableView(QTableView):
    """
    Veiw class for reading servers table in the database
    """
    def __init__(self):
        super(QTableView, self).__init__()

        self.setModel(sm.ServerModel())
        self.resizeColumnsToContents()

class ServerForm(QWidget):
    """
    Form class for creating a new server
    """
    def __init__(self):
        super(QWidget, self).__init__()

        self.server_data = dict()

        # Create labels and their inputs:
        self.lname, self.newServer_name = QLabel("Name"), QLineEdit()
        self.lworld,self.newServer_world = QLabel("World"), QLineEdit()
        self.lport, self.newServer_port = QLabel("Port"), QSpinBox()
        self.newServer_port.setRange(2456,9999)
        self.lpassword, self.newServer_password = QLabel("Password"), QLineEdit()
        self.ldir, self.newServer_dir = QLabel("Server Folder Location"), QLineEdit()
        self.lbackups, self.newServer_backups = QLabel("Backups?"), QCheckBox()
        self.lbackups_dir, self.newServer_backups_dir = QLabel("Backups Folder Location"), QLineEdit()
        self.lbackups_purge_age, self.newServer_backups_purge_age = QLabel("Purge Backups older than (days): "), QSpinBox()

        # Create a form layout and add labels and inputs:
        self.vbox = QFormLayout()
        self.vbox.addRow(self.lname, self.newServer_name)
        self.vbox.addRow(self.lworld, self.newServer_world)
        self.vbox.addRow(self.lport, self.newServer_port)
        self.vbox.addRow(self.lpassword, self.newServer_password)
        self.vbox.addRow(self.ldir, self.newServer_dir)
        self.vbox.addRow(self.lbackups, self.newServer_backups)
        self.vbox.addRow(self.lbackups_dir, self.newServer_backups_dir)
        self.vbox.addRow(self.lbackups_purge_age, self.newServer_backups_purge_age)

        # Save user input data as it changes:
        self.newServer_name.textEdited.connect(lambda name: self.collectServerData("name",name))
        self.newServer_world.textEdited.connect(lambda world: self.collectServerData("world",world))
        self.newServer_port.valueChanged.connect(lambda port: self.collectServerData("port", port))
        self.newServer_password.textEdited.connect(lambda password: self.collectServerData("password", password))
        self.newServer_dir.textEdited.connect(lambda dir: self.collectServerData("dir", dir))
        self.newServer_backups.stateChanged.connect(lambda backups: self.collectServerData("backups", backups))
        self.newServer_backups_dir.textEdited.connect(lambda backups_dir: self.collectServerData("backups_dir", backups_dir))
        self.newServer_backups_purge_age.valueChanged.connect(lambda purge_age: self.collectServerData("backups_purge_age", purge_age))

        # Set layout of the form:
        self.setLayout(self.vbox)

    def collectServerData(self, property, data):
        """
        Collects data from input fields to one data object
        """
        self.server_data[property] = data

    def addServer(self):
        """
        Leverages ServerManager to add a new server. Returns True if successful
        """
        # TODO: Validate form before submission
        # Try using ServerManager to add the server: 
        if not sm.addServer(self.server_data):
           return False
        # If successful, refresh data:
        sm.ServerModel().select()
        return True