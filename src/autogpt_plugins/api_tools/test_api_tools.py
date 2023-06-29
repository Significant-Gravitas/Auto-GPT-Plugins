import json
import random
import requests_mock
import unittest
try:
    from .api_tools import ApiCallCommand
except ImportError:
    from api_tools import ApiCallCommand

class TestAutoGPTAPITools(unittest.TestCase):

    def setUp(self):
        self.plugin_class = ApiCallCommand()

    def test_api_call_get(self):
        """Test the self.plugin_class.make_api_call() function with a GET request."""
        with requests_mock.Mocker() as m:
            m.get('http://example.com/endpoint', text='success', status_code=200)
            result = self.plugin_class.make_api_call('http://example.com', '/endpoint')
            response = json.loads(result)

            self.assertEqual(response['status'], 'success')
            self.assertEqual(response['status_code'], 200)
            self.assertEqual(response['response'], 'success')

    def test_api_call_post(self):
        """Test the self.plugin_class.make_api_call() function with a POST request."""
        with requests_mock.Mocker() as m:
            m.post('http://example.com/endpoint', text='success', status_code=200)
            result = self.plugin_class.make_api_call('http://example.com', '/endpoint', mthd='POST')
            response = json.loads(result)

            self.assertEqual(response['status'], 'success')
            self.assertEqual(response['status_code'], 200)
            self.assertEqual(response['response'], 'success')

    def test_api_call_put(self):
        """Test the self.plugin_class.make_api_call() function with a PUT request."""
        with requests_mock.Mocker() as m:
            m.put('http://example.com/endpoint', text='success', status_code=200)
            result = self.plugin_class.make_api_call('http://example.com', '/endpoint', mthd='PUT')
            response = json.loads(result)

            self.assertEqual(response['status'], 'success')
            self.assertEqual(response['status_code'], 200)
            self.assertEqual(response['response'], 'success')

    def test_api_call_delete(self):
        """Test the self.plugin_class.make_api_call() function with a DELETE request."""
        with requests_mock.Mocker() as m:
            m.delete('http://example.com/endpoint', text='success', status_code=200)
            result = self.plugin_class.make_api_call('http://example.com', '/endpoint', mthd='DELETE')
            response = json.loads(result)

            self.assertEqual(response['status'], 'success')
            self.assertEqual(response['status_code'], 200)
            self.assertEqual(response['response'], 'success')

    def test_api_call_patch(self):
        """Test the self.plugin_class.make_api_call() function with a PATCH request."""
        with requests_mock.Mocker() as m:
            m.patch('http://example.com/endpoint', text='success', status_code=200)
            result = self.plugin_class.make_api_call('http://example.com', '/endpoint', mthd='PATCH')
            response = json.loads(result)

            self.assertEqual(response['status'], 'success')
            self.assertEqual(response['status_code'], 200)
            self.assertEqual(response['response'], 'success')

    def test_api_call_head(self):
        """Test the self.plugin_class.make_api_call() function with a HEAD request."""
        with requests_mock.Mocker() as m:
            m.head('http://example.com/endpoint', text='success', status_code=200)
            result = self.plugin_class.make_api_call('http://example.com', '/endpoint', mthd='HEAD')
            response = json.loads(result)

            self.assertEqual(response['status'], 'success')
            self.assertEqual(response['status_code'], 200)
            self.assertEqual(response['response'], 'success')

    def test_api_call_options(self):
        """Test the self.plugin_class.make_api_call() function with a OPTIONS request."""
        with requests_mock.Mocker() as m:
            m.options('http://example.com/endpoint', text='success', status_code=200)
            result = self.plugin_class.make_api_call('http://example.com', '/endpoint', mthd='OPTIONS')
            response = json.loads(result)

            self.assertEqual(response['status'], 'success')
            self.assertEqual(response['status_code'], 200)
            self.assertEqual(response['response'], 'success')

    # Test host errors

    def test_api_call_valid_host(self):
        """Test the self.plugin_class.make_api_call() function with a valid host."""
        with requests_mock.Mocker() as m:
            m.get('http://example.com/endpoint', text='success', status_code=200)
            result = self.plugin_class.make_api_call('http://example.com', '/endpoint')
            response = json.loads(result)

            self.assertEqual(response['status'], 'success')
            self.assertEqual(response['status_code'], 200)
            self.assertEqual(response['response'], 'success')

    def test_api_call_valid_host_https(self):
        """Test the self.plugin_class.make_api_call() function with a valid host using HTTPS."""
        with requests_mock.Mocker() as m:
            m.get('https://example.com/endpoint', text='success', status_code=200)
            result = self.plugin_class.make_api_call('https://example.com', '/endpoint')
            response = json.loads(result)

            self.assertEqual(response['status'], 'success')
            self.assertEqual(response['status_code'], 200)
            self.assertEqual(response['response'], 'success')

    def test_api_call_host_without_protocol(self):
        """Test the self.plugin_class.make_api_call() function with a host without a protocol."""
        with requests_mock.Mocker() as m:
            m.get('https://example.com/endpoint', text='success', status_code=200)
            result = self.plugin_class.make_api_call('example.com', '/endpoint')
            response = json.loads(result)

            self.assertEqual(response['status'], 'success')
            self.assertEqual(response['status_code'], 200)
            self.assertEqual(response['response'], 'success')

    def test_api_call_host_garbage(self):
        """Test the self.plugin_class.make_api_call() function with a garbage host."""
        with self.assertRaises(ValueError) as excinfo:
            self.plugin_class.make_api_call('garbage', '/endpoint')
        self.assertIn("Invalid URL", str(excinfo.exception))

    def test_api_call_host_empty(self):
        """Test the self.plugin_class.make_api_call() function with an empty host."""
        with self.assertRaises(ValueError) as excinfo:
            self.plugin_class.make_api_call('', '/endpoint')
        self.assertIn("Invalid URL", str(excinfo.exception))

    def test_api_call_host_number(self):
        """Test the self.plugin_class.make_api_call() function with a host that is a number."""
        with self.assertRaises(ValueError) as excinfo:
            self.plugin_class.make_api_call(123, '/endpoint') # type: ignore
        self.assertIn("host must be a string", str(excinfo.exception))

    def test_api_call_host_none(self):
        """Test the self.plugin_class.make_api_call() function with no host."""
        with self.assertRaises(ValueError) as excinfo:
            self.plugin_class.make_api_call(None, '/endpoint') # type: ignore
        self.assertIn("host must be a string", str(excinfo.exception))

    def test_api_call_host_invalid_protocol(self):
        """Test the self.plugin_class.make_api_call() function with an invalid protocol."""
        with self.assertRaises(ValueError) as excinfo:
            self.plugin_class.make_api_call('ftp://example.com', '/endpoint')
        self.assertIn("Invalid URL", str(excinfo.exception))

    def test_api_call_host_query_marker(self):
        """Test the self.plugin_class.make_api_call() function with dangerous characters."""
        with self.assertRaises(ValueError) as excinfo:
            self.plugin_class.make_api_call('http://example.com?test=1', '/endpoint')
        self.assertIn("Invalid URL", str(excinfo.exception))

    def test_api_call_host_query_param_marker(self):
        """Test the self.plugin_class.make_api_call() function with dangerous characters."""
        with self.assertRaises(ValueError) as excinfo:
            self.plugin_class.make_api_call('http://example.com?test=1', '/endpoint')
        self.assertIn("Invalid URL", str(excinfo.exception))

    # Test endpoint errors

    def test_api_call_valid_endpoint(self):
        """Test the self.plugin_class.make_api_call() function with a valid endpoint."""
        with requests_mock.Mocker() as m:
            m.get('http://example.com/endpoint', text='success', status_code=200)
            result = self.plugin_class.make_api_call('http://example.com', '/endpoint')
            response = json.loads(result)

            self.assertEqual(response['status'], 'success')
            self.assertEqual(response['status_code'], 200)
            self.assertEqual(response['response'], 'success')

    def test_api_call_valid_endpoint_with_query(self):
        """Test the self.plugin_class.make_api_call() function with a valid endpoint."""
        with requests_mock.Mocker() as m:
            m.get('http://example.com/endpoint?test=1', text='success', status_code=200)
            result = self.plugin_class.make_api_call('http://example.com', '/endpoint?test=1')
            response = json.loads(result)

            self.assertEqual(response['status'], 'success')
            self.assertEqual(response['status_code'], 200)
            self.assertEqual(response['response'], 'success')

    def test_api_call_endpoint_empty(self):
        """Test the self.plugin_class.make_api_call() function with an empty endpoint."""
        with requests_mock.Mocker() as m:
            m.get('http://example.com', text='success', status_code=200)
            result = self.plugin_class.make_api_call('http://example.com', '')
            response = json.loads(result)

            self.assertEqual(response['status'], 'success')
            self.assertEqual(response['status_code'], 200)
            self.assertEqual(response['response'], 'success')

    def test_api_call_endpoint_number(self):
        """Test the self.plugin_class.make_api_call() function with an endpoint that is a number."""
        with self.assertRaises(ValueError) as excinfo:
            self.plugin_class.make_api_call('http://example.com', 123) # type: ignore
        self.assertIn("endpoint must be a string", str(excinfo.exception))

    def test_api_call_endpoint_none(self):
        """Test the self.plugin_class.make_api_call() function with no endpoint."""
        with self.assertRaises(ValueError) as excinfo:
            self.plugin_class.make_api_call('http://example.com', None) # type: ignore
        self.assertIn("endpoint must be a string", str(excinfo.exception))

    # Test method errors    

    def test_api_call_invalid_method(self):
        """Test the self.plugin_class.make_api_call() function with an invalid method."""
        with self.assertRaises(ValueError) as excinfo:
            self.plugin_class.make_api_call('http://example.com', '/endpoint', mthd='INVALID')
        self.assertIn("Invalid method: INVALID", str(excinfo.exception))

    def test_api_call_none_method(self):
        """Test the self.plugin_class.make_api_call() function with no method."""
        with self.assertRaises(ValueError) as excinfo:
            self.plugin_class.make_api_call('http://example.com', '/endpoint', mthd=None) # type: ignore
        self.assertIn("method must be a string", str(excinfo.exception))

    def test_api_call_empty_method(self):
        """Test the self.plugin_class.make_api_call() function with an empty method."""
        with self.assertRaises(ValueError) as excinfo:
            self.plugin_class.make_api_call('http://example.com', '/endpoint', mthd='')
        self.assertIn("Invalid method", str(excinfo.exception))

    def test_api_call_number_method(self):
        """Test the self.plugin_class.make_api_call() function with a number as a method."""
        with self.assertRaises(ValueError) as excinfo:
            self.plugin_class.make_api_call('http://example.com', '/endpoint', mthd=123) # type: ignore
        self.assertIn("method must be a string", str(excinfo.exception))

    def test_api_call_lowercase_method(self):
        """Test the self.plugin_class.make_api_call() function with a lowercase method."""
        with requests_mock.Mocker() as m:
            m.get('http://example.com/endpoint', text='success', status_code=200)
            result = self.plugin_class.make_api_call('http://example.com', '/endpoint', mthd='get')
            response = json.loads(result)

            self.assertEqual(response['status'], 'success')
            self.assertEqual(response['status_code'], 200)
            self.assertEqual(response['response'], 'success')

    # Test query_params errors

    def test_api_call_valid_query_params_with_number_as_dict_value(self):
        """Test the self.plugin_class.make_api_call() function with valid query_params."""
        with requests_mock.Mocker() as m:
            m.get('http://example.com/endpoint', text='success', status_code=200)
            result = self.plugin_class.make_api_call('http://example.com', '/endpoint', params={'test': 1})
            response = json.loads(result)

            self.assertEqual(response['status'], 'success')
            self.assertEqual(response['status_code'], 200)
            self.assertEqual(response['response'], 'success')

    def test_api_call_query_params_array(self):
        """Test the self.plugin_class.make_api_call() function with query_params that is an array."""
        with self.assertRaises(ValueError) as excinfo:
            self.plugin_class.make_api_call('http://example.com', '/endpoint', params=['test'])
        self.assertIn("query_params must be a dictionary", str(excinfo.exception))

    def test_api_call_query_params_string(self):
        """Test the self.plugin_class.make_api_call() function with query_params that is a string."""
        # This is interpreted as JSON and converted to a dictionary
        with requests_mock.Mocker() as m:
            m.get('http://example.com/endpoint', text='success', status_code=200)
            result = self.plugin_class.make_api_call('http://example.com', '/endpoint', params='{"test": 1}')
            response = json.loads(result)

            self.assertEqual(response['status'], 'success')
            self.assertEqual(response['status_code'], 200)
            self.assertEqual(response['response'], 'success')

    def test_api_call_query_params_invalid_json_string(self):
        """Test the self.plugin_class.make_api_call() function with query_params that is an invalid JSON string."""
        with self.assertRaises(ValueError) as excinfo:
            self.plugin_class.make_api_call('http://example.com', '/endpoint', params='{test": 1')
        self.assertIn("query_params must be a dictionary", str(excinfo.exception))

    def test_api_call_query_params_empty_string(self):
        """Test the self.plugin_class.make_api_call() function with query_params that is an empty string."""
        # This should be converted to an empty dictionary
        with requests_mock.Mocker() as m:
            m.get('http://example.com/endpoint', text='success', status_code=200)
            result = self.plugin_class.make_api_call('http://example.com', '/endpoint', params='')
            response = json.loads(result)

            self.assertEqual(response['status'], 'success')
            self.assertEqual(response['status_code'], 200)
            self.assertEqual(response['response'], 'success')

    def test_api_call_query_params_none(self):
        """Test the self.plugin_class.make_api_call() function with no query_params."""
        # This should be converted to an empty dictionary
        with requests_mock.Mocker() as m:
            m.get('http://example.com/endpoint', text='success', status_code=200)
            result = self.plugin_class.make_api_call('http://example.com', '/endpoint', params=None)
            response = json.loads(result)

            self.assertEqual(response['status'], 'success')
            self.assertEqual(response['status_code'], 200)
            self.assertEqual(response['response'], 'success')

    def test_api_call_query_params_empty_dict(self):
        """Test the self.plugin_class.make_api_call() function with an empty query_params."""
        with requests_mock.Mocker() as m:
            m.get('http://example.com/endpoint', text='success', status_code=200)
            result = self.plugin_class.make_api_call('http://example.com', '/endpoint', params={})
            response = json.loads(result)

            self.assertEqual(response['status'], 'success')
            self.assertEqual(response['status_code'], 200)
            self.assertEqual(response['response'], 'success')

    def test_api_call_query_params_number(self):
        """Test the self.plugin_class.make_api_call() function with query_params that is a number."""
        with self.assertRaises(ValueError) as excinfo:
            self.plugin_class.make_api_call('http://example.com', '/endpoint', params=123)
        self.assertIn("query_params must be a dictionary", str(excinfo.exception))

    def test_api_call_query_params_dict_has_key_none_value(self):
        """Test the self.plugin_class.make_api_call() function with query_params that has a None value."""
        with requests_mock.Mocker() as m:
            m.get('http://example.com/endpoint', text='success', status_code=200)
            result = self.plugin_class.make_api_call('http://example.com', '/endpoint', params={'test': None})
            response = json.loads(result)

            self.assertEqual(response['status'], 'success')
            self.assertEqual(response['status_code'], 200)
            self.assertEqual(response['response'], 'success')

    def test_api_call_query_params_dict_malformed(self):
        """Test the self.plugin_class.make_api_call() function with query_params that is a malformed dictionary."""
        with self.assertRaises(ValueError) as excinfo:
            self.plugin_class.make_api_call('http://example.com', '/endpoint', params={None: 'test'})
        self.assertIn("query_params cannot contain None keys", str(excinfo.exception))

    # Test body errors

    def test_api_call_valid_body_with_24k_text(self):
        """Test the self.plugin_class.make_api_call() function with valid body."""
        with requests_mock.Mocker() as m:
            m.post('http://example.com/endpoint', text='success', status_code=200)
            result = self.plugin_class.make_api_call('http://example.com', '/endpoint', mthd='POST', body='a' * 24000)
            response = json.loads(result)

            self.assertEqual(response['status'], 'success')
            self.assertEqual(response['status_code'], 200)
            self.assertEqual(response['response'], 'success')

    def test_api_call_valid_body_with_random_text(self):
        """Test the self.plugin_class.make_api_call() function with valid body."""
        with requests_mock.Mocker() as m:
            m.post('http://example.com/endpoint', text='success', status_code=200)
            body_length = random.randint(1, 24000)
            body = 'a' * body_length
            result = self.plugin_class.make_api_call('http://example.com', '/endpoint', mthd='POST', body=body)
            response = json.loads(result)

            self.assertEqual(response['status'], 'success')
            self.assertEqual(response['status_code'], 200)
            self.assertEqual(response['response'], 'success')

    def test_api_call_valid_body_with_control_code_text(self):
        """Test the self.plugin_class.make_api_call() function with valid body."""
        with requests_mock.Mocker() as m:
            m.post('http://example.com/endpoint', text='success', status_code=200)
            result = self.plugin_class.make_api_call('http://example.com', '/endpoint', mthd='POST', body='\x00')
            response = json.loads(result)

            self.assertEqual(response['status'], 'success')
            self.assertEqual(response['status_code'], 200)
            self.assertEqual(response['response'], 'success')

    def test_api_call_valid_body_with_unicode_text(self):
        """Test the self.plugin_class.make_api_call() function with valid body."""
        with requests_mock.Mocker() as m:
            m.post('http://example.com/endpoint', text='success', status_code=200)
            result = self.plugin_class.make_api_call('http://example.com', '/endpoint', mthd='POST', body=u'\u2713')
            response = json.loads(result)

            self.assertEqual(response['status'], 'success')
            self.assertEqual(response['status_code'], 200)
            self.assertEqual(response['response'], 'success')

    def test_api_call_valid_body_with_utf8_text(self):
        """Test the self.plugin_class.make_api_call() function with valid body."""
        with requests_mock.Mocker() as m:
            m.post('http://example.com/endpoint', text='success', status_code=200)
            body = u'\u2713'.encode('utf-8')
            result = self.plugin_class.make_api_call('http://example.com', '/endpoint', mthd='POST', body=body) # type: ignore
            response = json.loads(result)

            self.assertEqual(response['status'], 'success')
            self.assertEqual(response['status_code'], 200)
            self.assertEqual(response['response'], 'success')

    def test_api_call_valid_body_with_utf16_text(self):
        """Test the self.plugin_class.make_api_call() function with valid body."""
        with requests_mock.Mocker() as m:
            m.post('http://example.com/endpoint', text='success', status_code=200)
            body = u'\u2713'.encode('utf-16')
            result = self.plugin_class.make_api_call('http://example.com', '/endpoint', mthd='POST', body=body) # type: ignore
            response = json.loads(result)

            self.assertEqual(response['status'], 'success')
            self.assertEqual(response['status_code'], 200)
            self.assertEqual(response['response'], 'success')

    def test_api_call_body_empty(self):
        """Test the self.plugin_class.make_api_call() function with an empty body."""
        with requests_mock.Mocker() as m:
            m.post('http://example.com/endpoint', text='success', status_code=200)
            result = self.plugin_class.make_api_call('http://example.com', '/endpoint', mthd='POST', body='')
            response = json.loads(result)

            self.assertEqual(response['status'], 'success')
            self.assertEqual(response['status_code'], 200)

    def test_api_call_body_none(self):
        """Test the self.plugin_class.make_api_call() function with a None body."""
        with requests_mock.Mocker() as m:
            m.post('http://example.com/endpoint', text='success', status_code=200)
            result = self.plugin_class.make_api_call('http://example.com', '/endpoint', mthd='POST', body=None) # type: ignore
            response = json.loads(result)

            self.assertEqual(response['status'], 'success')
            self.assertEqual(response['status_code'], 200)

    def test_api_call_body_not_string(self):
        """Test the self.plugin_class.make_api_call() function with a body that is not a string."""
        with requests_mock.Mocker() as m:
            m.post('http://example.com/endpoint', text='success', status_code=200)
            result = self.plugin_class.make_api_call('http://example.com', '/endpoint', mthd='POST', body=1) # type: ignore
            response = json.loads(result)

            self.assertEqual(response['status'], 'success')
            self.assertEqual(response['status_code'], 200)
            self.assertEqual(response['response'], 'success')

    def test_api_call_body_json(self):
        """Test the self.plugin_class.make_api_call() function with a body that is json."""
        with requests_mock.Mocker() as m:
            m.post('http://example.com/endpoint', text='success', status_code=200)
            body = json.dumps({'test': 'test'})
            result = self.plugin_class.make_api_call('http://example.com', '/endpoint', mthd='POST', body=body)
            response = json.loads(result)

            self.assertEqual(response['status'], 'success')
            self.assertEqual(response['status_code'], 200)
            self.assertEqual(response['response'], 'success')

    def test_api_call_body_json_invalid(self):
        """Test the self.plugin_class.make_api_call() function with a body that is invalid json."""
        with requests_mock.Mocker() as m:
            m.post('http://example.com/endpoint', text='success', status_code=200)
            body = '{"test": "test"]'
            result = self.plugin_class.make_api_call('http://example.com', '/endpoint', mthd='POST', body=body)
            response = json.loads(result)

            self.assertEqual(response['status'], 'success')
            self.assertEqual(response['status_code'], 200)
            self.assertEqual(response['response'], 'success')

    def test_api_call_body_xml(self):
        """Test the self.plugin_class.make_api_call() function with a body that is xml."""
        with requests_mock.Mocker() as m:
            m.post('http://example.com/endpoint', text='success', status_code=200)
            body = '<test>test</test>'
            result = self.plugin_class.make_api_call('http://example.com', '/endpoint', mthd='POST', body=body)
            response = json.loads(result)

            self.assertEqual(response['status'], 'success')
            self.assertEqual(response['status_code'], 200)
            self.assertEqual(response['response'], 'success')

    def test_api_call_body_xml_invalid(self):
        """Test the self.plugin_class.make_api_call() function with a body that is invalid xml."""
        with requests_mock.Mocker() as m:
            m.post('http://example.com/endpoint', text='success', status_code=200)
            result = self.plugin_class.make_api_call('http://example.com', '/endpoint', mthd='POST', body='<test>test</test>')
            response = json.loads(result)

            self.assertEqual(response['status'], 'success')
            self.assertEqual(response['status_code'], 200)
            self.assertEqual(response['response'], 'success')

    # Test headers errors

    def test_api_call_valid_headers(self):
        """Test the self.plugin_class.make_api_call() function with valid headers."""
        with requests_mock.Mocker() as m:
            m.get('http://example.com/endpoint', text='success', status_code=200)
            result = self.plugin_class.make_api_call('http://example.com', '/endpoint', hdrs={'test': 'test'})
            response = json.loads(result)

            self.assertEqual(response['status'], 'success')
            self.assertEqual(response['status_code'], 200)

    def test_api_call_valid_headers_with_random_text(self):
        """Test the self.plugin_class.make_api_call() function with valid headers."""
        with requests_mock.Mocker() as m:
            m.get('http://example.com/endpoint', text='success', status_code=200)
            headers = {'test': 'a' * random.randint(1, 24000)}
            result = self.plugin_class.make_api_call('http://example.com', '/endpoint', hdrs=headers)
            response = json.loads(result)

            self.assertEqual(response['status'], 'success')
            self.assertEqual(response['status_code'], 200)

    def test_api_call_valid_headers_with_control_code_text(self):
        """Test the self.plugin_class.make_api_call() function with valid headers."""
        with requests_mock.Mocker() as m:
            m.get('http://example.com/endpoint', text='success', status_code=200)
            headers = {'test': '\x00'}
            result = self.plugin_class.make_api_call('http://example.com', '/endpoint', hdrs=headers)
            response = json.loads(result)

            self.assertEqual(response['status'], 'success')
            self.assertEqual(response['status_code'], 200)

    def test_api_call_valid_headers_with_unicode_text(self):
        """Test the self.plugin_class.make_api_call() function with valid headers."""
        with requests_mock.Mocker() as m:
            m.get('http://example.com/endpoint', text='success', status_code=200)
            headers = {'test': u'\u2713'}
            result = self.plugin_class.make_api_call('http://example.com', '/endpoint', hdrs=headers)
            response = json.loads(result)

            self.assertEqual(response['status'], 'success')
            self.assertEqual(response['status_code'], 200)

    def test_api_call_headers_with_array(self):
        """Test the self.plugin_class.make_api_call() function with headers that are an array."""
        with self.assertRaises(ValueError) as excinfo:
            headers = ['test']
            self.plugin_class.make_api_call('http://example.com', '/endpoint', hdrs=headers)
        self.assertIn("headers must be a dictionary", str(excinfo.exception))

    def test_api_call_headers_with_empty_dict(self):
        """Test the self.plugin_class.make_api_call() function with headers that are an empty dict."""
        with requests_mock.Mocker() as m:
            m.get('http://example.com/endpoint', text='success', status_code=200)
            result = self.plugin_class.make_api_call('http://example.com', '/endpoint', hdrs={})
            response = json.loads(result)

            self.assertEqual(response['status'], 'success')
            self.assertEqual(response['status_code'], 200)

    def test_api_call_headers_with_none(self):
        """Test the self.plugin_class.make_api_call() function with headers that are None."""
        with requests_mock.Mocker() as m:
            m.get('http://example.com/endpoint', text='success', status_code=200)
            result = self.plugin_class.make_api_call('http://example.com', '/endpoint', hdrs=None)
            response = json.loads(result)

            self.assertEqual(response['status'], 'success')
            self.assertEqual(response['status_code'], 200)

    def test_api_call_headers_with_not_dict(self):
        """Test the self.plugin_class.make_api_call() function with headers that are not a dict."""
        with self.assertRaises(ValueError) as excinfo:
            self.plugin_class.make_api_call('http://example.com', '/endpoint', hdrs=1)
        self.assertIn("headers must be a dictionary", str(excinfo.exception))

    def test_api_call_headers_with_invalid_key(self):
        """Test the self.plugin_class.make_api_call() function with headers that have an invalid key."""
        headers = {'test': 'test'}
        headers[1] = 'test' # type: ignore
        with requests_mock.Mocker() as m:
            m.get('http://example.com/endpoint', text='success', status_code=200, headers={'test': 'test', '1': 'test'})
            result = self.plugin_class.make_api_call(host='http://example.com', endpoint='/endpoint', hdrs=headers)
            response = json.loads(result)

            self.assertEqual(response['status'], 'success')
            self.assertEqual(response['status_code'], 200)
            self.assertEqual(response['response'], 'success')

    def test_api_call_headers_with_invalid_value(self):
        """Test the self.plugin_class.make_api_call() function with headers that have an invalid value."""
        headers = {'test': 'test'}
        headers['test'] = 1 # type: ignore
        with requests_mock.Mocker() as m:
            m.get('http://example.com/endpoint', text='success', status_code=200, headers={'test': '1'})
            result = self.plugin_class.make_api_call(host='http://example.com', endpoint='/endpoint', hdrs=headers)
            response = json.loads(result)

            self.assertEqual(response['status'], 'success')
            self.assertEqual(response['status_code'], 200)
            self.assertEqual(response['response'], 'success')

    # Test timeout_secs errors

    def test_api_call_valid_timeout_secs(self):
        """Test the self.plugin_class.make_api_call() function with valid timeout_secs."""
        with requests_mock.Mocker() as m:
            m.get('http://example.com/endpoint', text='success', status_code=200)
            result = self.plugin_class.make_api_call('http://example.com', '/endpoint', timeout=1)
            response = json.loads(result)

            self.assertEqual(response['status'], 'success')
            self.assertEqual(response['status_code'], 200)

    def test_api_call_timeout_secs_with_string(self):
        """Test the self.plugin_class.make_api_call() function with timeout_secs that is a string."""
        # The string will be converted to an integer, so no error will be thrown
        with requests_mock.Mocker() as m:
            m.get('http://example.com/endpoint', text='success', status_code=200)
            result = self.plugin_class.make_api_call('http://example.com', '/endpoint', timeout='1') # type: ignore
            response = json.loads(result)

            self.assertEqual(response['status'], 'success')
            self.assertEqual(response['status_code'], 200)

    def test_api_call_timeout_secs_with_float(self):
        """Test the self.plugin_class.make_api_call() function with timeout_secs that is a float."""
        # The float will be converted to an integer, so no error will be thrown
        with requests_mock.Mocker() as m:
            m.get('http://example.com/endpoint', text='success', status_code=200)
            result = self.plugin_class.make_api_call('http://example.com', '/endpoint', timeout=1.0) # type: ignore
            response = json.loads(result)

            self.assertEqual(response['status'], 'success')
            self.assertEqual(response['status_code'], 200)

    def test_api_call_timeout_secs_with_negative_number(self):
        """Test the self.plugin_class.make_api_call() function with timeout_secs that is a negative number."""
        with self.assertRaises(ValueError) as excinfo:
            self.plugin_class.make_api_call('http://example.com', '/endpoint', timeout=-1)
        self.assertIn("timeout_secs must be a positive integer", str(excinfo.exception))

    def test_api_call_timeout_secs_with_zero(self):
        """Test the self.plugin_class.make_api_call() function with timeout_secs that is zero."""
        with self.assertRaises(ValueError) as excinfo:
            self.plugin_class.make_api_call('http://example.com', '/endpoint', timeout=0)
        self.assertIn("timeout_secs must be a positive integer", str(excinfo.exception))

    def test_api_call_timeout_secs_with_empty_string(self):
        """Test the self.plugin_class.make_api_call() function with timeout_secs that is an empty string."""
        with self.assertRaises(ValueError) as excinfo:
            self.plugin_class.make_api_call('http://example.com', '/endpoint', timeout='') # type: ignore
        self.assertIn("timeout_secs must be an integer", str(excinfo.exception))

    def test_api_call_timeout_secs_with_none_value(self):
        """Test the self.plugin_class.make_api_call() function with timeout_secs that is None."""
        with self.assertRaises(ValueError) as excinfo:
            self.plugin_class.make_api_call('http://example.com', '/endpoint', timeout=None) # type: ignore
        self.assertIn("timeout_secs must be an integer", str(excinfo.exception))

    def test_api_call_timeout_secs_with_random_text(self):
        """Test the self.plugin_class.make_api_call() function with timeout_secs that is random text."""
        with self.assertRaises(ValueError) as excinfo:
            self.plugin_class.make_api_call('http://example.com', '/endpoint', timeout='test') # type: ignore
        self.assertIn("timeout_secs must be an integer", str(excinfo.exception))

    def test_api_call_timeout_secs_with_control_code_text(self):
        """Test the self.plugin_class.make_api_call() function with timeout_secs that is a control code."""
        with self.assertRaises(ValueError) as excinfo:
            self.plugin_class.make_api_call('http://example.com', '/endpoint', timeout='\x00') # type: ignore
        self.assertIn("timeout_secs must be an integer", str(excinfo.exception))
