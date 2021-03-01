import pytest
import pandas as pd
import os

from app.config import config
from app.app import create_app

@pytest.fixture
def app():
    app = create_app(config_object=config.TestConfig)
    with app.app_context():
        yield app


@pytest.fixture()
def flask_test_client(app):
    with app.test_client() as test_client:
        yield test_client

@pytest.fixture()
def data_for_test():
    test_dict = {
                "year":1990,
                "odometer":290010.9,
                "cylinders":"4 cylinders",
                "drive":"4wd",
                "fuel":"gas",
                "condition":"good",
                "manufacturer":"ford",
                "type":"suv"
            } 

    yield test_dict

@pytest.fixture()
def dataFrame_test(data_for_test):

    df = pd.DataFrame.from_dict([data_for_test])

    yield df


@pytest.fixture()
def model_features():

    input_feat =['year','cylinders','odometer',
                    'drive','fuel','condition','manufacturer','type']

    model_feat = ['year','odometer','cylinders_cat','vehicle_age',
                'drive_cat','fuel_gas','type_sedan',
                'type_truck','type_pickup','manufacturer_toyota',
                'manufacturer_nissan','manufacturer_ram',
                'manufacturer_ford','condition']


    derived_feat = 'vehicle_age'

    reference_feat = 'year'

    yield input_feat,model_feat,derived_feat,reference_feat


@pytest.fixture()
def model_name():
    low_md_name = 'low-quantil-model_14_Impfeat.pkl'
    mid_md_name = 'mid-quantil-model_14_Impfeat.pkl'
    high_md_name = 'up-quantil-model_14_Impfeat.pkl'

    yield low_md_name,mid_md_name,high_md_name


@pytest.fixture()
def model_path(model_name):
    # get model names
    md_low,md_mid,md_high = model_name

    # common path
    trained_path = 'zappa-app/app/trained-model/'
    # model paths
    low_md_path = os.path.join(trained_path,md_low)
    md_mid_path = os.path.join(trained_path,md_mid)
    md_high_path = os.path.join(trained_path,md_high)

    yield low_md_path,md_mid_path,md_high_path


@pytest.fixture()
def ordinal_variables():
    # drive map
    ord_drive = {'4wd':4,              
                'fwd':3,              
                'rwd':2,               
                'other':1}
    # cylinders map
    ord_cyl = {'12 cylinders':8, 
            '10 cylinders':7,
            '8 cylinders':6,
            '6 cylinders':5,   
            '5 cylinders':4, 
            '4 cylinders':3,      
            '3 cylinders':2,      
            'other':1}
    # conditin map
    ord_cond = {'new':5,
            'like new':4, 
            'excellent':3,
            'good':2, 
            'fair':1}

    # ordinal mapping for features
    ord_mapping = {
                'condition':ord_cond,
                'cylinders':ord_cyl,
                'drive':ord_drive
            }
    
    yield ord_mapping


@pytest.fixture()
def dummy_features():
    dummy_feat = {'type': ['sedan','truck','pickup'],
                  'manufacturer':['toyota','nissan','ram','ford']}

    yield dummy_feat