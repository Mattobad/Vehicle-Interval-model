import json
import re

from app import inference
from app.config import config

# def test_model_prediction(data_for_test):


def test_transform_ordinal(dataFrame_test):
    """ Tests the ordinal conversion """

    #when
    df = inference.transform_ordinal(dataFrame_test)

    #then
    assert len(df.columns) == len(dataFrame_test.columns)

    assert  df['condition'][0] in range(1,6)
    assert  df['cylinders_cat'][0] in range(1,9)
    assert  df['drive_cat'][0] in range(1,5)



def test_utils_dummies(dataFrame_test):
    """  Tests the dummies conversion for type & manufacturer"""

    #when
    for feat,cat in config.DUMMY_FEATURES.items():
        df = inference.utils_dummies(dataFrame_test,
                            feat,
                            cat)

    #then
    assert len(df) == len(dataFrame_test)

    # for vehicle type dummies
    type_list = [col for col in df.columns.values if re.search('type',col)]
    # manufacturer type dummies
    manufacturer_list = [col for col in df.columns.values if re.search('manufacturer',col)]

    # finding the separating categorical and dummy feature
    cat_val_feat = [col for col in type_list if df[col].dtypes=='O']
    num_val_feat = [col for col in type_list if df[col].dtypes!='O']

    assert len(df[type_list].columns) == len(type_list)
    assert len(df[manufacturer_list].columns) == len(manufacturer_list)
    assert len(cat_val_feat) == len(df[cat_val_feat].columns)
    assert len(num_val_feat) == len(df[num_val_feat].columns)
    
    # check the one-hot encoding
    for var in num_val_feat:
        assert df[var][0] in range(0,2) 


def test_transform_dummies(dataFrame_test):
    """ Tests all dummies conversion"""

    # when 
    df = inference.transform_dummies(dataFrame_test)

    #then
    assert df['fuel_gas'][0] in range(0,2)

    # for vehicle fuel dummies
    fuel_list = [col for col in df.columns.values if re.search('fuel',col)]
    # finding the separating categorical and dummy feature
    cat_val_feat = [col for col in fuel_list if df[col].dtypes=='O']
    num_val_feat = [col for col in fuel_list if df[col].dtypes!='O']

    assert len(cat_val_feat) == len(df[cat_val_feat].columns)
    assert len(num_val_feat) == len(df[num_val_feat].columns)


def test_derived_feature(dataFrame_test):
    """ Tests the validity of derived feature """

    df = inference.derived_feature(dataFrame_test,config.DERIVED_FEATURE,
                                                    config.REF_FEATURE)


    assert len(df) == len(dataFrame_test)

    assert isinstance(int(df[config.DERIVED_FEATURE][0]),int) == True


def test_preprocess(dataFrame_test):
    """ Tests the final result of all the preprocessing functions """

    df = inference.preprocess(dataFrame_test)

    assert len(df) == len(dataFrame_test)

    # check number of numerical and categorical columns
    cat_cols = [col for col in df.columns if df[col].dtypes == 'O']
    num_cols = [col for col in df.columns if df[col].dtypes != 'O']

    assert len(df[cat_cols].columns) == len(cat_cols)
    assert len(df[num_cols].columns) == len(num_cols)


def test_model_prediction(dataFrame_test):
    """ Tests the validity of model predicitons """

    preds = inference.model_prediction(dataFrame_test)

    assert type(preds['lower'])==type(preds['mid'])==type(preds['upper'])== type(180.2) # check float type
    assert len(preds) == 3
