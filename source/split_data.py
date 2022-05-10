from sklearn.model_selection import train_test_split
from get_data import GetData
from feature_engineering import FeatureEngineering
import pandas as pd
import argparse
from application_logging.logger import Applogger

class SplitData:
    def __init__(self):
        self.app_logger=Applogger()
        self.get_data=GetData()
        self.feature_engineering=FeatureEngineering()
        
    def split_data(self,config_path):
        self.config=self.get_data.read_params(config_path)
        self.data=self.config["final_data"]["transformed_data"]
        self.train_data=self.config["split_data"]["train_path"]
        self.test_data=self.config["split_data"]["test_path"]
        self.split_ratio=self.config["split_data"]["split_ratio"]
        self.random_state=self.config["base"]["random_state"]
        self.data=pd.read_csv(self.data,sep=",")
        self.data=self.data.drop("Unnamed: 0",axis=1)
        self.train,self.test=train_test_split(self.data,test_size=self.split_ratio,random_state=self.random_state)
        self.train.to_csv(self.train_data,sep=",",index=False,encoding="UTF-8")
        self.test.to_csv(self.test_data,sep=",",index=False,encoding="UTF-8")
        self.train_data=pd.read_csv(self.train_data)
        print(self.train_data)
        self.test_data=pd.read_csv(self.test_data)
        print(self.test_data)
        print(self.test_data.shape)
        print(self.train_data.shape)
   
object_=SplitData()
     
if __name__=="__main__":
    args=argparse.ArgumentParser()
    args.add_argument("--config",default="H:/consignment pricing using mlops/params.yaml")
    parsed_args=args.parse_args()
    data=object_.split_data(config_path=parsed_args.config)