import os 
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd 
from sklearn.model_selection import train_test_split 
from dataclasses import dataclass

@dataclass
class DataIngestioncofig:
    train_data_path: str = os.path.join('artifacts', "train.csv")
    test_data_path: str = os.path.join('artifacts', "test.csv")
    raw_data_path: str = os.path.join('artifacts', "data.csv")

class DataIngestion:
    def __init__(self) -> None:
        self.Ingestion_config = DataIngestioncofig()
    
    def initate_data_ingestion(self):
        logging.info("Entered the data ingestion method or config")

        try:
            df = pd.read_csv("notebook/data/stud.csv")
            logging.info("Reading the dataset as dataframe")
            
            # Ensure the directories for both raw data and train/test data exist
            os.makedirs(os.path.dirname(self.Ingestion_config.raw_data_path), exist_ok=True)
            os.makedirs(os.path.dirname(self.Ingestion_config.train_data_path), exist_ok=True)
            
            df.to_csv(self.Ingestion_config.raw_data_path, index=False, header=True)
            logging.info("Raw data saved")

            logging.info("Train test split initiated")
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)
            train_set.to_csv(self.Ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.Ingestion_config.test_data_path, index=False, header=True)
            
            logging.info("Ingestion of the data is completed")
            return(
                self.Ingestion_config.train_data_path,
                self.Ingestion_config.test_data_path
            )
        except Exception as e:
            raise CustomException(e, sys)

if __name__ == '__main__':
    obj1 = DataIngestion()
    obj1.initate_data_ingestion()
