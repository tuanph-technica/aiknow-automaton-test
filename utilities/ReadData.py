from utilities import ExcelUtil
from abc import ABC
import random
import ast
import pandas as pd
class ReadData(ABC):
    def __init__(self,data_file_name):
        self.data_file_name = data_file_name
        self.sheet_name = ""
        self.data = []
    def get_data_len(self):
        return len(self.data)
    def get_data_by_index(self,index):
        return self.data[index]
    def write_data_at_index(self,row_index,column_index,data_value):
        ExcelUtil.writeData(self.data_file_name,self.sheet_name, row_index, column_index, data_value)
    def read_data(self):
        pass
class ReadChatData(ReadData):
    def __init__(self,data_file_name):
        super().__init__(data_file_name)
        self.sheet_name = "Testcase_Ver4_22072025"
    def read_data(self):
        df = pd.read_excel(self.data_file_name,engine="openpyxl",header=0)
        return df.to_dict('records')
class ChatResponseData(ReadData):
    def __init__(self,data_file_name):
        super().__init__(data_file_name)
    def read_data(self):
        df = pd.read_excel(self.data_file_name,header=0, engine="openpyxl")
        return df.to_dict('records')
class UserManagementData(ReadData):
    def __init__(self,data_file_name):
        super().__init__(data_file_name)
    def read_data(self,sheet_name=""):
        df = pd.read_excel(self.data_file_name,sheet_name=sheet_name,header=0, engine="openpyxl")
        df = df.fillna('')
        return df.to_dict('records')
















