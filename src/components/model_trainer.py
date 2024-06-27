import os 
import sys
from dataclasses import dataclass
from catboost import CatBoostRegressor
from sklearn.ensemble import (
    AdaBoostRegressor, GradientBoostingRegressor, RandomForestRegressor
)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRFRegressor
from src.exception import CustomException
from src.logger import logging
from src.utils import save_object, evalute_models

@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join("artifacts", "model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()
    
    def Intiate_model_trainer(self, train_array, test_array):
        try:
            logging.info("Split Training and test input data")
            x_train, y_train, x_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1]
            )
            models = {
                "LinearRegression": LinearRegression(),
                "DecisionTreeRegressor": DecisionTreeRegressor(),
                "RandomForestRegressor": RandomForestRegressor(),
                "KNeighborsRegressor": KNeighborsRegressor(),
                "AdaBoostRegressor": AdaBoostRegressor(),
                "GradientBoostingRegressor": GradientBoostingRegressor(),
                "XGBRFRegressor": XGBRFRegressor(),
                "CatBoostRegressor": CatBoostRegressor()
            }

            params = {
                "DecisionTreeRegressor": {
                    'criterion': ['squared_error', 'friedman_mse', 'absolute_error', 'poisson']
                },
                "RandomForestRegressor": {
                    'n_estimators': [10, 50, 100, 200, 300, 400, 500],
                },
                "GradientBoostingRegressor": {
                    'learning_rate': [0.1, 0.01, 0.05, 0.001],
                    'subsample': [0.6, 0.7, 0.75, 0.8, 0.85, 0.9],
                    'n_estimators': [10, 50, 100, 200, 300, 400, 500]
                },
                "XGBRFRegressor": {
                    'learning_rate': [0.1, 0.01, 0.05, 0.001],
                    'n_estimators': [8, 16, 32, 64, 128, 256]
                },
                "LinearRegression": {
                    'fit_intercept': [True, False],
                    'copy_X': [True, False],
                    'n_jobs': [-1],
                    'positive': [True, False]
                },
                "CatBoostRegressor": {
                    'learning_rate': [0.1, 0.01, 0.05, 0.001],
                    'depth': [3, 5, 7, 9, 11, 13, 15],
                    'n_estimators': [10, 50, 100, 200, 300, 400, 500]
                },
                "KNeighborsRegressor": {
                    'n_neighbors': [3, 5, 7, 9, 11, 13, 15],
                    'weights': ['uniform', 'distance']
                },
                "AdaBoostRegressor": {
                    'n_estimators': [10, 50, 100, 200, 300, 400, 500],
                    'learning_rate': [0.1, 0.01, 0.05, 0.001]
                }
            }

            model_report: dict = evalute_models(x_train=x_train, y_train=y_train, x_test=x_test, y_test=y_test, models=models, params=params)

            # To get best model score from dict
            best_model_score = max(sorted(model_report.values()))
            # To get best model name from dict
            best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]
            
            best_model = models[best_model_name]

            if best_model_score < 0.6:
                raise CustomException("No best model found")
            logging.info(f"Best found model on both training and testing")

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )
            predicted = best_model.predict(x_test)
            r2_square = r2_score(y_test, predicted)
            return r2_square
        except Exception as e:
            raise CustomException(e, sys)
