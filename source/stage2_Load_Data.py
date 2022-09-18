from stage1_Get_Data import GetData
import argparse
import sys
from app_exception.app_exception import AppException
from application_logging import logging

class LoadData:
    '''
    The main functionality of this class is to load the data to the folder path
    we have assigned in params.yaml file
    function return data and save it to folder we have assigned 
    written by Rohan Patankar
    '''
    def __init__(self):
        self.getdata = GetData()

    def load_data(self, config_path):
        try:
            logging.info(f"Loading data from the source")
            self.config = self.getdata.read_params(config_path)
            self.data = self.getdata.get_data(config_path)
            self.raw_data = self.config["load_data"]["raw_data_csv"]
            self.data.to_csv(self.raw_data, index=False)
            logging.info(f"Data Loaded from the source Successfully !!!")
            return self.data
        except Exception as e:
            logging.info(
                f"Exception Occurred while loading data from the source -->{e}")
            raise AppException(e, sys) from e

if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument(
        "--config", default="/home/dataguy/Desktop/Consignment-Pricing-Using-Mlops-DVC-main/params.yaml")
    parsed_args = args.parse_args()
    LoadData().load_data(config_path=parsed_args.config)
