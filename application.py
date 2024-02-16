from flask import render_template, jsonify, Flask, send_file, request
from src.logger import logging
from src.exception import CustomException
import sys

from src.pipeline.training_pipeline import TrainingPipeline
from src.pipeline.prediction_pipeline import PredictionPipeline

logging.info('app started')


application = Flask(__name__)

@application.route("/")
def home():
    return "welcome to my appliction"

@application.route("/train")
def training():
    try:
        training_pipeline = TrainingPipeline()
        training_pipeline.run_pipeline()
        return "Training is completed"
    except Exception as e:
        raise CustomException(e,sys)
    
@application.route("/predict", methods = ['POST', 'GET'])
def prediction():
    try:
        if request.method == 'POST':
            prediction_pipeline = PredictionPipeline(request)

            prediction_file_detail = prediction_pipeline.run_prediction_pipeline()

            return send_file(prediction_file_detail.prediction_file_path,
                             download_name=prediction_file_detail.prediction_file_name,
                             as_attachment=True)
        else:
            return render_template('upload_file.html')
    except Exception as e:
        raise CustomException(e,sys)
    
if __name__=='__main__':
    application.run(host="0.0.0.0", port=5000, debug=True)
