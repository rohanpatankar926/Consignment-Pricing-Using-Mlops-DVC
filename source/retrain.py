
from train_evaluate import TrainEvaluate


if __name__=="__main__":
    try:
        TrainEvaluate().model_eval("H:/consignment pricing using mlops/params.yaml")
    except Exception as e:
        print("Error",e)
        