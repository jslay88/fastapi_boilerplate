def test_model_list(unit_test_client, valid_auth_token_header):
    response = unit_test_client.get('/api/v1/model',
                                    headers=valid_auth_token_header)
    assert response.status_code == 200
    assert 'models' in response.json()
    assert len(response.json()['models']) > 0


def test_predict_route(unit_test_client, valid_auth_token_header):
    # Basic Predict Test. Needs response validation
    response = unit_test_client.post(
        '/api/v1/model/example/predict',
        json={
            'field_1': 'string',
            'a_number_field_1': 0,
            'a_number_field_2': 22
        },
        headers=valid_auth_token_header
    )

    assert response.status_code == 200
