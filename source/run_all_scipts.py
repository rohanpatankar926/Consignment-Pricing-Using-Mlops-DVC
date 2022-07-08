'''This script functionality to run all the python scripts sequentially so that we can train it in frontend.'''

from stage1_Get_Data import GetData
from stage2_Load_Data import LoadData
from stage3_preprocessing import Preprocessing
from time import sleep
from stage5_split_data import SplitData
from stage4_feature_engineering import FeatureEngineering
from stage6_train_evaluate import TrainEvaluate
import os
import subprocess

GET_CWD=os.getcwd()
PARAM_FILE_NAME="params.yaml"
PARAM_FILE=os.path.join(GET_CWD,PARAM_FILE_NAME)

# mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root .\artifacts\ --host 127.0.0.1 -p 1234

if __name__=="__main__":
    GetData().get_data(PARAM_FILE)
    sleep(0.1)
    LoadData().load_data(PARAM_FILE)
    sleep(0.1)
    Preprocessing().data_(PARAM_FILE)
    sleep(0.1)
    FeatureEngineering().final_data(PARAM_FILE)
    sleep(0.1)
    SplitData().split_data(PARAM_FILE)
    sleep(0.1)
    TrainEvaluate().model_eval(PARAM_FILE)