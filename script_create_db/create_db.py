import sqlite3
import os


class CreateDb:
    def __init__(self):
        self.path = os.getcwd()
        self.full_path = os.path.join(self.path, 'patterns.sqlite')
        self.create_db()

    def create_db(self):
        if not os.path.exists(self.full_path):
            connect = sqlite3.connect(self.full_path)
            connect.close()
            self.create_table_student()
        else:
            print('----- db exist')

    def create_table_student(self):
        connect = sqlite3.connect(self.full_path)
        cursor = connect.cursor()
        path_to_file = os.path.join(self.path, 'script_create_db/create_student.sql')
        with open(path_to_file, 'r') as f:
            text = f.read()
        cursor.executescript(text)
        cursor.close()
        connect.close()

print(__name__)
if __name__ == "__main__":
    db_my = CreateDb()
