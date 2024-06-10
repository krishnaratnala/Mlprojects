'''
    logger is purpose of any excecution that probabliy happen we should be able to 
    log all those iformation and execution are in some files 

    if we get any erroe catch in the exception we going to log in to text file 
'''


import logging
import os
from datetime import datetime 
LOG_FILE =f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
log_path=os.path.join(os.getcwd(),"logs",LOG_FILE)
os.makedirs(log_path,exist_ok=True)
LOG_FILE_PATH=os.path.join(log_path,LOG_FILE)


logging.basicConfig(
    filename=LOG_FILE_PATH ,
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s- %(message)s",
    level=logging.INFO
)
