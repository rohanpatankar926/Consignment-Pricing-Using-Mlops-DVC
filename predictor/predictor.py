import os 
import sys
import dill
from numpy import apply_along_axis
from app_exception import app_exception
import pandas as pd

class ConsignmentData:
    def __init__(self,
                line_item_insurance:float, 
                line_item_quantity:float, 
                pack_price:float,
                days_to_process:float, 
                unit_price:float, 
                freight_cost:float, 
                country:float,
                unit_of_measure:float,
                line_item_value:float=None
                ):
        try:
            self.line_item_insurance=line_item_insurance 
            self.line_item_quantity=line_item_quantity 
            self.pack_price=pack_price
            self.days_to_process=days_to_process 
            self.unit_price=unit_price 
            self.freight_cost=freight_cost 
            self.country=country
            self.unit_of_measure=unit_of_measure
            self.line_item_value=line_item_value
        except Exception as e:
            raise app_exception(e,sys) from e
    
    def get_housing_input_data_frame(self):
        try:
            consignment_input_dict=self.get_housing_data_as_dict()
            return pd.DataFrame(consignment_input_dict)
        except Exception as e:
            raise app_exception(e,sys) from e
    
    def get_housing_data_as_dict(self):
        try:
            input_data={
                'line_item_insurance':[self.line_item_insurance],
                'line_item_quantity':[self.line_item_quantity], 
                'pack_price':[self.pack_price],
                'days_to_process':[self.days_to_process], 
                'unit_price':[self.unit_price], 
                'freight_cost':[self.freight_cost], 
                'country':[self.country],
                'unit_of_measure':[self.unit_of_measure],
                'line_item_value':[self.line_item_value]
            }
            return input_data
        except Exception as e:
            raise app_exception(e,sys)

class ConsignmentPredictor:
    def __init__(self,model_dir:str):
        try:
            self.model_dir=model_dir
        except Exception as e:
            raise app_exception(e,sys) from e
    
    # def get_latest_model_path(self):
    #     try:
    #         folder_name = list(map(int, os.listdir(self.model_dir)))
    #         latest_model_dir = os.path.join(self.model_dir, f"{max(folder_name)}")
    #         file_name = os.listdir(latest_model_dir)[0]
    #         latest_model_path = os.path.join(latest_model_dir, file_name)
    #         return latest_model_path
    #     except Exception as e:
    #         raise app_exception(e, sys) from e
    def get_latest_model_path(self):
        try:
            folder_name =  os.listdir(self.model_dir)
            
            return folder_name
        except Exception as e:
            raise app_exception(e, sys) from e
        
    def load_object(file_path:str):
        """
    file_path: str
    """
        try:
            with open(file_path, "rb") as file_obj:
                return dill.load(file_obj)
        except Exception as e:
            raise app_exception(e,sys) from e
        
    def pred(self, X):
        try:
            model_path = self.get_latest_model_path()
            model = self.load_object(file_path=model_path)
            consignment_pricing = model.predict(X)
            return consignment_pricing[0]
        except Exception as e:
            raise app_exception(e, sys) from e