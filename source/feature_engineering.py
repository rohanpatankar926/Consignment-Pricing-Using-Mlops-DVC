import argparse
import numpy as np
from load_data import LoadData
from data_preprocessing import Preprocessing
from get_data import GetData
from sklearn.preprocessing import LabelEncoder
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import sys
from app_exception.app_exception import AppException
from application_logging import logging

class FeatureEngineering:
    def __init__(self):
        self.get_data = GetData()
        self.load_data = LoadData()

    def data_(self, config_path):
        try:
            logging.info("'data_' FUNCTION STARTED")
            self.config = self.get_data.read_params(config_path)
            self.data = self.config["data"]["processed"]
            self.data = pd.read_csv(self.data)
            logging.info("Data loaded successfully")
            return self.data
        except Exception as e:
            logging.info(
                 "Exception occurred while loading the data" + str(e))
            logging.info(
                 "Failed to load the data please check your code and run")
            raise AppException(e, sys) from e
            

    # outlier detection
    def outlier_detection(self, data, colname):
        self.data = data[data[colname] <= (
            data[colname].mean()+3*data[colname].std())]
        return self.data

    def remove_outliers(self, config_path):
        try:
            logging.info( "'remove_outliers' FUNCTION STARTED")
            self.data = self.data_(config_path)
            self.data0 = self.outlier_detection(self.data, "line_item_value")
            self.data1 = self.outlier_detection(
                self.data0, "unit_of_measure_(per_pack)")
            self.data2 = self.outlier_detection(self.data1, "pack_price")
            self.data3 = self.outlier_detection(self.data2, "unit_price")
            # self.data4=self.outlier_detection(self.data3,"days_to_process")
            self.data = self.data3
            logging.info(
                 "removed outliers function compiled successfully")
            return self.data
        except Exception as e:
            logging.info(
                 "Exception occured in remove_outliers method"+str(e))
            logging.info( "Error occured while removing outliers")
            raise AppException(e, sys) from e

    def trans_freight_cost(self, x):
        if x.find("See") != -1:
            return np.nan
        elif x == "Freight Included in Commodity Cost" or x == "Invoiced Separately":
            return 0
        else:
            return x

    def freight_cost_transform(self, config_path):
        try:
            
            logging.info(
                 "'freight_cost_transform' FUNCTION STARTED")
            self.data = self.remove_outliers(config_path)
            self.data["freight_cost_(usd)"] = self.data["freight_cost_(usd)"].apply(
                self.trans_freight_cost)
            self.median_value = self.data["freight_cost_(usd)"].median()
            self.data["freight_cost_(usd)"] = self.data["freight_cost_(usd)"].replace(
                np.nan, self.median_value)
            self.data["freight_cost_(usd)"] = self.data["freight_cost_(usd)"].astype(
                float)
            logging.info(
                 "freight_cost_transform function compiled successfully")
            return self.data
        except Exception as e:
            logging.info(
                 "Exception occurred while compiling the code" + str(e))
            logging.info(
                 "Failed to execute the code please check your code and run")
            raise AppException(e, sys) from e

    def feature_engineering(self, config_path):
        try:
            
            logging.info( "'feature_engineering' FUNCTION STARTED")
            self.data = self.freight_cost_transform(config_path)
            self.data["po_/_so_#"] = pd.get_dummies(self.data["po_/_so_#"])
            self.data["asn/dn_#"] = pd.get_dummies(self.data["asn/dn_#"])
            lb=LabelEncoder()
            self.data["country"]=lb.fit_transform(self.data["country"])
            self.data["fulfill_via"] = pd.get_dummies(self.data["fulfill_via"])
            self.data["vendor_inco_term"] = pd.get_dummies(
                self.data["vendor_inco_term"])
            self.data["sub_classification"] = pd.get_dummies(
                self.data["sub_classification"])
            self.data["first_line_designation"] = pd.get_dummies(
                self.data["first_line_designation"])
            self.data["shipment_mode"] = pd.get_dummies(
                self.data["shipment_mode"])
            # self.data["pq_#"] = pd.get_dummies(self.data["pq_#"])
            self.data.drop("pq_#",axis=1,inplace=True)
            
            logging.info(
                 "feature engineering function compiled successfully")
            return self.data
            # [data for data in self.data if self.data[data].dtypes=="O"]
        except Exception as e:
            logging.info(
                 "Exception occurred while compiling the code" + str(e))
            logging.info(
                 "Failed to execute the code please check your code and run")
            raise AppException(e, sys) from e


    def final_data(self,config_path):
        try:
            
            logging.info( "'data' FUNCTION STARTED")
            self.finaldata = self.feature_engineering(config_path)
            self.config = self.get_data.read_params(config_path)
            self.data.drop("Unnamed: 0", axis=1, inplace=True)
            self.data.to_csv(self.config["final_data"]["transformed_data"])
            print(self.data)
            logging.info( "data function compiled successfully")
        except Exception as e:
            logging.info(
                 "Exception occurred while compiling the code" + str(e))
            logging.info(
                 "Failed to execute the code please check your code and run")
            raise AppException(e, sys) from e


object_ = FeatureEngineering()

if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument(
        "--config", default="H:/consignment pricing using mlops/params.yaml")
    parsed_args = args.parse_args()
    data = object_.final_data(config_path=parsed_args.config)