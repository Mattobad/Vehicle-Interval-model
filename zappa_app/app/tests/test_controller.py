import json

def test_status_endpoint_returns_200(flask_test_client):
    """Tests the staus of the endpoint"""

    res = flask_test_client.get('/')

    assert res.status_code == 200
    res_json = json.loads(res.data)
    result = res_json['results']
    assert result == 'ok'


def test_pred_endpoint_returns_prediciton(flask_test_client,data_for_test):
    """Tests model prediction endpoint"""

    #when 
    res = flask_test_client.post('/v1/model/predict',json=data_for_test)

    #then 
    assert res.status_code == 200

    # load the response
    res_json = json.loads(res.data)
    lower_preds = res_json['lower']
    mid_preds = res_json['mid']
    upper_preds = res_json['upper']

    assert type(lower_preds)==type(mid_preds)==type(upper_preds)== type(180.2) # check float type