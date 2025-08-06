HOST = '10.1.40.7'
PORT = 3309
USER_NAME = 'aiknow'
PASS_WORD = 'aiknow@123'
DATABASE = "aiknow_v2"
import mysql.connector
from abc import ABC
class MySQLData(ABC):
    def __init__(self):
        pass

    def execute_select_query(self,query):
        connection = mysql.connector.connect(user = USER_NAME,password=PASS_WORD,host=HOST,port=PORT,database=DATABASE)
        cursor = connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        connection.close()
        return results
    def execute_delete_query(self,query):
        connection = mysql.connector.connect(user=USER_NAME, password=PASS_WORD, host=HOST, port=PORT,
                                             database=DATABASE)
        cursor = connection.cursor()
        cursor.execute("SET SQL_SAFE_UPDATES = 0")

        cursor.execute(query)
        connection.commit()
        cursor.execute("SET SQL_SAFE_UPDATES = 1")
        cursor.close()
        connection.close()
    def execute_insert_query(self,query):
        connection = mysql.connector.connect(user=USER_NAME, password=PASS_WORD, host=HOST, port=PORT,
                                             database=DATABASE)
        cursor = connection.cursor()
        cursor.execute("SET SQL_SAFE_UPDATES = 0")

        cursor.execute(query)
        connection.commit()
        cursor.execute("SET SQL_SAFE_UPDATES = 1")
        cursor.close()
        connection.close()
class DataDocuments(MySQLData):
    def __init__(self):
        super().__init__()
    def get_document_extracted(self):
        str_query = "SELECT original_name FROM documents WHERE extract_error_code = 0"
        return self.execute_select_query(str_query)
    def check_document_exist(self,document_file_name):
        str_query = "SELECT original_name FROM documents WHERE original_name LIKE '%" + document_file_name + "%'"
        ret = self.execute_select_query(str_query)
        if len(ret) > 0:
            return True
        else:
            return False







