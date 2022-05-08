import pandas
from get_data import GetData
from data_preprocessing import Preprocessing
from load_data import LoadData
from application_logging.logger import Applogger

class FeatureEngineering:
    def __init__(self):
        self.logger = Applogger()
        self.get_data = GetData()
        self.load_data = LoadData()

    def data_(self, config_path):
        self.config = self.get_data.read_params(
            "H:/consignment pricing using mlops/params.yaml")
        self.data = self.config["data"]["process"]
        self.data = pandas.read_csv(self.data)
        return self.data

    # outlier detection
    def outlier_detection(self, data, colname):
        self.data = data[data[colname] <= (
            data[colname].mean()+3*data[colname].std())]
        return self.data

    def remove_outliers(self, config_path):
        try:
            logfile = open("logs/feature_engineering_log.txt", "a+")
            self.logger.log(logfile, "'remove_outliers' FUNCTION STARTED")
            self.data = self.data_(
                "H:/consignment pricing using mlops/params.yaml")
            self.data0 = self.outlier_detection(self.data, "line_item_value")
            self.data1 = self.outlier_detection(
                self.data0, "unit_of_measure_(per_pack)")
            self.data2 = self.outlier_detection(self.data1, "pack_price")
            self.data3 = self.outlier_detection(self.data2, "unit_price")
            # self.data4=self.outlier_detection(self.data3,"days_to_process")
            self.data = self.data3
            self.logger.log(
                logfile, "removed outliers function compiled successfully")
            return self.data
        except Exception as e:
            self.logger.log(
                logfile, "Exception occured in remove_outliers method"+str(e))
            self.logger.log(logfile, "Error occured while removing outliers")

    def feature_engineering(self):
        self.data = self.remove_outliers(
            "H:/consignment pricing using mlops/params.yaml")
        self.data["country"].value_counts()
        frequency = self.data["country"].value_counts().to_dict()
        self.data["country"] = self.data["country"].map(frequency)

        # for i in self.data:
        #     self.data=pandas.get_dummies(i)
        self.data["days_to_process"]
        print(self.data)


object_ = FeatureEngineering()
object_.feature_engineering()
