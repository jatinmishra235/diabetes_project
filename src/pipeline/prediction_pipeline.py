import os, sys
import pandas as pd

from flask import request

from src.exception import CustomException
from src.logger import logging

from src.constant import *
from src.utils.main_utils import MainUtils

from dataclasses import dataclass

@dataclass
class PredictionPipelineConfig:
    prediction_dir = 'prediction'
    prediction_file_name = 'prediction.csv'
    model_file_path = os.path.join(artifacts_folder,'model.pkl')
    preprocessor_file_path = os.path.join(artifacts_folder,'preprocessor.pkl')
    prediction_file_path = os.path.join(prediction_dir,prediction_file_name)

class PredictionPipeline:
    def __init__(self, request):
        self.request = request
        self.utils = MainUtils()
        self.prediction_pipeline_config = PredictionPipelineConfig()

    def save_input_file(self):
        """
        Method : save_input_file
        Description : This method saves input file to prediction artifact
        """
        try:
            pred_input_file_dir = 'prediction_artifacts'
            os.makedirs(pred_input_file_dir, exist_ok=True)

            input_file = self.request.files['file']
            pred_file_path = os.path.join(pred_input_file_dir, input_file.filename)

            input_file.save(pred_file_path)

            return pred_file_path
        except Exception as e :
            raise CustomException(e,sys)
        
    def predict(self,features):
        try:

            model = self.utils.load_object(filename=self.prediction_pipeline_config.model_file_path)
            preprocessor = self.utils.load_object(filename=self.prediction_pipeline_config.preprocessor_file_path)

            transformed_x = preprocessor.transform(features)

            pred = model.predict(transformed_x)

            return pred
        except Exception as e:
            raise CustomException(e,sys)
        
    def get_predicted_dataframe(self,input_file_path):
        try:
            prediction_column_name = target_column
            input_dataframe = pd.read_csv(input_file_path)

            input_dataframe = input_dataframe.drop('Unnamed: 0', axis=1) if 'Unnamed: 0' in input_dataframe.columns else input_dataframe

            predictions = self.predict(input_dataframe)

            input_dataframe[prediction_column_name] = [pred for pred in predictions]

            target_mapping = {0:'non_diabetic',1:'Diabetic'}

            input_dataframe[prediction_column_name] = input_dataframe[prediction_column_name].map(target_mapping)

            # os.makedirs(self.prediction_pipeline_config.prediction_dir, exist_ok=True)

            input_dataframe.to_csv(self.prediction_pipeline_config.prediction_file_path)

        except Exception as e:
            raise CustomException(e,sys) from e
        
    def run_prediction_pipeline(self):
        try:
            input_csv_path = self.save_input_file()
            self.get_predicted_dataframe(input_csv_path)
            return self.prediction_pipeline_config
        except Exception as e:
            raise CustomException(e,sys)


