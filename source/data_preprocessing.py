from load_data import LoadData
from get_data import GetData
from application_logging.logger import Applogger
import pandas as pd
import numpy as np
import argparse


class Preprocessing:
    def __init__(self):
        self.logger = Applogger()
        self.load_data = LoadData()
        self.get_data = GetData()

    def column_imputation(self, config_path):
        try:
            log_file = open("logs/preprocessing_logs.log", "a+")
            self.logger.log(log_file, "'column_imputation' FUNCTION STARTED")
            self.data = self.get_data.get_data(config_path)
            self.data.columns = self.data.columns.str.lower()
            self.data.columns = self.data.columns.str.replace(" ", "_")
            self.logger.log(
                log_file, "column_imputation function compiled successfully")
            return self.data
        except Exception as e:
            self.logger.log(
                log_file, "Exception occurred while compiling the code", str(e))
            self.logger.log(
                "Failed to execute the code please check your code and run")

    def impute_missing(self, config_path):
        try:
            log_file = open("logs/preprocessing_logs.log", "a+")
            self.logger.log(log_file, "'impute_missing' FUNCTION STARTED")
            self.data = self.column_imputation(config_path)
            self.data = self.data.drop("dosage", axis=1)
            self.data["shipment_mode"].fillna("Air", inplace=True)
            self.data["line_item_insurance_(usd)"].fillna(47.04, inplace=True)
            self.logger.log(
                log_file, "impute_missing function compiled successfully")
            return self.data
        except Exception as e:
            self.logger.log(
                log_file, "Exception occurred while compiling the code", str(e))
            self.logger.log(
                "Failed to execute the code please check your code and run")

    def client_dates(self, date):
        if date == "Pre-PQ Process":
            return pd.to_datetime('01/06/2009', format="%d/%m/%Y")
        elif date == "Date Not Captured":
            return "Date Not Captured"
        else:
            if len(date) < 9:
                date = pd.to_datetime(date, format="%m/%d/%y")
                return date
            else:
                date = date.replace("-", "/")
                date = pd.to_datetime(date, format="%d/%m/%Y")
                return date

    def transform_pq_first_sent_to_client_date_columns(self, config_path):
        try:
            log_file = open("logs/preprocessing_logs.log", "a+")
            self.logger.log(
                log_file, "'transform_pq_first_sent_to_client_date_columns' FUNCTION STARTED")
            self.data = self.impute_missing(config_path)
            self.data["pq_first_sent_to_client_date"] = self.data["pq_first_sent_to_client_date"].apply(
                self.client_dates)
            self.data = self.data.drop(
                self.data.index[self.data["pq_first_sent_to_client_date"] == "Date Not Captured"])
            self.logger.log(
                log_file, "transform_pq_first_sent_to_client_date_columns function compiled successfully")
            return self.data
        except Exception as e:
            self.logger.log(
                log_file, "Exception occurred while compiling the code", str(e))
            self.logger.log(
                "Failed to execute the code please check your code and run")

    def transform_dates(self, data):
        data = data.replace("-", "/")
        data = pd.to_datetime(data, format="%d/%b/%y")
        return data

    def transform_dates_columns(self, config_path):
        try:
            log_file = open("logs/preprocessing_logs.log", "a+")
            self.logger.log(
                log_file, "'transform_dates_columns' FUNCTION STARTED")
            self.data = self.transform_pq_first_sent_to_client_date_columns(
                config_path)
            self.data["delivery_recorded_date"] = self.data["delivery_recorded_date"].apply(
                self.transform_dates)
            self.data["delivered_to_client_date"] = self.data["delivered_to_client_date"].apply(
                self.transform_dates)
            self.data["days_to_process"] = self.data["delivery_recorded_date"] - \
                self.data["pq_first_sent_to_client_date"]
            self.data['days_to_process'] = self.data['days_to_process'].dt.days.astype(
                'int64')
            self.logger.log(
                log_file, "transform_dates_columns function compiled successfully")
            return self.data
        except Exception as e:
            self.logger.log(
                log_file, "Exception occurred while compiling the code", str(e))
            self.logger.log(
                "Failed to execute the code please check your code and run")

    def trans_freight_cost(self, x):
        if x.find("See") != -1:
            return np.nan
        elif x == "Freight Included in Commodity Cost" or x == "Invoiced Separately":
            return 0
        else:
            return x

    def transform_freight_cost_columns(self, config_path):
        try:
            log_file = open("logs/preprocessing_logs.log", "a+")
            self.logger.log(
                log_file, "'transform_freight_cost_columns' FUNCTION STARTED")
            self.data = self.transform_dates_columns(config_path)
            self.data["freight_cost_(usd)"] = self.data["freight_cost_(usd)"].apply(
                self.trans_freight_cost)

            self.median_value = self.data["freight_cost_(usd)"].median()
            self.data["freight_cost_(usd)"] = self.data["freight_cost_(usd)"].replace(
                np.nan, self.median_value)
            self.logger.log(
                log_file, "transform_freight_cost_columns function compiled successfully")
            return self.data
        except Exception as e:
            self.logger.log(
                log_file, "Exception occurred while compiling the code", str(e))
            self.logger.log(
                "Failed to execute the code please check your code and run")

    def drop_unnecessary_columns(self, config_path):
        try:
            log_file = open("logs/preprocessing_logs.log", "a+")
            self.logger.log(
                log_file, "'drop_unnecessary_columns' FUNCTION STARTED")
            self.config = self.get_data.read_params(config_path)
            self.data = self.transform_dates_columns(config_path)
            self.data = self.data[self.config["columns"]["select"]]
            self.logger.log(
                log_file, "drop_unnecessary_columns function compiled successfully")
            return self.data
        except Exception as e:
            self.logger.log(
                log_file, "Exception occurred while compiling the code", str(e))
            self.logger.log(
                "Failed to execute the code please check your code and run")

    def data_(self, config_path):
        try:
            log_file = open("logs/preprocessing_logs.log", "a+")
            self.logger.log(log_file, "'data' FUNCTION STARTED")
            self.config = self.get_data.read_params(config_path)
            self.data = self.drop_unnecessary_columns(config_path)
            print(self.data)
            self.data.to_csv(self.config["data"]["processed"])
            self.logger.log(log_file, "data function compiled successfully")
        except Exception as e:
            self.logger.log(
                log_file, "Exception occurred while compiling the code" + str(e))
            self.logger.log(log_file,
                            "Failed to execute the code please check your code and run")


object_ = Preprocessing()


def main_func(__name__, object_):
    if __name__ == "__main__":
        args = argparse.ArgumentParser()
        args.add_argument(
            "--config", default="H:/Consignment pricing using mlops/params.yaml")
        parsed_args = args.parse_args()
        data = object_.data_(config_path=parsed_args.config)


main_func(__name__, object_)
