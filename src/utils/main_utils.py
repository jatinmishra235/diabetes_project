import sys
import os
import pandas as pd
import pickle

from src.exception import CustomException
from src.logger import logging
import yaml

class MainUtils:
    def __init__(self):
        pass

    @staticmethod
    def save_object(file_path, obj):
        logging.info('entered the save_object method pf MainUtils class')

        try:
            with open(file_path, 'wb') as file_obj:
                pickle.dump(obj, file_obj)
            
            logging.info('exited the save_object method of MainUtils class')
        except Exception as e:
            raise CustomException(e, sys)
        

    def read_yaml_file(self, filename):
        try:
            with open(filename, 'rb') as yaml_file:
                return yaml.safe_load(yaml_file)
        except Exception as e:
            raise CustomException(e,sys)

    @staticmethod 
    def load_object(filename):
        logging.info('entered into load_object')
        try:
            with open(filename, 'rb') as object:
                obj = pickle.load(object)
            return obj
        except Exception as e:
            raise CustomException(e,sys)

