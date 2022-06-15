from get_data import GetData
from load_data import LoadData
from data_preprocessing import Preprocessing
from time import sleep
from split_data import SplitData
from feature_engineering import FeatureEngineering
from train_evaluate import TrainEvaluate
import os 

GET_CWD=os.getcwd()
PARAM_FILE_NAME="params.yaml"
PARAM_FILE=os.path.join(GET_CWD,PARAM_FILE_NAME)

def training(PARAM_FILE):
    getdata=GetData().get_data(PARAM_FILE)
    load_data=LoadData().load_data(PARAM_FILE)
    preprocessing=Preprocessing().data_(PARAM_FILE)
    feature_engineering=FeatureEngineering().final_data
    (PARAM_FILE)
    split_data=SplitData().split_data(PARAM_FILE)
    train_evaluate=TrainEvaluate().model_eval(PARAM_FILE)

if __name__=="__main__":
    training(PARAM_FILE)