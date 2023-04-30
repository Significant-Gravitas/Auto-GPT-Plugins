import pytest
import requests
import requests_mock
import json
from .api_tools import _make_api_call

def test_make_api_call_get_method():
    with requests_mock.Mocker() as mock_req:
        mock_url = 'https://mockapi.com/endpoint'
        mock_response = 'Mock Response'
        mock_req.get(mock_url, text=mock_response)
        response = _make_api_call(host='https://mockapi.com', endpoint='/endpoint', method='GET')
        expected_response = json.dumps({
            "response": mock_response,
            "status_code": 200
        })
        assert response == expected_response

def test_make_api_call_post_method():
    with requests_mock.Mocker() as mock_req:
        mock_url = 'https://mockapi.com/endpoint'
        mock_response = 'Mock Post Response'
        mock_req.post(mock_url, text=mock_response)
        body = {"message": "test message"}
        response = _make_api_call(host='https://mockapi.com', endpoint='/endpoint', method='POST', body=body)
        expected_response = json.dumps({
            "response": mock_response,
            "status_code": 200
        })
        assert response == expected_response

def test_make_api_call_put_method():
    with requests_mock.Mocker() as mock_req:
        mock_url = 'https://mockapi.com/endpoint'
        mock_response = 'Mock Put Response'
        mock_req.put(mock_url, text=mock_response)
        body = {"message": "test message"}
        response = _make_api_call(host='https://mockapi.com', endpoint='/endpoint', method='PUT', body=body)
        expected_response = json.dumps({
            "response": mock_response,
            "status_code": 200
        })
        assert response == expected_response

def test_make_api_call_delete_method():
    with requests_mock.Mocker() as mock_req:
        mock_url = 'https://mockapi.com/endpoint'
        mock_response = 'Mock Delete Response'
        mock_req.delete(mock_url, text=mock_response)
        response = _make_api_call(host='https://mockapi.com', endpoint='/endpoint', method='DELETE')
        expected_response = json.dumps({
            "response": mock_response,
            "status_code": 200
        })
        assert response == expected_response

def test_make_api_call_patch_method():
    with requests_mock.Mocker() as mock_req:
        mock_url = 'https://mockapi.com/endpoint'
        mock_response = 'Mock Patch Response'
        mock_req.patch(mock_url, text=mock_response)
        body = {"message": "test message"}
        response = _make_api_call(host='https://mockapi.com', endpoint='/endpoint', method='PATCH', body=body)
        expected_response = json.dumps({
            "response": mock_response,
            "status_code": 200
        })
        assert response == expected_response

def test_make_api_call_head_method():
    with requests_mock.Mocker() as mock_req:
        mock_url = 'https://mockapi.com/endpoint'
        mock_response = 'Mock Head Response'
        mock_req.head(mock_url, text=mock_response)
        response = _make_api_call(host='https://mockapi.com', endpoint='/endpoint', method='HEAD')
        expected_response = json.dumps({
            "response": mock_response,
            "status_code": 200
        })
        assert response == expected_response

def test_make_api_call_option_method():
    with requests_mock.Mocker() as mock_req:
        mock_url = 'https://mockapi.com/endpoint'
        mock_response = 'Mock Option Response'
        mock_req.options(mock_url, text=mock_response)
        response = _make_api_call(host='https://mockapi.com', endpoint='/endpoint', method='OPTIONS')
        expected_response = json.dumps({
            "response": mock_response,
            "status_code": 200
        })
        assert response == expected_response

def test_make_api_call_invalid_host():
    response = _make_api_call(host='invalid_host', endpoint='/endpoint', method='GET')
    response_dict = json.loads(response)
    assert response_dict['response'] == 'Invalid host or endpoint'
    assert response_dict['status_code'] is None

def test_make_api_call_invalid_endpoint():
    with requests_mock.Mocker() as mock_req:
        with pytest.raises(ValueError):
            _make_api_call(host='https://mockapi.com', endpoint='endpoint', method='GET')

