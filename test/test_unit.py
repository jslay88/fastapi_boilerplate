def test_health_check(unit_test_client):
    response = unit_test_client.get('/health')
    assert response.status_code == 200
    assert 'health' in response.json()
    assert response.json()['health'] == 'healthy'


def test_auth(unit_test_client, valid_auth_token_header):
    response = unit_test_client.get('/auth_test',
                                    headers=valid_auth_token_header)
    assert response.status_code == 200


def test_invalid_auth(unit_test_client, invalid_auth_token_header):
    response = unit_test_client.get('/auth_test',
                                    headers=invalid_auth_token_header)
    assert response.status_code == 401
    assert 'detail' in response.json()
    assert response.json()['detail'] == 'Unauthorized'


def test_no_auth_header(unit_test_client):
    response = unit_test_client.get('/auth_test')
    assert response.status_code == 403
    assert 'detail' in response.json()
    assert response.json()['detail'] == 'Not authenticated'


def test_correlation_id(unit_test_client):
    # Test Correlation ID
    header = {
        'X-Correlation-ID': 'Test Correlation ID'
    }
    response = unit_test_client.get('/health',
                                    headers=header)
    assert response.status_code == 200
    assert response.headers.get('X-Correlation-ID') == header['X-Correlation-ID']

    # Test No Correlation ID
    response = unit_test_client.get('/health')
    assert response.status_code == 200
    assert response.headers.get('X-Correlation-ID') is None


def test_request_id(unit_test_client):
    # Test Request ID
    header = {
        'X-Request-ID': 'Test Request ID'
    }
    response = unit_test_client.get('/health',
                                    headers=header)
    assert response.status_code == 200
    assert response.headers.get('X-Request-ID') == header['X-Request-ID']

    # Test Generated Request ID
    response = unit_test_client.get('/health')
    assert response.status_code == 200
    assert response.headers.get('X-Request-ID') is not None
    assert len(response.headers.get('X-Request-ID')) == 36
