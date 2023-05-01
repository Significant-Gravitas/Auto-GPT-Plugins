import pytest
import random
import requests_mock
import json
from .api_tools import _make_api_call

class TestAutoGPTAPITools():

    # Test call methods

    def test_api_call_get(self):
        """Test the _make_api_call() function with a GET request."""
        with requests_mock.Mocker() as m:
            m.get('http://example.com/endpoint', text='success', status_code=200)
            result = _make_api_call('http://example.com', '/endpoint')
            assert json.loads(result)['status'] == 'success'
            assert json.loads(result)['status_code'] == 200
            assert json.loads(result)['response'] == 'success'

    def test_api_call_post(self):
        """Test the _make_api_call() function with a POST request."""
        with requests_mock.Mocker() as m:
            m.post('http://example.com/endpoint', text='success', status_code=200)
            result = _make_api_call('http://example.com', '/endpoint', method='POST')
            assert json.loads(result)['status'] == 'success'
            assert json.loads(result)['status_code'] == 200
            assert json.loads(result)['response'] == 'success'

    def test_api_call_put(self):
        """Test the _make_api_call() function with a PUT request."""
        with requests_mock.Mocker() as m:
            m.put('http://example.com/endpoint', text='success', status_code=200)
            result = _make_api_call('http://example.com', '/endpoint', method='PUT')
            assert json.loads(result)['status'] == 'success'
            assert json.loads(result)['status_code'] == 200
            assert json.loads(result)['response'] == 'success'

    def test_api_call_delete(self):
        """Test the _make_api_call() function with a DELETE request."""
        with requests_mock.Mocker() as m:
            m.delete('http://example.com/endpoint', text='success', status_code=200)
            result = _make_api_call('http://example.com', '/endpoint', method='DELETE')
            assert json.loads(result)['status'] == 'success'
            assert json.loads(result)['status_code'] == 200
            assert json.loads(result)['response'] == 'success'

    def test_api_call_patch(self):
        """Test the _make_api_call() function with a PATCH request."""
        with requests_mock.Mocker() as m:
            m.patch('http://example.com/endpoint', text='success', status_code=200)
            result = _make_api_call('http://example.com', '/endpoint', method='PATCH')
            assert json.loads(result)['status'] == 'success'
            assert json.loads(result)['status_code'] == 200
            assert json.loads(result)['response'] == 'success'

    def test_api_call_head(self):
        """Test the _make_api_call() function with a HEAD request."""
        with requests_mock.Mocker() as m:
            m.head('http://example.com/endpoint', text='success', status_code=200)
            result = _make_api_call('http://example.com', '/endpoint', method='HEAD')
            assert json.loads(result)['status'] == 'success'
            assert json.loads(result)['status_code'] == 200
            assert json.loads(result)['response'] == 'success'

    def test_api_call_options(self):
        """Test the _make_api_call() function with a OPTIONS request."""
        with requests_mock.Mocker() as m:
            m.options('http://example.com/endpoint', text='success', status_code=200)
            result = _make_api_call('http://example.com', '/endpoint', method='OPTIONS')
            assert json.loads(result)['status'] == 'success'
            assert json.loads(result)['status_code'] == 200
            assert json.loads(result)['response'] == 'success'

    # Test host errors

    def test_api_call_valid_host(self):
        """Test the _make_api_call() function with a valid host."""
        with requests_mock.Mocker() as m:
            m.get('http://example.com/endpoint', text='success', status_code=200)
            result = _make_api_call('http://example.com', '/endpoint')
            assert json.loads(result)['status'] == 'success'
            assert json.loads(result)['status_code'] == 200
            assert json.loads(result)['response'] == 'success'

    def test_api_call_valid_host_https(self):
        """Test the _make_api_call() function with a valid host using HTTPS."""
        with requests_mock.Mocker() as m:
            m.get('https://example.com/endpoint', text='success', status_code=200)
            result = _make_api_call('https://example.com', '/endpoint')
            assert json.loads(result)['status'] == 'success'
            assert json.loads(result)['status_code'] == 200
            assert json.loads(result)['response'] == 'success'

    def test_api_call_host_without_protocol(self):
        """Test the _make_api_call() function with a host without a protocol."""
        with requests_mock.Mocker() as m:
            m.get('https://example.com/endpoint', text='success', status_code=200)
            result = _make_api_call('example.com', '/endpoint')
            assert json.loads(result)['status'] == 'success'
            assert json.loads(result)['status_code'] == 200
            assert json.loads(result)['response'] == 'success'

    def test_api_call_host_garbage(self):
        """Test the _make_api_call() function with a garbage host."""
        with pytest.raises(ValueError) as excinfo:
            _make_api_call('garbage', '/endpoint')
        assert "Invalid URL" in str(excinfo.value)

    def test_api_call_host_empty(self):
        """Test the _make_api_call() function with an empty host."""
        with pytest.raises(ValueError) as excinfo:
            _make_api_call('', '/endpoint')
        assert "Invalid URL" in str(excinfo.value)

    def test_api_call_host_number(self):
        """Test the _make_api_call() function with a host that is a number."""
        with pytest.raises(ValueError) as excinfo:
            _make_api_call(123, '/endpoint')
        assert "host must be a string" in str(excinfo.value)

    def test_api_call_host_none(self):
        """Test the _make_api_call() function with no host."""
        with pytest.raises(ValueError) as excinfo:
            _make_api_call(None, '/endpoint')
        assert "host must be a string" in str(excinfo.value)

    def test_api_call_host_invalid_protocol(self):
        """Test the _make_api_call() function with an invalid protocol."""
        with pytest.raises(ValueError) as excinfo:
            _make_api_call('ftp://example.com', '/endpoint')
        assert "Invalid URL" in str(excinfo.value)

    def test_api_call_host_query_marker(self):
        """Test the _make_api_call() function with dangerous characters."""
        with pytest.raises(ValueError) as excinfo:
            _make_api_call('http://example.com?test=1', '/endpoint')
        assert "Invalid URL" in str(excinfo.value)

    def test_api_call_host_query_param_marker(self):
        """Test the _make_api_call() function with dangerous characters."""
        with pytest.raises(ValueError) as excinfo:
            _make_api_call('http://example.com?test=1', '/endpoint')
        assert "Invalid URL" in str(excinfo.value)

    # Test endpoint errors

    def test_api_call_valid_endpoint(self):
        """Test the _make_api_call() function with a valid endpoint."""
        with requests_mock.Mocker() as m:
            m.get('http://example.com/endpoint', text='success', status_code=200)
            result = _make_api_call('http://example.com', '/endpoint')
            assert json.loads(result)['status'] == 'success'
            assert json.loads(result)['status_code'] == 200
            assert json.loads(result)['response'] == 'success'

    def test_api_call_valid_endpoint_with_query(self):
        """Test the _make_api_call() function with a valid endpoint."""
        with requests_mock.Mocker() as m:
            m.get('http://example.com/endpoint?test=1', text='success', status_code=200)
            result = _make_api_call('http://example.com', '/endpoint?test=1')
            assert json.loads(result)['status'] == 'success'
            assert json.loads(result)['status_code'] == 200
            assert json.loads(result)['response'] == 'success'

    def test_api_call_endpoint_empty(self):
        """Test the _make_api_call() function with an empty endpoint."""
        with requests_mock.Mocker() as m:
            m.get('http://example.com', text='success', status_code=200)
            result = _make_api_call('http://example.com', '')
            assert json.loads(result)['status'] == 'success'
            assert json.loads(result)['status_code'] == 200
            assert json.loads(result)['response'] == 'success'

    def test_api_call_endpoint_number(self):
        """Test the _make_api_call() function with an endpoint that is a number."""
        with pytest.raises(ValueError) as excinfo:
            _make_api_call('http://example.com', 123)
        assert "endpoint must be a string" in str(excinfo.value)

    def test_api_call_endpoint_none(self):
        """Test the _make_api_call() function with no endpoint."""
        with pytest.raises(ValueError) as excinfo:
            _make_api_call('http://example.com', None)
        assert "endpoint must be a string" in str(excinfo.value)

    # Test method errors    

    def test_api_call_invalid_method(self):
        """Test the _make_api_call() function with an invalid method."""
        with pytest.raises(ValueError) as excinfo:
            _make_api_call('http://example.com', '/endpoint', method='INVALID')
        assert "Invalid method: INVALID" in str(excinfo.value)          

    def test_api_call_none_method(self):
        """Test the _make_api_call() function with no method."""
        with pytest.raises(ValueError) as excinfo:
            _make_api_call('http://example.com', '/endpoint', method=None)
        assert "method must be a string" in str(excinfo.value)

    def test_api_call_empty_method(self):
        """Test the _make_api_call() function with an empty method."""
        with pytest.raises(ValueError) as excinfo:
            _make_api_call('http://example.com', '/endpoint', method='')
        assert "Invalid method" in str(excinfo.value)

    def test_api_call_number_method(self):
        """Test the _make_api_call() function with a number as a method."""
        with pytest.raises(ValueError) as excinfo:
            _make_api_call('http://example.com', '/endpoint', method=123)
        assert "method must be a string" in str(excinfo.value)

    def test_api_call_lowercase_method(self):
        """Test the _make_api_call() function with a lowercase method."""
        with requests_mock.Mocker() as m:
            m.get('http://example.com/endpoint', text='success', status_code=200)
            result = _make_api_call('http://example.com', '/endpoint', method='get')
            assert json.loads(result)['status'] == 'success'
            assert json.loads(result)['status_code'] == 200
            assert json.loads(result)['response'] == 'success'

    # Test query_params errors

    def test_api_call_valid_query_params_with_number_as_dict_value(self):
        """Test the _make_api_call() function with valid query_params."""
        with requests_mock.Mocker() as m:
            m.get('http://example.com/endpoint', text='success', status_code=200)
            result = _make_api_call('http://example.com', '/endpoint', query_params={'test': 1})
            assert json.loads(result)['status'] == 'success'
            assert json.loads(result)['status_code'] == 200
            assert json.loads(result)['response'] == 'success'

    def test_api_call_query_params_array(self):
        """Test the _make_api_call() function with query_params that is an array."""
        with pytest.raises(ValueError) as excinfo:
            _make_api_call('http://example.com', '/endpoint', query_params=['test'])
        assert "query_params must be a dictionary" in str(excinfo.value)

    def test_api_call_query_params_string(self):
        """Test the _make_api_call() function with query_params that is a string."""
        # This is interpreted as JSON and converted to a dictionary
        with requests_mock.Mocker() as m:
            m.get('http://example.com/endpoint', text='success', status_code=200)
            result = _make_api_call('http://example.com', '/endpoint', query_params='{"test": 1}')
            assert json.loads(result)['status'] == 'success'
            assert json.loads(result)['status_code'] == 200
            assert json.loads(result)['response'] == 'success'

    def test_api_call_query_params_invalid_json_string(self):
        """Test the _make_api_call() function with query_params that is an invalid JSON string."""
        with pytest.raises(ValueError) as excinfo:
            _make_api_call('http://example.com', '/endpoint', query_params='{test": 1')
        assert "query_params must be a dictionary" in str(excinfo.value)

    def test_api_call_query_params_number(self):
        """Test the _make_api_call() function with query_params that is a number."""
        with pytest.raises(ValueError) as excinfo:
            _make_api_call('http://example.com', '/endpoint', query_params=123)
        assert "query_params must be a dictionary" in str(excinfo.value)

    def test_api_call_query_params_empty_string(self):
        """Test the _make_api_call() function with query_params that is an empty string."""
        # This should be converted to an empty dictionary
        with requests_mock.Mocker() as m:
            m.get('http://example.com/endpoint', text='success', status_code=200)
            result = _make_api_call('http://example.com', '/endpoint', query_params='')
            assert json.loads(result)['status'] == 'success'
            assert json.loads(result)['status_code'] == 200
            assert json.loads(result)['response'] == 'success'

    def test_api_call_query_params_none(self):
        """Test the _make_api_call() function with no query_params."""
        # This should be converted to an empty dictionary
        with requests_mock.Mocker() as m:
            m.get('http://example.com/endpoint', text='success', status_code=200)
            result = _make_api_call('http://example.com', '/endpoint', query_params=None)
            assert json.loads(result)['status'] == 'success'
            assert json.loads(result)['status_code'] == 200
            assert json.loads(result)['response'] == 'success'

    def test_api_call_query_params_empty_dict(self):
        """Test the _make_api_call() function with an empty query_params."""
        with requests_mock.Mocker() as m:
            m.get('http://example.com/endpoint', text='success', status_code=200)
            result = _make_api_call('http://example.com', '/endpoint', query_params={})
            assert json.loads(result)['status'] == 'success'
            assert json.loads(result)['status_code'] == 200
            assert json.loads(result)['response'] == 'success'

    def test_api_call_query_params_number(self):
        """Test the _make_api_call() function with query_params that is a number."""
        with pytest.raises(ValueError) as excinfo:
            _make_api_call('http://example.com', '/endpoint', query_params=123)
        assert "query_params must be a dictionary" in str(excinfo.value)

    def test_api_call_query_params_dict_has_key_none_value(self):
        """Test the _make_api_call() function with query_params that has a None value."""
        with requests_mock.Mocker() as m:
            m.get('http://example.com/endpoint', text='success', status_code=200)
            result = _make_api_call('http://example.com', '/endpoint', query_params={'test': None})
            assert json.loads(result)['status'] == 'success'
            assert json.loads(result)['status_code'] == 200
            assert json.loads(result)['response'] == 'success'

    def test_api_call_query_params_dict_malformed(self):
        """Test the _make_api_call() function with query_params that is a malformed dictionary."""
        with pytest.raises(ValueError) as excinfo:
            _make_api_call('http://example.com', '/endpoint', query_params={None: 'test'})
        assert "query_params cannot contain None keys" in str(excinfo.value)

    # Test body errors

    def test_api_call_valid_body_with_24k_text(self):
        """Test the _make_api_call() function with valid body."""
        with requests_mock.Mocker() as m:
            m.post('http://example.com/endpoint', text='success', status_code=200)
            result = _make_api_call('http://example.com', '/endpoint', method='POST', body='a' * 24000)
            assert json.loads(result)['status'] == 'success'
            assert json.loads(result)['status_code'] == 200
            assert json.loads(result)['response'] == 'success'

    def test_api_calll_valid_body_with_random_text(self):
        """Test the _make_api_call() function with valid body."""
        with requests_mock.Mocker() as m:
            m.post('http://example.com/endpoint', text='success', status_code=200)
            result = _make_api_call('http://example.com', '/endpoint', method="POST", body='a' * random.randint(1, 24000))
            assert json.loads(result)['status'] == 'success'
            assert json.loads(result)['status_code'] == 200
            assert json.loads(result)['response'] == 'success'

    def test_api_call_valid_body_with_control_code_text(self):
        """Test the _make_api_call() function with valid body."""
        with requests_mock.Mocker() as m:
            m.post('http://example.com/endpoint', text='success', status_code=200)
            result = _make_api_call('http://example.com', '/endpoint', method="POST", body='\x00')
            assert json.loads(result)['status'] == 'success'
            assert json.loads(result)['status_code'] == 200
            assert json.loads(result)['response'] == 'success'

    def test_api_call_valid_body_with_unicode_text(self):
        """Test the _make_api_call() function with valid body."""
        with requests_mock.Mocker() as m:
            m.post('http://example.com/endpoint', text='success', status_code=200)
            result = _make_api_call('http://example.com', '/endpoint', method="POST", body=u'\u2713')
            assert json.loads(result)['status'] == 'success'
            assert json.loads(result)['status_code'] == 200
            assert json.loads(result)['response'] == 'success'

    def test_api_call_valid_body_with_utf8_text(self):
        """Test the _make_api_call() function with valid body."""
        with requests_mock.Mocker() as m:
            m.post('http://example.com/endpoint', text='success', status_code=200)
            result = _make_api_call('http://example.com', '/endpoint', method="POST", body=u'\u2713'.encode('utf-8'))
            assert json.loads(result)['status'] == 'success'
            assert json.loads(result)['status_code'] == 200
            assert json.loads(result)['response'] == 'success'

    def test_api_call_valid_body_with_utf16_text(self):
        """Test the _make_api_call() function with valid body."""
        with requests_mock.Mocker() as m:
            m.post('http://example.com/endpoint', text='success', status_code=200)
            result = _make_api_call('http://example.com', '/endpoint', method="POST", 
                                    body=u'\u2713'.encode('utf-16'))
            assert json.loads(result)['status'] == 'success'
            assert json.loads(result)['status_code'] == 200
            assert json.loads(result)['response'] == 'success'

    def test_api_call_body_empty(self):
        """Test the _make_api_call() function with an empty body."""
        with requests_mock.Mocker() as m:
            m.post('http://example.com/endpoint', text='success', status_code=200)
            result = _make_api_call('http://example.com', '/endpoint', method="POST", body='')
            assert json.loads(result)['status'] == 'success'
            assert json.loads(result)['status_code'] == 200

    def test_api_call_body_none(self):
        """Test the _make_api_call() function with a None body."""
        with requests_mock.Mocker() as m:
            m.post('http://example.com/endpoint', text='success', status_code=200)
            result = _make_api_call('http://example.com', '/endpoint', method="POST", body='')
            assert json.loads(result)['status'] == 'success'
            assert json.loads(result)['status_code'] == 200

    def test_api_call_body_not_string(self):
        """Test the _make_api_call() function with a body that is not a string."""
        with requests_mock.Mocker() as m:
            m.post('http://example.com/endpoint', text='success', status_code=200)
            result = _make_api_call('http://example.com', '/endpoint', method="POST", body=1)
            assert json.loads(result)['status'] == 'success'
            assert json.loads(result)['status_code'] == 200
            assert json.loads(result)['response'] == 'success'

    def test_api_call_body_json(self):
        """Test the _make_api_call() function with a body that is json."""
        with requests_mock.Mocker() as m:
            m.post('http://example.com/endpoint', text='success', status_code=200)
            result = _make_api_call('http://example.com', '/endpoint', method="POST", body=json.dumps({'test': 'test'}))
            assert json.loads(result)['status'] == 'success'
            assert json.loads(result)['status_code'] == 200
            assert json.loads(result)['response'] == 'success'

    def test_api_call_body_json_invalid(self):
        """Test the _make_api_call() function with a body that is invalid json."""
        with requests_mock.Mocker() as m:
            m.post('http://example.com/endpoint', text='success', status_code=200)
            result = _make_api_call('http://example.com', '/endpoint', method="POST", body='{"test": "test"]')
            assert json.loads(result)['status'] == 'success'
            assert json.loads(result)['status_code'] == 200
            assert json.loads(result)['response'] == 'success'

    def test_api_call_body_xml(self):
        """Test the _make_api_call() function with a body that is xml."""
        with requests_mock.Mocker() as m:
            m.post('http://example.com/endpoint', text='success', status_code=200)
            result = _make_api_call('http://example.com', '/endpoint', method="POST", body='<test>test</test>')
            assert json.loads(result)['status'] == 'success'
            assert json.loads(result)['status_code'] == 200
            assert json.loads(result)['response'] == 'success'

    def test_api_call_body_xml_invalid(self):
        """Test the _make_api_call() function with a body that is invalid xml."""
        with requests_mock.Mocker() as m:
            m.post('http://example.com/endpoint', text='success', status_code=200)
            result = _make_api_call('http://example.com', '/endpoint', method="POST", body='<test>test</test>')
            assert json.loads(result)['status'] == 'success'
            assert json.loads(result)['status_code'] == 200
            assert json.loads(result)['response'] == 'success'

    # Test headers errors

    def test_api_call_valid_headers(self):
        """Test the _make_api_call() function with valid headers."""
        with requests_mock.Mocker() as m:
            m.get('http://example.com/endpoint', text='success', status_code=200)
            result = _make_api_call('http://example.com', '/endpoint', headers={'test': 'test'})
            assert json.loads(result)['status'] == 'success'
            assert json.loads(result)['status_code'] == 200

    def test_api_call_valid_headers_with_random_text(self):
        """Test the _make_api_call() function with valid headers."""
        with requests_mock.Mocker() as m:
            m.get('http://example.com/endpoint', text='success', status_code=200)
            result = _make_api_call('http://example.com', '/endpoint', headers={'test': 'a' * random.randint(1, 24000)})
            assert json.loads(result)['status'] == 'success'
            assert json.loads(result)['status_code'] == 200

    def test_api_call_valid_headers_with_control_code_text(self):
        """Test the _make_api_call() function with valid headers."""
        with requests_mock.Mocker() as m:
            m.get('http://example.com/endpoint', text='success', status_code=200)
            result = _make_api_call('http://example.com', '/endpoint', headers={'test': '\x00'})
            assert json.loads(result)['status'] == 'success'
            assert json.loads(result)['status_code'] == 200

    def test_api_call_valid_headers_with_unicode_text(self):
        """Test the _make_api_call() function with valid headers."""
        with requests_mock.Mocker() as m:
            m.get('http://example.com/endpoint', text='success', status_code=200)
            result = _make_api_call('http://example.com', '/endpoint', headers={'test': u'\u2713'})
            assert json.loads(result)['status'] == 'success'
            assert json.loads(result)['status_code'] == 200

    def test_api_call_headers_with_array(self):
        """Test the _make_api_call() function with headers that are an array."""
        # This is not a valid header, and ValueError "headers must be a dictionary" will be thrown
        with pytest.raises(ValueError) as e:
            _make_api_call('http://example.com', '/endpoint', headers=['test'])
        assert "headers must be a dictionary" in str(e.value)

    def test_api_call_headers_with_empty_dict(self):
        """Test the _make_api_call() function with headers that are an empty dict."""
        with requests_mock.Mocker() as m:
            m.get('http://example.com/endpoint', text='success', status_code=200)
            result = _make_api_call('http://example.com', '/endpoint', headers={})
            assert json.loads(result)['status'] == 'success'
            assert json.loads(result)['status_code'] == 200

    def test_api_call_headers_with_none(self):
        """Test the _make_api_call() function with headers that are None."""
        with requests_mock.Mocker() as m:
            m.get('http://example.com/endpoint', text='success', status_code=200)
            result = _make_api_call('http://example.com', '/endpoint', headers=None)
            assert json.loads(result)['status'] == 'success'
            assert json.loads(result)['status_code'] == 200

    def test_api_call_headers_with_not_dict(self):
        """Test the _make_api_call() function with headers that are not a dict."""
        with pytest.raises(ValueError) as e:
            _make_api_call('http://example.com', '/endpoint', headers=1)
        assert "headers must be a dictionary" in str(e.value)

    def test_api_call_headers_with_invalid_key(self):
        """Test the _make_api_call() function with headers that have an invalid key."""
        headers = {'test': 'test'}
        headers[1] = 'test'
        with requests_mock.Mocker() as m:
            m.get('http://example.com/endpoint', text='success', status_code=200, request_headers={'test': 'test', '1': 'test'})
            result = _make_api_call('http://example.com', '/endpoint', headers=headers)
            assert json.loads(result)['status'] == 'success'
            assert json.loads(result)['status_code'] == 200
            assert json.loads(result)['response'] == 'success'

    def test_api_call_headers_with_invalid_value(self):
        """Test the _make_api_call() function with headers that have an invalid value."""
        headers = {'test': 'test'}
        headers['test'] = 1
        with requests_mock.Mocker() as m:
            m.get('http://example.com/endpoint', text='success', status_code=200, request_headers={'test': '1'})
            result = _make_api_call('http://example.com', '/endpoint', headers=headers)
            assert json.loads(result)['status'] == 'success'
            assert json.loads(result)['status_code'] == 200
            assert json.loads(result)['response'] == 'success'

    # Test timeout_secs errors

    def test_api_call_valid_timeout_secs(self):
        """Test the _make_api_call() function with valid timeout_secs."""
        with requests_mock.Mocker() as m:
            m.get('http://example.com/endpoint', text='success', status_code=200)
            result = _make_api_call('http://example.com', '/endpoint', timeout_secs=1)
            assert json.loads(result)['status'] == 'success'
            assert json.loads(result)['status_code'] == 200

    def test_api_call_timeout_secs_with_string(self):
        """Test the _make_api_call() function with timeout_secs that is a string."""
        # The string will be converted to an integer, so no error will be thrown
        with requests_mock.Mocker() as m:
            m.get('http://example.com/endpoint', text='success', status_code=200)
            result = _make_api_call('http://example.com', '/endpoint', timeout_secs='1')
            assert json.loads(result)['status'] == 'success'
            assert json.loads(result)['status_code'] == 200

    def test_api_call_timeout_secs_with_float(self):
        """Test the _make_api_call() function with timeout_secs that is a float."""
        # The float will be converted to an integer, so no error will be thrown
        with requests_mock.Mocker() as m:
            m.get('http://example.com/endpoint', text='success', status_code=200)
            result = _make_api_call('http://example.com', '/endpoint', timeout_secs=1.0)
            assert json.loads(result)['status'] == 'success'
            assert json.loads(result)['status_code'] == 200

    def test_api_call_timeout_secs_with_negative_number(self):
        """Test the _make_api_call() function with timeout_secs that is a negative number."""
        with pytest.raises(ValueError) as e:
            _make_api_call('http://example.com', '/endpoint', timeout_secs=-1)
        assert "timeout_secs must be a positive integer" in str(e.value)

    def test_api_call_timeout_secs_with_zero(self):
        """Test the _make_api_call() function with timeout_secs that is zero."""
        with pytest.raises(ValueError) as e:
            _make_api_call('http://example.com', '/endpoint', timeout_secs=0)
        assert "timeout_secs must be a positive integer" in str(e.value)

    def test_api_call_timeout_secs_with_empty_string(self):
        """Test the _make_api_call() function with timeout_secs that is an empty string."""
        with pytest.raises(ValueError) as e:
            _make_api_call('http://example.com', '/endpoint', timeout_secs='')
        assert "timeout_secs must be an integer" in str(e.value)

    def test_api_call_timeout_secs_with_none_value(self):
        """Test the _make_api_call() function with timeout_secs that is None."""
        with pytest.raises(ValueError) as e:
            _make_api_call('http://example.com', '/endpoint', timeout_secs=None)
        assert "timeout_secs must be an integer" in str(e.value)

    def test_api_call_timeout_secs_with_random_text(self):
        """Test the _make_api_call() function with timeout_secs that is random text."""
        with pytest.raises(ValueError) as e:
            _make_api_call('http://example.com', '/endpoint', timeout_secs='test')
        assert "timeout_secs must be an integer" in str(e.value)

    def test_api_call_timeout_secs_with_control_code_text(self):
        """Test the _make_api_call() function with timeout_secs that is a control code."""
        with pytest.raises(ValueError) as e:
            _make_api_call('http://example.com', '/endpoint', timeout_secs='\x00')
        assert "timeout_secs must be an integer" in str(e.value)