import sys
import os
import pandas as pd
import numpy as np

from  sklearn.metrics import accuracy_score


from xgboost import XGBClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import GridSearchCV, train_test_split

from src.constant import *
from src.exception import CustomException
from src.logger import logging
from src.utils.main_utils import MainUtils

from dataclasses import dataclass


@dataclass
class DataTrainerConfig:
    artifacts_folder = os.path.join(artifacts_folder)
    trained_model_path = os.path.join(artifacts_folder, 'model.pkl')
    model_config_file_path = os.path.join('config', 'model.yaml')

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = DataTrainerConfig()

        self.utils = MainUtils()

        self.models = {
            'logistic_regression':LogisticRegression(),
            'svc':SVC(),
            'RandomForestClassifier':RandomForestClassifier(),
            'GradientBoostClassifier':GradientBoostingClassifier()
        }

    def evaluate_model(self,x_train,y_train,x_test,y_test,models):
        try:

            report = {}

            for i in range(len(models)):
                model = list(models.values())[i]
                model.fit(x_train, y_train)

                y_train_pred = model.predict(x_train)
                y_test_pred = model.predict(x_test)

                train_model_score = accuracy_score(y_train, y_train_pred)
                test_model_score = accuracy_score(y_test, y_test_pred)

                report[list(models.keys())[i]] = test_model_score
            
            return report
        
        except Exception as e:
            raise CustomException(e,sys)
        

    def get_best_model(self,x_train,y_train,x_test,y_test):
        try:
            model_report = self.evaluate_model(
                x_train,y_train,x_test,y_test, models=self.models)
            
            print(model_report)

            best_model_score = max(sorted(model_report.values()))

            best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]

            best_model_object = self.models[best_model_name]

        except Exception as e:
            raise CustomException(e, sys)
        
    def fine_tune_best_model(self, best_model_object, best_model_name, x_train, y_train):
        try:
            model_param_grid = self.utils.read_yaml_file(self.model_trainer_config.model_config_file_path)['model_selection']['model'][best_model_name]
            grid_search = GridSearchCV(
                best_model_object, param_grid= model_param_grid, cv = 2,n_jobs=-1)
            
            grid_search.fit(x_train, y_train)

            best_params = grid_search.best_params_
            print('best params are: ', best_params)

            finetuned_model = best_model_object.set_params(**best_params)

            return finetuned_model
        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_model_trainer(self,train_array, test_array):
        try:
            logging.info('splitting training and testing data')

            x_train, y_train, x_test, y_test = (
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
            )

            model_report = self.evaluate_model(x_train=x_train,y_train=y_train,x_test=x_test,y_test=y_test,models=self.models)

            best_model_score = max(sorted(model_report.values()))

            best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]

            best_model = self.models[best_model_name]

            best_model = self.fine_tune_best_model(
                best_model_name=best_model_name,
                best_model_object=best_model,
                x_train=x_train,
                y_train=y_train
            )

            best_model.fit(x_train, y_train)
            y_pred = best_model.predict(x_test)
            best_model_score = accuracy_score(y_test,y_pred)
            
            logging.info('best model training done')
            logging.info(f'saving model path {self.model_trainer_config.trained_model_path}')

            os.makedirs(os.path.dirname(self.model_trainer_config.trained_model_path), exist_ok=True)

            self.utils.save_object(
                file_path=self.model_trainer_config.trained_model_path,
                obj = best_model
            )

            # return self.model_trainer_config.trained_model_path
            return best_model_score
        
        except Exception as e:
            raise CustomException(e,sys)