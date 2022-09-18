# This python file is for fetching the data and dump to the folder called data
# import modules and libraries
import sys

import pandas as pd
import argparse
import yaml
sys.path.append("/home/dataguy/Desktop/Consignment-Pricing-Using-Mlops-DVC-main")
from app_exception.app_exception import AppException
from application_logging import logging


class GetData:
    '''
    The main functionality is to get data from source 
    Function return None
    written by:Rohan patankar  
    '''
    def __init__(self):
        pass

    def read_params(self, config_path):
        try:
            logging.info(f"Reading all parameters from config_path")
            with open(config_path) as file:
                self.config = yaml.safe_load(file)
                logging.info(
                    f"Parameters Readed from config_path Successfully !!!")
                return self.config

        except Exception as e:
            logging.info(
                f"Exception Occurred while reading parameters from config_path -->{e}")
            raise AppException(e, sys) from e

    def get_data(self, config_path):
        try:
            logging.info(f"Getting the data from the source")
            self.config = self.read_params(config_path)
            self.data_path = self.config["data_source"]["local_data"]
            self.raw_path = self.config["raw_data"]["raw"]
            self.data = pd.read_csv(self.raw_path)
            logging.info(f"Data Fetched from the source Successfully !!!")
            return self.data
        except Exception as e:
            logging.info(
                f"Exception Occurred while getting data from the source -->{e}")
            raise AppException(e, sys) from e

if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="/home/dataguy/Desktop/Consignment-Pricing-Using-Mlops-DVC-main/params.yaml")
    parsed_args = args.parse_args()
    data = GetData().get_data(config_path=parsed_args.config)
