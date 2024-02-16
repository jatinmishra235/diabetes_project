from pymongo.mongo_client import MongoClient
import pandas as pd
import json
import os
import src
from src.constant import *


client = MongoClient(mongo_db_url)

database = 'practice'
collection = 'diabetes'

file_path = os.path.abspath(r'/Users/jatin/Diabetes_project/data/diabetes.csv')


df = pd.read_csv(file_path)
df = df.drop('Unnamed: 0', axis=1) if 'Unnamed: 0' in df.columns.to_list() else df

json_record = list(json.loads(df.T.to_json()).values())

client[database][collection].insert_many(json_record)