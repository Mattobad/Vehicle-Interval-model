from app.config import config



def test_config_model_features(model_features):
    """ Tests validity of different sets of features in config """

    input_feat,model_feat,derived_feat,reference_feat = model_features

    assert set(input_feat) == set(config.INPUT_FEATURES)

    assert set(model_feat) == set(config.MODEL_FEATURES)

    assert derived_feat == config.DERIVED_FEATURE

    assert reference_feat == config.REF_FEATURE


def test_config_model_utils(model_name,model_path):
    """ Tests validity related to trained models """

    # models name
    low_md_name,mid_md_name,high_md_name = model_name

    # models path
    low_md_path,md_mid_path,md_high_path = model_path


    assert low_md_name == config.TRAINED_LOW_MODEL
    assert mid_md_name == config.TRAINED_MID_MODEL
    assert high_md_name == config.TRAINED_UP_MODEL

    assert low_md_path == config.LOW_MODEL_PATH
    assert md_mid_path == config.MID_MODEL_PATH
    assert md_high_path ==  config.UP_MODEL_PATH


def test_ordinal_variables_map(ordinal_variables):
    """ Tests validity in ordinal variables mapping """

    assert set(ordinal_variables.keys()) == set(config.ORDINAL_FEATURES_MAPPING.keys())

    for key,inner_dict in config.ORDINAL_FEATURES_MAPPING.items():
        # check the length of the inner dictionary
        assert len(ordinal_variables[key]) == len(inner_dict)

        # check keys of the inner dictionary
        assert set(ordinal_variables[key].keys()) == set(inner_dict.keys())
        # check inner dictionary values
        for inner_key,value in inner_dict.items():
            # check for each of the values
            assert ordinal_variables[key][inner_key] == value


def test_dummy_features(dummy_features):
    """ Tests dummy features required for the models """

    assert set(dummy_features.keys()) == set(config.DUMMY_FEATURES.keys())

    for key,value in config.DUMMY_FEATURES.items():
        # check the values 
        assert set(value) == set(dummy_features[key])