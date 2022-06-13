from get_data import GetData
from load_data import LoadData
from data_preprocessing import Preprocessing
from feature_engineering import FeatureEngineering
from time import sleep
import os 

GET_CWD=os.getcwd()
PARAM_FILE_NAME="params.yaml"
PARAM_FILE=os.path.join(GET_CWD,PARAM_FILE_NAME)

def training(PARAM_FILE):
    getdata=GetData().get_data(PARAM_FILE)
    load_data=LoadData().load_data(PARAM_FILE)
    preprocessing=Preprocessing().data_(PARAM_FILE)
    feature_engineering=FeatureEngineering().final_data(PARAM_FILE)

if __name__=="__main__":
    training(PARAM_FILE)
    