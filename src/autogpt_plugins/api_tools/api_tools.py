"""API Call command for Autogpt."""

import json
import requests
import re

from typing import Optional, Dict
from urllib.parse import urlparse
from urllib.parse import urljoin

def _make_api_call(
        host: str = "https://localhost", 
        endpoint: str = "/", 
        method: str = "GET", 
        query_params = {},
        body: str = "", 
        headers = {},
        timeout_secs: int = 120) -> str:
    """Return the results of an API call
    Args:
        host (str): The host of the API.
        endpoint (str): The endpoint of the API.
        method (str): The method of the API.
        query_params (dict): The query parameters of the API.
        body (str): The body of the API.
        headers (dict): The headers of the API.
        timeout_secs (int): The timeout in seconds.
    Returns:
        str: A JSON string containing the results of the API 
            call in the format
            {"response": "<response>", "status_code": <status_code>}
    """

    def is_valid_url(url: str) -> bool:

        """Return True if the url is valid, False otherwise."""

        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False
        
    # End of is_valid_url

    def sanitize(input_string: str) -> str:

        """Remove potentially harmful characters from the input string."""
        
        try:
            data = json.loads(input_string)
        except json.JSONDecodeError:
            # If it's not JSON, sanitize it as a single value.
            sanitized_string = re.sub(r'[^a-zA-Z0-9_: -{}[\],"]', '', input_string)
        else:
            # If it's JSON, sanitize all the values.
            sanitized_string = json.dumps({sanitize(k): sanitize(str(v)) for k, v in data.items()})

        return sanitized_string
    
    # End of sanitize

    # Initialize variables  
    response = {}
    if isinstance(query_params, str):
        try:
            query_params = json.loads(query_params)
        except json.JSONDecodeError:
            query_params = {}
    if isinstance(headers, str):
        try:
            headers = json.loads(headers)
        except json.JSONDecodeError:
            headers = {}

    # Validate inputs
    if not isinstance(query_params, dict):
        raise ValueError("query_params must be a dictionary")
    if not isinstance(headers, dict):
        raise ValueError("headers must be a dictionary")
    if not isinstance(timeout_secs, int) or timeout_secs <= 0:
        raise ValueError("timeout_secs must be a positive integer")

    # Prepare the request -- URL
    if not host.startswith(("http://", "https://")):
        host = f"https://{host}"
    url = urljoin(host, endpoint)
    if not is_valid_url(url):
        return json.dumps({
            "response": 'Invalid host or endpoint',
            "status_code": None
        })
    
    # Prepare the request -- Method
    allowed_methods = ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]
    if method not in allowed_methods:
        raise ValueError("Invalid method: " + method)

    # Prepare the request -- Headers
    if 'Content-Type' not in headers:
        headers['Content-Type'] = 'application/json'
    sanitized_headers = {sanitize(k): sanitize(v) for k, v in headers.items()}
    
    # Prepare the request -- Body
    sanitized_body = sanitize(str(body))
    content_type = sanitized_headers.get('Content-Type')
    if content_type == 'application/json':
        try:
            body_dict = json.loads(sanitized_body)
        except json.JSONDecodeError:
            body_dict = sanitized_body
    elif content_type == 'application/x-www-form-urlencoded':
        body_dict = sanitized_body
    elif content_type == 'multipart/form-data':
        raise ValueError("Content type 'multipart/form-data' is not supported.")
    else:
        raise ValueError('Unsupported Content-Type: ' + content_type)
    
    # Prepare the request -- Query Parameters
    sanitized_query_params = {sanitize(k): sanitize(v) for k, v in query_params.items()}

    # Make the request
    try:
        if method == "GET":
            response = requests.get(url, params=sanitized_query_params, headers=sanitized_headers, timeout=timeout_secs)
        elif method == "HEAD":
            response = requests.head(url, params=sanitized_query_params, headers=sanitized_headers, timeout=timeout_secs)
        elif method == "OPTIONS":
            response = requests.options(url, params=sanitized_query_params, headers=sanitized_headers, timeout=timeout_secs)
        elif method == "POST":
            response = requests.post(url, params=sanitized_query_params, json=body_dict, headers=sanitized_headers, timeout=timeout_secs)
        elif method == "PUT":
            response = requests.put(url, params=sanitized_query_params, json=body_dict, headers=sanitized_headers, timeout=timeout_secs)
        elif method == "DELETE":
            response = requests.delete(url, params=sanitized_query_params, json=body_dict, headers=sanitized_headers, timeout=timeout_secs)
        elif method == "PATCH":
            response = requests.patch(url, params=sanitized_query_params, json=body_dict, headers=sanitized_headers, timeout=timeout_secs)
        else:
            raise ValueError("Invalid method: " + method)
        
        try:
            response_text = json.loads(response.text)
        except json.JSONDecodeError:
            response_text = response.text
        response = {
            "response": response_text,
            "status_code": response.status_code
        }

    except requests.exceptions.RequestException as e:
        response = {
            "error": str(e),
            "status_code": None
        }

    return json.dumps(response)
