from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.data_trainer import ModelTrainer
from src.exception import CustomException

import sys

class TrainingPipeline:
    
    def start_data_ingestion(self):
        try:
            self.data_ingestion = DataIngestion()
            feature_store_file_path = self.data_ingestion.initiate_data_ingestion()
            return feature_store_file_path
        except Exception as e:
            raise CustomException(e,sys)

    def start_data_transformation(self, feature_store_file_path):
        try:
            self.data_transformation = DataTransformation(feature_store_file_path=feature_store_file_path)
            train_arr, test_arr, preprocessor_path = self.data_transformation.initiate_data_transformation()
            return train_arr, test_arr, preprocessor_path
        except Exception as e:
            raise CustomException(e,sys)
        
    def start_data_training(self, train_arr, test_arr):
        try:
            self.data_trainer = ModelTrainer()
            model_score = self.data_trainer.initiate_model_trainer(train_arr,test_arr)
            return model_score
        except Exception as e:
            raise CustomException(e, sys)
        
    def run_pipeline(self):
        try:
            feature_store_file_path = self.start_data_ingestion()
            train_arr, test_arr, preprocessor_path = self.start_data_transformation(feature_store_file_path)
            score = self.start_data_training(train_arr,test_arr)
            print('training has been completed and score is ',score)
        except Exception as e:
            raise CustomException(e, sys)

