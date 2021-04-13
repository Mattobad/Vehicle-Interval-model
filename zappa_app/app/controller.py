from flask import Blueprint, jsonify, request
from flask_cors import CORS

import pandas as pd

import os
import sys
import json
import logging
import time

from app.inference import model_prediction
from app.config import config



# set app log
LOGGING_LEVEL = os.environ.get('LOGGING_LEVEL', 'DEBUG').upper()
logger = logging.getLogger(__name__)
logger.setLevel(LOGGING_LEVEL)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(LOGGING_LEVEL)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.handlers = []
logger.addHandler(handler)
logger.propagate = False  # to prevent log duplication in lambda

# set boto log level
logging.getLogger('boto3').setLevel(logging.CRITICAL)
logging.getLogger('boto').setLevel(logging.CRITICAL)
logging.getLogger('botocore').setLevel(logging.CRITICAL)
logging.getLogger('urllib3').setLevel(logging.CRITICAL)
logging.getLogger('s3transfer').setLevel(logging.CRITICAL)
logging.getLogger('zappa').setLevel(logging.CRITICAL)


prediction_app = Blueprint('prediction_app',__name__)

CORS(prediction_app)

"""Routes"""
@prediction_app.route('/')
def index():
    
    return jsonify({'results':'ok'}),200



@prediction_app.route('/v1/model/predict',methods=['POST'])
def predict():
    """
    ---
    post:
        description: predict the vehicle price based on user inputs
        requestBody:
            required: true
            content:
                application/json:
                schema: json
        
        responses:
            '200':
                description: on success
                content:
                    application/json:
                        schema: json
    """
    if request.method == 'POST':
        # extract post data from request body as JSON
        json_data = request.get_json()
        logger.info(f'User input from UI: {json_data}')

        start_time = time.time()
        # df = pd.read_json(json_io,typ='series')
        df = pd.DataFrame.from_dict([json_data])
        logger.info(f'columns: {df.columns}')

        # preprocess the data
        preds = model_prediction(df)

        logger.info(f'models prediction time = {time.time() - start_time :.4f} secs')

        
        return jsonify(preds),200





