from get_data import GetData
import argparse
import sys
from app_exception.app_exception import AppException

main_log_file=open("H:/consignment pricing using mlops/logs/logs.log", "a+")
from application_logging import logging

class LoadData:
    def __init__(self):
        self.getdata=GetData()
        
    def load_data(self,config_path):
        try:
            logging.info(f"Loading data from the source")
            self.config = self.getdata.read_params(config_path)
            self.data=self.getdata.get_data(config_path)
            self.raw_data = self.config["load_data"]["raw_data_csv"]
            self.data.to_csv(self.raw_data, index=False)
            logging.info(f"Data Loaded from the source Successfully !!!")
            return self.data
        except Exception as e:
            logging.info(f"Exception Occurred while loading data from the source -->{e}")
            raise AppException(e, sys) from e


object_ = LoadData()

if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="H:/consignment pricing using mlops/params.yaml")
    parsed_args = args.parse_args()
    object_.load_data(config_path=parsed_args.config)
