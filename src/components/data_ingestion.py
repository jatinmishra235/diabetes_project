import os
import sys
from pymongo.mongo_client import MongoClient
import pandas as pd
import numpy as np
from dataclasses import dataclass
from src.constant import *
from src.exception import CustomException
from src.logger import logging


@dataclass
class DataIngestionConfig:
    artifacts_folder = os.path.join(artifacts_folder)


class DataIngestion:
    def __init__(self):
        self.DataIngestionConfig = DataIngestionConfig()

    def export_collection_as_dataframe(self,collection,database):
        try:
            mongo_client = MongoClient(mongo_db_url)

            collection = mongo_client[database][collection]

            df = pd.DataFrame(list(collection.find()))

            if "_id" in df.columns.to_list():
                df = df.drop('_id', axis=1)

            df.replace({'na':np.nan}, inplace = True)

            return df
        except Exception as e:
            raise CustomException(e, sys)
        
    def export_data_into_feature_store_filepath(self):
        """
        Method Name : export_data_into_feature_store_filepath
        Description : This method reads data from mongodb and stores it into artifact
        Output : dataset is returned as pd.DataFrame

        """

        try:
            logging.info('exporting data from mongodb')
            raw_file_path = self.DataIngestionConfig.artifacts_folder
            os.makedirs(raw_file_path, exist_ok=True)

            diabetes_data = self.export_collection_as_dataframe(collection=collection_name, database=database_name)

            logging.info(f"saving exported data into feature store file path: {raw_file_path}")

            feature_store_file_path = os.path.join(raw_file_path, 'diabetes_mongo.csv')

            diabetes_data.to_csv(feature_store_file_path, index=False)

            return feature_store_file_path
        
        except Exception as e:
            raise CustomException(e, sys)
        
    def initiate_data_ingestion(self):
        """
        Method Name : initiate_data_ingestion
        Description : This method initiates data ingestion component of training pipeline
        """
        logging.info("entered initiate_data_ingestion")

        try:
            feature_store_filepath = self.export_data_into_feature_store_filepath()

            logging.info('got data from mongodb')

            return feature_store_filepath
        
        except Exception as e:
            raise CustomException(e, sys)