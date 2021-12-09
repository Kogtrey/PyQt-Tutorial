CREATE TABLE IF NOT EXISTS Servers (
    ID INT PRIMARY KEY,
    Name TEXT,
    World TEXT,
    Port INT,
    Password TEXT,
    dir TEXT,
    Backups INT,
    BackupsDir TEXT,
    BackupsPurgeAge INT
)