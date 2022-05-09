import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
from get_data import GetData
from data_preprocessing import Preprocessing
from load_data import LoadData
from application_logging.logger import Applogger
import numpy as np
import argparse

class FeatureEngineering:
    def __init__(self):
        self.logger = Applogger()
        self.get_data = GetData()
        self.load_data = LoadData()

    def data_(self,config_path):
        self.config = self.get_data.read_params(config_path)
        self.data = self.config["data"]["processed"]
        self.data = pd.read_csv(self.data)
        return self.data

    # outlier detection
    def outlier_detection(self, data, colname):
        self.data = data[data[colname] <= (
            data[colname].mean()+3*data[colname].std())]
        return self.data

    def remove_outliers(self,config_path):
        try:
            logfile = open("logs/feature_engineering_log.txt", "a+")
            self.logger.log(logfile, "'remove_outliers' FUNCTION STARTED")
            self.data = self.data_(config_path)
            self.data0 = self.outlier_detection(self.data, "line_item_value")
            self.data1 = self.outlier_detection(
                self.data0, "unit_of_measure_(per_pack)")
            self.data2 = self.outlier_detection(self.data1, "pack_price")
            self.data3 = self.outlier_detection(self.data2, "unit_price")
            # self.data4=self.outlier_detection(self.data3,"days_to_process")
            self.data = self.data3
            self.logger.log(
                logfile, "removed outliers function compiled successfully")
            return self.data
        except Exception as e:
            self.logger.log(
                logfile, "Exception occured in remove_outliers method"+str(e))
            self.logger.log(logfile, "Error occured while removing outliers")

    def trans_freight_cost(self,x):
        if x.find("See")!=-1:
            return np.nan
        elif x=="Freight Included in Commodity Cost" or x=="Invoiced Separately":
            return 0
        else:
            return x
    
    def freight_cost_transform(self,config_path):
        self.data = self.remove_outliers(config_path)
        self.data["freight_cost_(usd)"]=self.data["freight_cost_(usd)"].apply(self.trans_freight_cost)
        self.median_value=self.data["freight_cost_(usd)"].median()
        self.data["freight_cost_(usd)"]=self.data["freight_cost_(usd)"].replace(np.nan,self.median_value)
        self.data["freight_cost_(usd)"]=self.data["freight_cost_(usd)"].astype(float)
        return self.data
    
    def feature_engineering(self,config_path):
        self.data = self.freight_cost_transform(config_path)
        self.data["po_/_so_#"]=pd.get_dummies(self.data["po_/_so_#"])
        self.data["asn/dn_#"]=pd.get_dummies(self.data["asn/dn_#"])
        self.data["country"].value_counts()
        frequency=self.data["country"].value_counts().to_dict()
        self.data["country"]=self.data["country"].map(frequency)
        self.data["fulfill_via"]=pd.get_dummies(self.data["fulfill_via"])
        self.data["vendor_inco_term"]=pd.get_dummies(self.data["vendor_inco_term"])
        self.data["sub_classification"]=pd.get_dummies(self.data["sub_classification"])
        self.data["first_line_designation"]=pd.get_dummies(self.data["first_line_designation"])
        self.data["shipment_mode"]=pd.get_dummies(self.data["shipment_mode"])
        self.data["pq_#"]=pd.get_dummies(self.data["pq_#"])
        print(self.data)
        # [data for data in self.data if self.data[data].dtypes=="O"]

    def final_data(self,config_path):
            try:
                log_file = open("logs/feature_engineering_log.txt", "a+")
                self.logger.log(log_file, "'data' FUNCTION STARTED")
                self.finaldata = self.feature_engineering(config_path)
                self.config = self.get_data.read_params(config_path)
                self.data.drop("Unnamed: 0",axis=1,inplace=True)
                self.data.to_csv(self.config["final_data"]["transformed_data"])
                self.logger.log(log_file, "data function compiled successfully")
            except Exception as e:
                self.logger.log(log_file, "Exception occurred while compiling the code"+ str(e))
                self.logger.log(log_file,"Failed to execute the code please check your code and run")

object_=FeatureEngineering()

if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="H:/consignment pricing using mlops/params.yaml")
    parsed_args = args.parse_args()
    data = object_.final_data(config_path=parsed_args.config)


