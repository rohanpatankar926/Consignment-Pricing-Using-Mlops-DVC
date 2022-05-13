from get_data import GetData
import argparse
from application_logging.logger import Applogger

class LoadData:
    def __init__(self):
        self.logger = Applogger()
        self.getdata = GetData()

    def load_data(self, config_path):
        try:
            log_file=open("logs/load_data_log.log", "a+") 
            self.logger.log(log_file, "'load_data' FUNCTION STARTED")
            self.config = self.getdata.read_params(config_path)
            self.data = self.getdata.get_data(config_path)
            self.raw_data = self.config["load_data"]["raw_data_csv"]
            self.data.to_csv(self.raw_data, index=False)
            self.logger.log(log_file, "Data loaded successfully to 'raw' folder")
        except Exception as e:
            log_file=open("logs/load_data_log.log", "a+") 
            self.logger.log(log_file, "Exception occured in load_data method"+str(e))
            self.logger.log(log_file, "Error occured while loading the data")


object_ = LoadData()

if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument(
        "--config", default="/params.yaml")
    parsed_args = args.parse_args()
    object_.load_data(config_path=parsed_args.config)
