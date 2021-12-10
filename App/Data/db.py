import sys
import os

from pathlib import Path
from PyQt5.QtSql import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtSql import *

# Initializations

db_location = Path('App\\Data\\ValheimServers.db').resolve()
print(db_location.is_file())


# Check if the database file exists
def exists() -> bool:
    return db_location.is_file()

# Create a conneciton to the database
def createConnection() -> bool:

    print("Checking if database exists")
    if not exists():
        QMessageBox.critical(
            None,
            "QTableView Example - Error!",
            f"Database Error: {db_location} not found"
        )
        return False

    print("Opening connection to database")
    con = QSqlDatabase.addDatabase("QSQLITE")
    con.setDatabaseName(str(db_location))

    if not con.open(): 
        QMessageBox.critical(
            None,
            "Valheim Server Manager - Error!",
            f"Database Error: {con.lastError().databaseText()}"
        )
        return False

    print("Conneciton success")
    return True

# Initialize database
def init_db() -> bool:
    print("Creating temporary initializer connection")
    temp_con = QSqlDatabase.addDatabase("QSQLITE", connectionName="initializer")
    temp_con.setDatabaseName(str(db_location))

    print(f"Attempting to open {temp_con.connectionName()} connection ")
    if not temp_con.open(): 
        QMessageBox.critical(
            None,
            "Valheim Server Manager - Error!",
            f"Database Error: {temp_con.lastError().databaseText()}"
        )
        return False
    
    createTableQuery = QSqlQuery(temp_con)
    
    createTableQuery.prepare(
        """
        CREATE TABLE servers (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            name VARCHAR(40) NOT NULL,
            world VARCHAR(40) UNIQUE NOT NULL,
            port INTEGER UNIQE NOT NULL,
            password VARCHAR(40) NOT NULL,
            dir VARCHAR(40) UNIQUE NOT NULL,
            backups INTEGER,
            backups_dir VARCHAR(40),
            backups_purge_age INTEGER
        )
        """
    )

    print("Executing table creation")
    if not createTableQuery.exec_():
        temp_con.close()
        QMessageBox.critical(
            None,
            "Valheim Server Manager - Error!",
            f"Database Error: {createTableQuery.lastError().databaseText()}"
        )
        return False
    print(f"Closing {temp_con.connectionName()} connection")
    temp_con.close()
    return True
