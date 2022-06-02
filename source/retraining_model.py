import os
from train_evaluate import TrainEvaluate

GET_CWD=os.getcwd()
PARAM_FILE_NAME="params.yaml"
PARAM_FILE=os.path.join(GET_CWD,PARAM_FILE_NAME)
print(PARAM_FILE)
if __name__=="__main__":
    try:
        TrainEvaluate().model_eval(PARAM_FILE)
    except Exception as e:
        print("Error",e)
        