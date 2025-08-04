HOST = '10.1.40.44'
PORT = 3309
USER_NAME = 'bellapp'
PASS_WORD = 'Bell@123'
DATABASE = "knowledge_v2"
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





class Kcs_Category(MySQLData):
    SELECT_CATEGORY_ACTIVE_SQL = "SELECT `name`, name_en , is_active , `description` from kcs_categories where is_active = 1;"
    SELECT_CATEGORY_INACTIVE_SQL = "SELECT `name`, name_en , is_active , `description` from kcs_categories where is_active = 0;"
    SELECT_ALL_CATEGORY_SQL = "SELECT `name`, name_en , is_active , `description` from kcs_categories;"
    def __init__(self):
        super().__init__()
    def get_category_by_jp_title(self,category_jp_title):
        str_query = "SELECT id from kcs_categories WHERE `name` = '" + category_jp_title + "'"
        results = self.execute_select_query(str_query)
        return results
    def get_category_by_en_title(self,category_en_title):
        str_query = "SELECT id from kcs_categories WHERE name_en = '" + category_en_title + "'"
        results = self.execute_select_query(str_query)
        return results
    def get_category_by_jp_en_title(self,category_jp_title,category_en_title):
        str_query = "SELECT id from kcs_categories WHERE `name` = '" + category_jp_title + "' AND name_en = '" + category_en_title + "'"
        results = self.execute_select_query(str_query)
        return results
    def insert_new_category(self,category_jp,category_en,description):
        str_query = "INSERT INTO kcs_categories (`name`,name_en,description) VALUES ('"
        str_query = str_query + category_jp + "','" + category_en + "','" + description + "');"
        self.execute_insert_query(str_query)


    def select_active_categories(self):
        results = self.execute_select_query(self.SELECT_CATEGORY_ACTIVE_SQL)
        return results
    def select_inactive_categories(self):
        results = self.execute_select_query(self.SELECT_CATEGORY_INACTIVE_SQL)
        return results
    def select_all_categories(self):
        results = self.execute_select_query(self.SELECT_ALL_CATEGORY_SQL)
        return results
    def delete_jp_category_title(self,category_jp_title):
        id = self.get_category_by_jp_title(category_jp_title)
        query_delete = "DELETE FROM kcs_categories WHERE id = " + str(id[0][0])
        self.execute_delete_query(query_delete)
    def delete_en_category_title(self,category_en_title):
        id = self.get_category_by_en_title(category_en_title)
        query_delete = "DELETE FROM kcs_categories WHERE id = " + str(id[0][0])
        self.execute_delete_query(query_delete)
    def delete_category_by_jp_en_title(self,jp_title,en_title):
        id = self.get_category_by_jp_en_title(jp_title,en_title)
        query_delete = "DELETE FROM kcs_categories WHERE id = " + str(id[0][0])
        self.execute_delete_query(query_delete)
    def select_top_categories(self,n_top = 10):
        query_select = "SELECT `name` FROM kcs_categories ORDER BY created_at DESC LIMIT " + str(n_top) +" WHERE is;"
        results = self.execute_select_query(query_select)
        return results





