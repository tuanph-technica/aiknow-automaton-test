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
        df = pd.read_excel(self.data_file_name,engine="openpyxl")
        df = df.iloc[:,4:8]
        df.columns = ['question','question_vi','expected_context','expected_result']
        df['model'] = ""
        df['actual_answer'] = ""
        df['test_result'] = ""
        df['screen_shot'] = ""
        return df.to_dict('records')
class ChatResponseData(ReadData):
    def __init__(self,data_file_name):
        super().__init__(data_file_name)
    def read_data(self):
        df = pd.read_excel(self.data_file_name, engine="openpyxl")
        df = df.iloc[:, [1,4,6,7]]
        df.columns = ["file_name",'question', 'expected_context', 'expected_result']

        df['file_name'] = df['file_name'].str.split('https').str[0]
        df = df.dropna(subset=['file_name'])
        return df.to_dict('records')
class UserManagementData(ReadData):
    def __init__(self,data_file_name):
        super().__init__(data_file_name)
    def read_data(self,sheet_name=""):
        df = pd.read_excel(self.data_file_name,sheet_name=sheet_name,header=0, engine="openpyxl")
        return df.to_dict('records')
















