import logging 
import os
import sys
from datetime import datetime        
# Creating logs directory to store log in files
LOG_DIR = "logs"
LOG_DIR = os.path.join(os.getcwd(), LOG_DIR)

#Creating LOG_DIR if it does not exists.
os.makedirs(LOG_DIR, exist_ok=True)


# Creating file name for log file based on current timestamp
CURRENT_TIME_STAMP = f"{datetime.now().strftime('%Y_%m_%d_%H')}"
file_name = f"log_{CURRENT_TIME_STAMP}.log"

#Creating file path for projects.
log_file_path = os.path.join(LOG_DIR, file_name)


logging.basicConfig(filename=log_file_path,
                    filemode='w',
                    format='[%(asctime)s] %(name)s - %(levelname)s - %(message)s',
                    level=logging.NOTSET)
