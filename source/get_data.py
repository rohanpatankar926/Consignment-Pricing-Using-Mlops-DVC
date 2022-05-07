# This python file is for fetching the data and dump to the folder called data
# import modules and libraries
import pandas as pd
import sys
sys.path.append('H:\consignment pricing using mlops')
from application_logging.logger import Applogger
import yaml
import argparse

class GetData:
    def __init__(self):
        self.logger = Applogger()
        
    def read_params(self,config_path):
        try:
            log_file = open("logs/get_data_log.txt", "a+")
            self.logger.log(log_file,"'read_params' FUNCTION STARTED")
            with open(config_path) as file:
                self.config = yaml.safe_load(file)
                self.logger.log(log_file,"config file i.e 'params.yaml' loaded successfully")
                return self.config
            
        except Exception as e:
            self.logger.log(
                log_file, "Exception occured in read_params method:"+str(e))
            self.logger.log(
                log_file, "Error occured while reading the yaml file")
            log_file.close()
            
    def get_data(self,config_path):
        try:
            log_file = open("logs/get_data_log.txt", "a+")
            self.logger.log(log_file,"'get_data' FUNCTION STARTED")
            self.config = self.read_params(config_path)
            self.data_path = self.config["data_source"]["local_data"]
            self.raw_path = self.config["raw_data"]["raw"]
            self.data = pd.read_csv(self.raw_path)
            self.logger.log(log_file,"Raw data loaded successfully")
            return self.data
        except Exception as e:
            self.logger.log(
                log_file, "Exception occured in get_data method:"+str(e))
            self.logger.log(log_file, "Error occured while reading the data")
            log_file.close()

object_=GetData()

def main_func(__name__, object_):
    if __name__=="__main__":
        args=argparse.ArgumentParser()
        args.add_argument("--config",default="H:/consignment pricing using mlops/params.yaml")
        parsed_args=args.parse_args()
        data=object_.get_data(config_path=parsed_args.config)

main_func(__name__, object_)
