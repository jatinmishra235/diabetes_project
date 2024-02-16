import sys
import os
from src.constant import *
from src.logger import logging
from src.exception import CustomException
import pandas as pd
import numpy as np
from  dataclasses import dataclass

from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from src.utils.main_utils import MainUtils


@dataclass
class DataTransformationConfig:
    artifacts_folder = os.path.join(artifacts_folder)
    transformed_train_file_path = os.path.join(artifacts_folder, 'train.csv')
    transformed_test_file_path = os.path.join(artifacts_folder, 'test.py')
    transformation_object_file_path = os.path.join(artifacts_folder, 'preprocessor.pkl')


class DataTransformation:
    def __init__(self, feature_store_file_path):
        
        self.feature_store_file_path = feature_store_file_path
        self.data_transform_config = DataTransformationConfig()
        self.utils = MainUtils()
    @staticmethod
    def get_data(feature_store_file_path):
        """
        Method Name : get_data
        Description : this method reads all data from  feature_store_file_path and returns DataFrame of merged.
        """
        
        try:
            data = pd.read_csv(feature_store_file_path)
            
            return data

        except Exception as e:
            raise CustomException(e, sys)
        
    def get_data_transformer_object(self):
        try:

            imputer_step = ('imputer', SimpleImputer(strategy = 'mean'))
            scaler_step = ('scaler', RobustScaler())

            preprocessor = Pipeline(
                steps=[
                    imputer_step,
                    scaler_step
                ]
            )
            return preprocessor
        except Exception as e:
            raise CustomException(e, sys)
        
    def initiate_data_transformation(self):
        """
        Method Name : initiate_data_transformation
        Description : this method initiates DataTransformation comeponent for pipeline
        Output      : Data transformation artifact created and returned
        """

        logging.info('entered initiate_data_transformation coponent of Data_transformation class')

        try:
            df = self.get_data(feature_store_file_path=self.feature_store_file_path)

            x = df.drop(columns=target_column)
            y = df[target_column]

            x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.2)

            preprocessor = self.get_data_transformer_object()

            x_train_scaled = preprocessor.fit_transform(x_train)
            x_test_scaled = preprocessor.transform(x_test)


            preprocessor_path = self.data_transform_config.transformation_object_file_path
            os.makedirs(os.path.dirname(preprocessor_path), exist_ok=True)
            self.utils.save_object(file_path=preprocessor_path, obj=preprocessor)

            train_arr = np.c_[x_train_scaled, np.array(y_train)]
            test_arr = np.c_[x_test_scaled, np.array(y_test)]

            return (train_arr, test_arr, preprocessor_path)
        
        except Exception as e:
            raise CustomException(e, sys)