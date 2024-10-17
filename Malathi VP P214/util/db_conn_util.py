import pyodbc
from util.db_property_util import DBPropertyUtil

class DBConnUtil:
    @staticmethod
    def get_db_connection():
        connection_string = DBPropertyUtil.get_connection_string()
        try:
            connection = pyodbc.connect(connection_string)
            return connection
        except Exception as e:
            print(f"Connection error: {e}")
            return None
