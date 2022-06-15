import sys
sys.path.append("H:/consignment pricing using mlops")
import numpy as np
from sklearn.metrics import mean_absolute_error,r2_score,mean_squared_error
from sklearn.ensemble import RandomForestRegressor
from urllib.parse import urlparse
import pandas as pd
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import GridSearchCV
import argparse
import sys
from app_exception.app_exception import AppException
from application_logging import logging
import pandas as pd
import joblib
import json
import os
from get_data import GetData


class TrainEvaluate:
    def __init__(self):
        self.get_data=GetData()

   
    def evaluation_metrics(self,act,pred):
        self.r2_score=r2_score(act,pred)
        self.mse=mean_squared_error(act,pred)
        self.rmse=np.sqrt(mean_squared_error(act,pred))
        return self.r2_score,self.mse,self.rmse

    def model_eval(self,config_path):
        try:
            
            logging.info(
"'train_evaluate' function started")
            self.config=self.get_data.read_params(config_path)
            self.test_data=self.config["split_data"]["test_path"]
            self.train_data=self.config["split_data"]["train_path"]
            self.model_dir=self.config["model_dirs"]
            self.target_col=self.config["base"]["target_data"]
            logging.info("train data read successfully-->path: "+self.train_data)
            self.train=pd.read_csv(self.train_data,sep=",")
            logging.info("train data read successfully")
            self.test=pd.read_csv(self.test_data,sep=",")
            logging.info("test data read successfully")
            logging.info("model training started")
            self.criterion=self.config["estimators"]["RandomForestRegressor"]["params"]["criterion"]
            self.max_deapth=self.config["estimators"]["RandomForestRegressor"]["params"]["max_deapth"]
            self.min_sample_leaf=self.config["estimators"]["RandomForestRegressor"]["params"]["min_sample_leaf"]
            self.n_estimators=self.config["estimators"]["RandomForestRegressor"]["params"]["n_estimators"]
            self.min_sample_split=self.config["estimators"]["RandomForestRegressor"]["params"]["min_sample_split"]
            self.oob_score=self.config["estimators"]["RandomForestRegressor"]["params"]["oob_score"]
            self.x_train,self.x_test=self.train.drop(self.target_col,axis=1),self.test.drop(self.target_col,axis=1) 
            self.y_train,self.y_test=self.train[self.target_col],self.test[self.target_col]
        
        
            rf=RandomForestRegressor()
            RCV = RandomizedSearchCV(estimator = rf, 
                         param_distributions = self.config["RandomizedSearchCV"]["params"], 
                         n_iter = self.config["RandomizedSearchCV"]["n_iter"], 
                         scoring = self.config["RandomizedSearchCV"]["scoring"], 
                         cv = self.config["RandomizedSearchCV"]["cv"], 
                         verbose=self.config["RandomizedSearchCV"]["verbose"], 
                         random_state=42, 
                         n_jobs=self.config["RandomizedSearchCV"]["n_jobs"], 
                         return_train_score=self.config["RandomizedSearchCV"]["return_train_score"])
            RCV.fit(self.x_train,self.y_train)
            rf.fit(self.x_train,self.y_train)
            # Feature importances
            self.rf1_feature_imp = pd.DataFrame(rf.feature_importances_, index = self.x_train.columns, columns = ['Feature_importance'])

            self.rf1_feature_imp.sort_values(by = 'Feature_importance', ascending = False, inplace = True)

            print(round(self.rf1_feature_imp,3))
            self.rf1_feature_imp['Feature_importance'] = self.rf1_feature_imp[self.rf1_feature_imp['Feature_importance'] > 0.001] 

            self.rf1_feature_imp = self.rf1_feature_imp[self.rf1_feature_imp['Feature_importance'].notna()]
            self.features_by_rf = self.rf1_feature_imp.index
            
            self.x_train_rf=self.x_train[self.features_by_rf]
            self.x_test_rf=self.x_test[self.features_by_rf]
            
            self.x_train.to_csv(self.config["data"]["training_data"])
            self.x_test.to_csv(self.config["data"]["test_data"])
            
            rf2=RandomForestRegressor()
            RCV = RandomizedSearchCV(estimator = rf2, 
                         param_distributions = self.config["RandomizedSearchCV"]["params"], 
                         n_iter = self.config["RandomizedSearchCV"]["n_iter"], 
                         scoring = self.config["RandomizedSearchCV"]["scoring"], 
                         cv = self.config["RandomizedSearchCV"]["cv"], 
                         verbose=self.config["RandomizedSearchCV"]["verbose"], 
                         random_state=42, 
                         n_jobs=self.config["RandomizedSearchCV"]["n_jobs"], 
                         return_train_score=self.config["RandomizedSearchCV"]["return_train_score"])
            RCV.fit(self.x_train,self.y_train)
            
        
            rf2=RCV.best_estimator_
            rf2.fit(self.x_train,self.y_train)
            y_pred=rf.predict(self.x_test)
            logging.info("Model Trained on RandomizedSearchCV successfully")
            (r2,mse,rmse)=self.evaluation_metrics(self.y_test,y_pred)
            print(r2*100,mse,rmse)
            
            # normalized_rmse=rmse/(63770.43-1121)
            # print(f"normalized rmse::{normalized_rmse}")
            
            os.makedirs(self.model_dir,exist_ok=True)
            self.model_path=os.path.join(self.model_dir,"model_rf.pkl")
            
            joblib.dump(rf2,self.model_path)
            
        #################reports logging###############

            scores_file=self.config["reports"]["scores"]
            params_file=self.config["reports"]["params"]
            
            with open(scores_file,"w") as f:
                scores={
                "rmse":rmse,
                "r2 score":r2*100,
                # "normalized rmse":self.normalized_rmse
                    }
                json.dump(scores,f,indent=4)
            logging.info("scores written to file")
            with open(params_file,"w") as f:
                params={
                    "best params":RCV.best_params_,
                    "criterion":self.criterion,
                    "n_estimators":self.n_estimators,
                    "max_deapth":self.max_deapth,
                    "min_sample_leaf":self.min_sample_leaf,
                    "min_sample_split":self.min_sample_split,
                    "oob_score":self.oob_score
                }
                json.dump(params,f,indent=4)
        except Exception as e:
            logging.info("Exception occured in 'train_evaluate' function"+str(e))
            logging.info(
"train_evaluate function reported error in the function")
            raise AppException(e, sys) from e

object_=TrainEvaluate()

if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="H:/consignment pricing using mlops/params.yaml")
    parsed_args = args.parse_args()
    data=object_.model_eval(config_path=parsed_args.config)