def test_make_api_call_invalid_url():
    with requests_mock.Mocker() as mock_req:
        with pytest.raises(ValueError):
            _make_api_call(host='https://mockapi.com', endpoint='https://mockapi.com/endpoint', method='GET')

def test_make_api_call_invalid_method():
    with requests_mock.Mocker() as mock_req:
        with pytest.raises(ValueError):
            _make_api_call(host='https://mockapi.com', endpoint='/endpoint', method='INVALID_METHOD')

def test_make_api_call_query_params_eq_string():
    with requests_mock.Mocker() as mock_req:
        mock_url = 'https://mockapi.com/endpoint'
        mock_response = 'Mock Response'
        mock_req.get(mock_url, text=mock_response)
        response = _make_api_call(host='https://mockapi.com', endpoint='/endpoint', method='GET', query_params='test=1')
        expected_response = json.dumps({
            "response": mock_response,
            "status_code": 200
        })
        assert response == expected_response

def test_make_api_call_query_params_eq_dict():
    with requests_mock.Mocker() as mock_req:
        mock_url = 'https://mockapi.com/endpoint'
        mock_response = 'Mock Response'
        mock_req.get(mock_url, text=mock_response)
        response = _make_api_call(host='https://mockapi.com', endpoint='/endpoint', method='GET', query_params={'test': 1})
        expected_response = json.dumps({
            "response": mock_response,
            "status_code": 200
        })
        assert response == expected_response

def test_make_api_call_body_eq_json():
    with requests_mock.Mocker() as mock_req:
        mock_url = 'https://mockapi.com/endpoint'
        mock_response = 'Mock Response'
        mock_req.post(mock_url, text=mock_response)
        response = _make_api_call(host='https://mockapi.com', endpoint='/endpoint', method='POST', body='{"message": "test message"}')
        expected_response = json.dumps({
            "response": mock_response,
            "status_code": 200
        })
        assert response == expected_response

def test_make_api_call_body_eq_dict():
    with requests_mock.Mocker() as mock_req:
        mock_url = 'https://mockapi.com/endpoint'
        mock_response = 'Mock Response'
        mock_req.post(mock_url, text=mock_response)
        response = _make_api_call(host='https://mockapi.com', endpoint='/endpoint', method='POST', body={"message": "test message"})
        expected_response = json.dumps({
            "response": mock_response,
            "status_code": 200
        })
        assert response == expected_response

def test_make_api_call_body_eq_list():
    with requests_mock.Mocker() as mock_req:
        mock_url = 'https://mockapi.com/endpoint'
        mock_response = 'Mock Response'
        mock_req.post(mock_url, text=mock_response)
        response = _make_api_call(host='https://mockapi.com', endpoint='/endpoint', method='POST', body=["test message"])
        expected_response = json.dumps({
            "response": mock_response,
            "status_code": 200
        })
        assert response == expected_response

def test_make_api_call_body_eq_string():
    with requests_mock.Mocker() as mock_req:
        mock_url = 'https://mockapi.com/endpoint'
        mock_response = 'Mock Response'
        mock_req.post(mock_url, text=mock_response)
        response = _make_api_call(host='https://mockapi.com', endpoint='/endpoint', method='POST', body="test message")
        expected_response = json.dumps({
            "response": mock_response,
            "status_code": 200
        })
        assert response == expected_response

def test_make_api_call_body_eq_none():
    with requests_mock.Mocker() as mock_req:
        mock_url = 'https://mockapi.com/endpoint'
        mock_response = 'Mock Response'
        mock_req.post(mock_url, text=mock_response)
        response = _make_api_call(host='https://mockapi.com', endpoint='/endpoint', method='POST', body=None)
        expected_response = json.dumps({
            "response": mock_response,
            "status_code": 200
        })
        assert response == expected_response

