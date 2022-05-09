from application_logging.logger import Applogger
from get_data import GetData
from feature_engineering import FeatureEngineering
import pandas as pd
import argparse

class SplitData:
    def __init__(self):
        self.app_logger=Applogger()
        self.get_data=GetData()
        self.feature_engineering=FeatureEngineering()
        
    def split_data(self):
        pass