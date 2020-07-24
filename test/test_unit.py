def test_health_check(unit_test_client):
    response = unit_test_client.get('/health')
    assert response.status_code == 200
    assert 'health' in response.json()
    assert response.json()['health'] == 'healthy'


def test_auth(unit_test_client, valid_auth_token, log_capture):
    response = unit_test_client.get('/auth_test',
                                    headers={
                                        'Authorization': f'Bearer {valid_auth_token["token"]}'
                                    })
    assert response.status_code == 200
    for log in log_capture:
        assert 'auth_description' in log
        assert log['auth_description'] == valid_auth_token['description']


def test_invalid_auth(unit_test_client, invalid_auth_token_header, log_capture):
    response = unit_test_client.get('/auth_test',
                                    headers=invalid_auth_token_header)
    assert response.status_code == 401
    assert 'detail' in response.json()
    assert response.json()['detail'] == 'Unauthorized'
    for log in log_capture:
        assert 'auth_description' in log
        assert log['auth_description'] is None


def test_no_auth_header(unit_test_client, log_capture):
    response = unit_test_client.get('/auth_test')
    assert response.status_code == 403
    assert 'detail' in response.json()
    assert response.json()['detail'] == 'Not authenticated'
    for log in log_capture:
        assert 'auth_description' in log
        assert log['auth_description'] is None


def test_correlation_id(unit_test_client, log_capture):
    # Test Correlation ID
    header = {
        'X-Correlation-ID': 'Test Correlation ID'
    }
    response = unit_test_client.get('/health',
                                    headers=header)
    assert response.status_code == 200
    assert response.headers.get('X-Correlation-ID') == header['X-Correlation-ID']
    for log in log_capture:
        assert 'correlation_id' in log
        assert log['correlation_id'] == header['X-Correlation-ID']
    log_count = len(log_capture)

    # Test No Correlation ID
    response = unit_test_client.get('/health')
    assert response.status_code == 200
    assert response.headers.get('X-Correlation-ID') is None
    for log in log_capture[log_count:]:
        assert 'correlation_id' in log
        assert log['correlation_id'] is None


def test_request_id(unit_test_client, log_capture):
    # Test Request ID
    header = {
        'X-Request-ID': 'Test Request ID'
    }
    response = unit_test_client.get('/health',
                                    headers=header)
    assert response.status_code == 200
    assert response.headers.get('X-Request-ID') == header['X-Request-ID']
    for log in log_capture:
        assert 'request_id' in log
        assert log['request_id'] == header['X-Request-ID']
    log_count = len(log_capture)

    # Test Generated Request ID
    response = unit_test_client.get('/health')
    assert response.status_code == 200
    assert response.headers.get('X-Request-ID') is not None
    assert len(response.headers.get('X-Request-ID')) == 36
    for log in log_capture[log_count:]:
        assert 'request_id' in log
        assert log['request_id'] == response.headers.get('X-Request-ID')
