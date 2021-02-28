import pandas as pd
import numpy as np
import joblib

from datetime import datetime as dt
import time
import logging

from app.config import config


# set the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# for showing the logs to console
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

# adding the stream handler
logger.addHandler(stream_handler)


def model_prediction(df):
    """
    Function to return quantile prediction(0.25,0.5,0.75)

    Args:
        df: user data from as dataFrame
    
    Returns:
        quantile prediction as json
    """
    start_time = time.time()
    lower_model = joblib.load(config.LOW_MODEL_PATH)
    mid_model = joblib.load(config.MID_MODEL_PATH)
    upper_model = joblib.load(config.UP_MODEL_PATH)
    logger.info(f'load time for all the models = {time.time() - start_time :.4f} secs')

    # preprocessing the data
    df = preprocess(df)
    
    # list of prediction
    preds_list = []
    # loading the trained models
    try:
        preds_list.append(lower_model.predict(df[config.MODEL_FEATURES]))
        preds_list.append(mid_model.predict(df[config.MODEL_FEATURES]))
        preds_list.append(upper_model.predict(df[config.MODEL_FEATURES]))
    except:
        logger.exception('Error in getting predictions!!!')

    #sort the list
    preds_list =sorted(preds_list)

    # predictions as dict
    predictions = {  
                    'lower': float(np.round(preds_list[0],2)),
                    'mid': float(np.round(preds_list[1],2)),
                    'upper': float(np.round(preds_list[2],2))
                    }

    logger.info(f'quantile prediction: {predictions}')

    return predictions

# data transformation functions
def preprocess(df):
    """
    Function to process the data for the model

    Args:
        df: user's input as dataFrame
    Returns:
        dataFrame ready for model
    """
    #change the ordinal features
    df = transform_ordinal(df)
    
    # change the dummy features
    df = transform_dummies(df)
    
    # derived feature
    df = derived_feature(df,config.DERIVED_FEATURE,config.REF_FEATURE)
    
    #drop the features
    #df = df.drop(config.DROP_FEATURES,axis=1)
    
    return df

# data transformation functions

def transform_ordinal(df):
    """
    Function to transform the data to make it ready to feed into the trained model
    Args:
        df: dataFrame
    """

    for feature,val in config.ORDINAL_FEATURES_MAPPING.items():
        if feature == 'condition':
            df[feature] = df[feature].map(val)
        else:
            feature_val = df[feature]
            #df[feature] = val[feature_val]
            df[feature+'_cat'] = df[feature].map(val)

    return df

def transform_dummies(df):
    """
    Function to return the dataFrame with dummy variables
    Args:
        df: dataFrame
    """
    # convert for fuel
    if df['fuel'][0] == 'gas':
        df['fuel_gas'] = 1
    else:
        df['fuel_gas'] = 0

    # converting the dummies variables
    for feat,categories in config.DUMMY_FEATURES.items():
        df = utils_dummies(df,feat,categories)
    
    return df

def utils_dummies(df,feature,cat_feature):
    """
    Function to return df with dummies encoding for a particular features
    Args:
        df: dataframe
        feature: feature to which dummies encoding to be returned
        cat_feature: list of categories in the feature
    """

    # converting the list into set
    cat_feature = set(cat_feature)

    if cat_feature.intersection(df[feature]):
        df[feature+"_"+ df[feature][0]] = 1
    # for rest of the values
    for val in list(cat_feature.difference(df[feature])):
        df[feature+"_"+val] = 0 

    return df

def derived_feature(df,derived_feature,reference_feature):
    """
    Function to calculate the derived variable vehicle age
    Args:
        df: dataFrame,
        derived_feature: name of the derived feature
        reference_feature: name of the feature used to calculate the derived variable
    """

    df[derived_feature] = dt.now().year - df[reference_feature]

    return df