def test_make_api_call_headers_eq_json():
    with requests_mock.Mocker() as mock_req:
        mock_url = 'https://mockapi.com/endpoint'
        mock_response = 'Mock Response'
        mock_req.post(mock_url, text=mock_response)
        response = _make_api_call(host='https://mockapi.com', endpoint='/endpoint', method='POST', headers='{"Content-Type": "application/json"}')
        expected_response = json.dumps({
            "response": mock_response,
            "status_code": 200
        })
        assert response == expected_response

def test_make_api_call_headers_eq_string():
    with requests_mock.Mocker() as mock_req:
        mock_url = 'https://mockapi.com/endpoint'
        mock_response = 'Mock Response'
        mock_req.post(mock_url, text=mock_response)
        response = _make_api_call(host='https://mockapi.com', endpoint='/endpoint', method='POST', headers="Content-Type: application/json")
        expected_response = json.dumps({
            "response": mock_response,
            "status_code": 200
        })
        assert response == expected_response

def test_make_api_call_headers_eq_dict():
    with requests_mock.Mocker() as mock_req:
        mock_url = 'https://mockapi.com/endpoint'
        mock_response = 'Mock Response'
        mock_req.post(mock_url, text=mock_response)
        response = _make_api_call(host='https://mockapi.com', endpoint='/endpoint', method='POST', headers={"Content-Type": "application/json"})
        expected_response = json.dumps({
            "response": mock_response,
            "status_code": 200
        })
        assert response == expected_response

def test_make_api_call_headers_eq_none():
    with requests_mock.Mocker() as mock_req:
        mock_url = 'https://mockapi.com/endpoint'
        mock_response = 'Mock Response'
        mock_req.post(mock_url, text=mock_response)
        response = _make_api_call(host='https://mockapi.com', endpoint='/endpoint', method='POST', headers=None)
        expected_response = json.dumps({
            "response": mock_response,
            "status_code": 200
        })
        assert response == expected_response

def test_make_api_call_timeout_eq_int():
    with requests_mock.Mocker() as mock_req:
        mock_url = 'https://mockapi.com/endpoint'
        mock_req.get(mock_url, exc=requests.exceptions.ConnectTimeout)
        response = _make_api_call(host='https://mockapi.com', endpoint='/endpoint', method='GET', timeout=1)
        expected_response = json.dumps({
            "response": "Request timed out.",
            "status_code": 408
        })
        assert response == expected_response

def test_make_api_call_timeout_eq_float():
    with requests_mock.Mocker() as mock_req:
        mock_url = 'https://mockapi.com/endpoint'
        mock_req.get(mock_url, exc=requests.exceptions.ConnectTimeout)
        response = _make_api_call(host='https://mockapi.com', endpoint='/endpoint', method='GET', timeout=1.0)
        expected_response = json.dumps({
            "response": "Request timed out.",
            "status_code": 408
        })
        assert response == expected_response

def test_make_api_call_timeout_eq_string():
    with requests_mock.Mocker() as mock_req:
        mock_url = 'https://mockapi.com/endpoint'
        mock_req.get(mock_url, exc=requests.exceptions.ConnectTimeout)
        response = _make_api_call(host='https://mockapi.com', endpoint='/endpoint', method='GET', timeout="1.0")
        expected_response = json.dumps({
            "response": "Request timed out.",
            "status_code": 408
        })
        assert response == expected_response

def test_make_api_call_timeout_eq_none():
    with requests_mock.Mocker() as mock_req:
        mock_url = 'https://mockapi.com/endpoint'
        mock_req.get(mock_url, exc=requests.exceptions.ConnectTimeout)
        response = _make_api_call(host='https://mockapi.com', endpoint='/endpoint', method='GET', timeout=None)
        expected_response = json.dumps({
            "response": "Request timed out.",
            "status_code": 408
        })
        assert response == expected_response