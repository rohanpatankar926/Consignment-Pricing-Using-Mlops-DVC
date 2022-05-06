from load_data import LoadData
from get_data import GetData
from application_logging.logger import Applogger
import pandas as pd
class Preprocessing:
    def __init__(self):
        self.logger=Applogger()
        self.load_data=LoadData()
        self.get_data=GetData()
             
    def column_imputation(self):
        self.data = self.get_data.get_data("H:/consignment pricing using mlops/params.yaml")
        self.data.columns=self.data.columns.str.lower()
        self.data.columns=self.data.columns.str.replace(" ","_")
        return self.data.columns
    

a=Preprocessing()
a.column_imputation()
