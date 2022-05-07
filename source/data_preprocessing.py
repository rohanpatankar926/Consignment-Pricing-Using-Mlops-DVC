from load_data import LoadData
from get_data import GetData
from application_logging.logger import Applogger
import pandas as pd
import numpy as np
class Preprocessing:
    def __init__(self):
        self.logger=Applogger()
        self.load_data=LoadData()
        self.get_data=GetData()
             
    def column_imputation(self,config_path):
        self.data = self.get_data.get_data("H:/consignment pricing using mlops/params.yaml")
        self.data.columns=self.data.columns.str.lower()
        self.data.columns=self.data.columns.str.replace(" ","_")
        return self.data
    
    # def drop_columns(self,config_path):
    #     self.config=self.get_data.read_params(config_path)
    #     self.data=self.config["raw_data"]["raw"]
    #     self.data=self.data.drop(labels=self.config["columns"]["drop"],axis=1)
    
    def impute_missing(self,config_path):
        self.data=self.column_imputation("H:/consignment pricing using mlops/params.yaml")
        self.data=self.data.drop("dosage",axis=1)
        self.data["shipment_mode"].fillna("Air",inplace=True)
        self.data["line_item_insurance_(usd)"].fillna(47.04,inplace=True)
        return self.data
    
    def client_dates(self,date):
            if date=="Pre-PQ Process":
                return pd.to_datetime('01/06/2009',format="%d/%m/%Y")
            elif date=="Date Not Captured":
                return "Date Not Captured"
            else:
                if len(date)<9:
                    date=pd.to_datetime(date,format="%m/%d/%y")
                    return date
                else:
                    date=date.replace("-","/")
                    date=pd.to_datetime(date,format="%d/%m/%Y")
                    return date
    
    def transform_pq_first_sent_to_client_date_columns(self,config_path):
        self.data=self.impute_missing("H:/consignment pricing using mlops/params.yaml")
        self.data["pq_first_sent_to_client_date"]=self.data["pq_first_sent_to_client_date"].apply(self.client_dates)
        self.data=self.data.drop(self.data.index[self.data["pq_first_sent_to_client_date"]=="Date Not Captured"])
        return self.data
    
    def transform_dates(self,data):
        data=data.replace("-","/")
        data=pd.to_datetime(data,format="%d/%b/%y")
        return data
    
    def transform_dates_columns(self,config_path):
        self.data=self.transform_pq_first_sent_to_client_date_columns("H:/consignment pricing using mlops/params.yaml")
        self.data["delivery_recorded_date"]=self.data["delivery_recorded_date"].apply(self.transform_dates)
        self.data["delivered_to_client_date"]=self.data["delivered_to_client_date"].apply(self.transform_dates)
        self.data["days_to_process"]=self.data["delivery_recorded_date"]-self.data["pq_first_sent_to_client_date"]
        return self.data
    
    def trans_freight_cost(self,x):
        if x.find("See")!=-1:
            return np.nan
        elif x=="Freight Included in Commodity Cost" or x=="Invoiced Separately":
            return 0
        else:
            return x 
        
    def transform_freight_cost_columns(self):
        self.data=self.transform_dates_columns("H:/consignment pricing using mlops/params.yaml")
        self.data["freight_cost_(usd)"]=self.data["freight_cost_(usd)"].apply(self.trans_freight_cost)
        self.median_value=self.data["freight_cost_(usd)"].median()
        self.data["freight_cost_(usd)"]=self.data["freight_cost_(usd)"].replace(np.nan,self.median_value)
        return self.data
        
        
a=Preprocessing()
a.transform_freight_cost_columns()
