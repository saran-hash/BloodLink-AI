import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        self.__db = None
        self.cursor = None
        try:
            self.__db = mysql.connector.connect(
                host=os.getenv('DB_HOST', 'localhost'),
                user=os.getenv('DB_USER', 'root'),
                password=os.getenv('DB_PASSWORD', 'saran@2006'),
                database=os.getenv('DB_NAME', 'blood_bank_system')
            )
            self.cursor = self.__db.cursor(dictionary=True)
            print("\nConnected to database!")
        except mysql.connector.Error as err:
            print(f" DB Connection Error: {err}")

    def commit(self):
        self.__db.commit()

    def close(self):
        self.cursor.close()
        self.__db.close()
        print("Database connection closed.")

    def get_cursor(self):
        if self.cursor:
            return self.cursor
        else:
            raise ConnectionError("Database cursor not initialized.")

    def get_connection(self):
        return self.__db
