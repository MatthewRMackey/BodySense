import sqlite3
import os
import shutil
from datetime import date
from pathlib import Path

TYPE_GLU = "glu"
TYPE_KET = "ket"
TYPE_BP = "bp"
TYPE_WT = "wt"

class EntryDatabase:
    def __init__(self):
        os.makedirs(self.get_path_root()+ "\\Readings", exist_ok=True)
        self.path = self.get_path_root() + "\\Readings\\readings.db"
        self.create_database(self.path)


    # Generates Database
    def create_database(self, db_file):
        """Creates a new SQLite database with a table for entries."""
        conn = sqlite3.connect(db_file)
        c = conn.cursor()

        # Create table (if it doesn't exist)
        c.execute("CREATE TABLE IF NOT EXISTS "+"glucose "+"(id INTEGER PRIMARY KEY AUTOINCREMENT, date DATETIME, morning INTEGER, glucose real)")
        conn.commit()
        c.execute("CREATE TABLE IF NOT EXISTS "+"ketones "+"(id INTEGER PRIMARY KEY AUTOINCREMENT, date DATETIME, morning INTEGER, ketones real)")
        conn.commit()
        c.execute("CREATE TABLE IF NOT EXISTS "+"bloodpressure "+"(id INTEGER PRIMARY KEY AUTOINCREMENT, date DATETIME, morning INTEGER, high real, low real)")
        conn.commit()
        c.execute("CREATE TABLE IF NOT EXISTS "+"weight "+"(id INTEGER PRIMARY KEY AUTOINCREMENT, date DATETIME, morning INTEGER, weight real)")
        conn.commit()

        conn.close()
    

    # Inserts into Database
    def insert_db_entry(self, type, date, morning, value):
        """Inserts a new entry into the database."""
        conn = sqlite3.connect(self.path)
        c = conn.cursor()
        if type == TYPE_GLU:
            create_str = "INSERT INTO "+"glucose "+"(date, morning, glucose) VALUES (?, ?, ?)" 
            c.execute(create_str, (date, morning.get(), value))
        elif type == TYPE_KET:
            create_str = "INSERT INTO "+"ketones "+"(date, morning, ketones) VALUES (?, ?, ?)"
            c.execute(create_str, (date, morning.get(), value))
        elif type == TYPE_BP:
            create_str = "INSERT INTO "+"bloodpressure "+"(date, morning, high, low) VALUES (?, ?, ?, ?)"
            c.execute(create_str, (date, morning.get(), value[0], value[1]))
        elif type == TYPE_WT:
            create_str = "INSERT INTO "+"weight "+"(date, morning, weight) VALUES (?, ?, ?)"
            c.execute(create_str, (date, morning.get(), value))
    
        conn.commit()
        conn.close()


    # Deletes from the Database
    def delete_db_entry(self, type, entry_id):
        """Deletes an entry from the database based on its ID."""
        conn = sqlite3.connect(self.path)
        c = conn.cursor()

        if type == TYPE_GLU:
            create_str = "DELETE FROM "+"glucose "+"WHERE id = ?" 
        elif type == TYPE_KET:
            create_str = "DELETE FROM "+"ketones "+"WHERE id = ?" 
        elif type == TYPE_BP:
            create_str = "DELETE FROM "+"bloodpressure "+"WHERE id = ?" 
        elif type == TYPE_WT:
            create_str = "DELETE FROM "+"weight "+"WHERE id = ?" 

        # Delete entry
        c.execute(create_str, (entry_id,))
        conn.commit()
        conn.close()


    # Get all database entries from both tables
    def get_all_database_entries(self):
        conn = sqlite3.connect(self.path)
        c = conn.cursor()

        tables = []
        c.execute("SELECT * FROM glucose")
        tables.append(c.fetchall())
        c.execute("SELECT * FROM ketones")
        tables.append(c.fetchall())
        c.execute("SELECT * FROM bloodpressure")
        tables.append(c.fetchall())
        c.execute("SELECT * FROM weight")
        tables.append(c.fetchall())

        return (t for t in tables)


    # Backup database keeping the ten most recent backups
    ##TODO Need to fix the ordering of backups to delete the oldest one when there are 10
    def backup_database(self):
        os.makedirs(self.get_path_root()+"\\Backups", exist_ok=True)
        backups = [f for f in Path(self.get_path_root()+"\\Backups").iterdir() if f.is_file()]
        backup_count = len(backups)
        shutil.copy2(self.path, self.get_path_root()+"\\Backups\\backup_"+str(backup_count)+"_On_"+str(date.today())+".db")


    # Determine the root up to the current user's home directory (Windows only)
    def get_path_root(self):
        cwd = os.getcwd()
        slashes = 0
        index = 0
        root_path = ""
        while slashes < 3:
            root_path += cwd[index]
            if cwd[index] == "\\":
                slashes += 1
            index += 1
        return root_path + "BodySense"