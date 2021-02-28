import os
# from pathlib import Path


# root package
# PACKAGE_ROOT =Path('ml-api').resolve().parent

# TRAINED_MODEL_DIR = PACKAGE_ROOT / "trained-models"


# target label
TARGET = 'price'

# trained model name
TRAINED_LOW_MODEL = 'low-quantil-model_14_Impfeat.pkl'
TRAINED_MID_MODEL = 'mid-quantil-model_14_Impfeat.pkl'
TRAINED_UP_MODEL = 'up-quantil-model_14_Impfeat.pkl'

# common path
TRAINED_PATH = 'app/trained-model/'
# model path
LOW_MODEL_PATH = os.path.join(TRAINED_PATH,TRAINED_LOW_MODEL)
MID_MODEL_PATH = os.path.join(TRAINED_PATH,TRAINED_MID_MODEL)
UP_MODEL_PATH = os.path.join(TRAINED_PATH,TRAINED_UP_MODEL)

# input variables
INPUT_FEATURES =['year','cylinders','odometer',
                    'drive','fuel','condition','manufacturer','type']

# model features
# MODEL_FEATURES =['vehicle_age','cylinders_cat','odometer','drive_cat','fuel_gas',
#                     'condition']

MODEL_FEATURES = ['year','odometer','cylinders_cat','vehicle_age',
                'drive_cat','fuel_gas','type_sedan',
                'type_truck','type_pickup','manufacturer_toyota',
                'manufacturer_nissan','manufacturer_ram',
                'manufacturer_ford','condition']

# derived feature
DERIVED_FEATURE = 'vehicle_age'
# reference feature
REF_FEATURE = 'year'

# features that are dropped during training the model
# DROP_FEATURES = ['cylinders','drive','fuel']

# # ordinal encoding features
# ORDINAL_FEATURES = ['condition','cylinders','drive']

# one-hot encoding features
DUMMY_FEATURES = {'type': ['sedan','truck','pickup'],
                  'manufacturer':['toyota','nissan','ram','ford']}

# mapping for Ordinal categorical variables
ORDINAL_DRIVE = {'4wd':4,              
                'fwd':3,              
                'rwd':2,               
                'other':1}

ORDINAL_CYLINDERS = {'12 cylinders':8, 
            '10 cylinders':7,
            '8 cylinders':6,
            '6 cylinders':5,   
            '5 cylinders':4, 
            '4 cylinders':3,      
            '3 cylinders':2,      
            'other':1}

ORDINAL_CONDITION = {'new':5,
    'like new':4, 
    'excellent':3,
    'good':2, 
    'fair':1
    }

# ordinal mapping for features
ORDINAL_FEATURES_MAPPING = {
    'condition':ORDINAL_CONDITION,
    'cylinders':ORDINAL_CYLINDERS,
    'drive':ORDINAL_DRIVE
}

class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'things-to-keep-secret'


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class TestConfig(Config):
    TESTING = True