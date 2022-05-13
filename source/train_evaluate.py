from statistics import mean
from get_data import GetData
from feature_engineering import FeatureEngineering
import numpy as np
from sklearn.metrics import mean_absolute_error,r2_score,mean_squared_error
from sklearn.ensemble import GradientBoostingRegressor
from urllib.parse import urlparse
import pandas as pd
import argparse
from application_logging.logger import Applogger
import pandas as pd
import joblib
import json
import os

class TrainEvaluate:
    def __init__(self):
        self.get_data=GetData()
        self.logger=Applogger()
        self.feature_engineering=FeatureEngineering()
   
    def evaluation_metrics(self,act,pred):
        self.r2_score=r2_score(act,pred)
        self.mse=mean_squared_error(act,pred)
        self.rmse=np.sqrt(self.mse)
        return self.r2_score,self.mse,self.rmse

    def model_eval(self,config_path):
        self.config=self.get_data.read_params(config_path)
        self.test_data=self.config["split_data"]["test_path"]
        self.train_data=self.config["split_data"]["train_path"]
        self.model_dir=self.config["model_dirs"]
        self.target_col=self.config["base"]["target_data"]
        self.train=pd.read_csv(self.train_data,sep=",")
        self.test=pd.read_csv(self.test_data,sep=",")
        self.learning_rate=self.config["estimators"]["GradientBoostingRegressor"]["params"]["learning_rate"]
        self.n_estimators=self.config["estimators"]["GradientBoostingRegressor"]["params"]["n_estimators"]
        self.alpha=self.config["estimators"]["GradientBoostingRegressor"]["params"]["alpha"]
        self.verbose=self.config["estimators"]["GradientBoostingRegressor"]["params"]["verbose"]
        self.val_factor=self.config["estimators"]["GradientBoostingRegressor"]["params"]["validation_fraction"]
        self.tol=self.config["estimators"]["GradientBoostingRegressor"]["params"]["tol"]
        self.ccp_alpha=self.config["estimators"]["GradientBoostingRegressor"]["params"]["ccp_alpha"]
        self.x_train,self.x_test=self.train.drop(self.target_col,axis=1),self.test.drop(self.target_col,axis=1) 
        self.y_train,self.y_test=self.train[self.target_col],self.test[self.target_col]
        GB=GradientBoostingRegressor(learning_rate=self.learning_rate,n_estimators=self.n_estimators,alpha=self.alpha,verbose=self.verbose,validation_fraction=self.val_factor,tol=self.tol,ccp_alpha=self.ccp_alpha)
        GB.fit(self.x_train,self.y_train)
        y_pred=GB.predict(self.x_test)
        (r2,rmse,mse)=self.evaluation_metrics(self.y_test,y_pred)
        print(r2*100,rmse,mse)
        
        # normalized_rmse=rmse/(63770.43-1121)
        # print(f"normalized rmse::{normalized_rmse}")
        
        os.makedirs(self.model_dir,exist_ok=True)
        self.model_path=os.path.join(self.model_dir,"model.pkl")
        
        joblib.dump(GB,self.model_path)
        
    #################reports logging###############

        scores_file=self.config["reports"]["scores"]
        params_file=self.config["reports"]["params"]
        
        with open(scores_file,"w") as f:
            scores={
            "rmse":rmse,
            "mse":mse,
            "r2 score":r2,
            "rmse":rmse,
            # "normalized rmse":self.normalized_rmse
                }
            json.dump(scores,f,indent=4)
        with open(params_file,"w") as f:
            params={
                "learning_rate":self.learning_rate,
                "n_estimators":self.n_estimators,
                "verbose":self.verbose,
                "validation_fraction":self.val_factor,
                "tol":self.tol,
                "ccp":self.ccp_alpha
            }
            json.dump(params,f,indent=4)

object_=TrainEvaluate()

if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    data=object_.model_eval(config_path=parsed_args.config)

