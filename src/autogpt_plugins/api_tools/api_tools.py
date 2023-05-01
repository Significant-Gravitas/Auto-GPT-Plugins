"""API Call command for Autogpt."""

import json
import requests
import re

from typing import Optional, Dict
from urllib.parse import urlparse
from urllib.parse import urljoin
from validators import url as is_valid_url

def _make_api_call(
        host = "", 
        endpoint = "", 
        method = "GET", 
        query_params = {},
        body = "", 
        headers = {"Content-Type": "application/json"},
        timeout_secs = 60) -> str:
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
            {"status": "success|error", "status_code": int, "response": str, "response": str}
    """

    def sanitize_string(input_string: str) -> str:
        """Remove potentially harmful characters from the string."""

        return re.sub(r'[^a-zA-Z0-9_: -{}[\],"]', '', input_string)
    
    # End of sanitize_string()


    def sanitize_json(input_string: str) -> str:
        """Sanitize all the values in a JSON string."""

        data = json.loads(input_string)
        sanitized_data = {sanitize_string(k): sanitize_string(str(v)) for k, v in data.items()}
        return json.dumps(sanitized_data)
    
    # End of sanitize_json()

    
    def sanitize(input_string: str) -> str:
        """Remove potentially harmful characters from the input string."""

        try:
            sanitized_string = sanitize_json(input_string)
        except json.JSONDecodeError:
            sanitized_string = sanitize_string(input_string)
        return sanitized_string

    # End of sanitize()


    # Initialize variables  
    response = {}

    # Type-check inputs - host
    if not isinstance(host, str):
        raise ValueError("host must be a string")
    
    # Type-check inputs - endpoint
    if not isinstance(endpoint, str):
        raise ValueError("endpoint must be a string")
    
    # Type-check inputs - method
    if not isinstance(method, str):
        raise ValueError("method must be a string")
    
    # Type-check inputs - query_params
    if not query_params:
        query_params = {}
    elif isinstance(query_params, str):
        try:
            query_params = json.loads(query_params)
        except json.JSONDecodeError:
            raise ValueError("query_params must be a dictionary")
    elif isinstance(query_params, dict):
        new_query_params = {}
        for k, v in query_params.items():
            if k is None:
                raise ValueError("query_params cannot contain None keys")
            if not isinstance(k, str):
                k = str(k)
            if v is not None and not isinstance(v, str):
                v = str(v)
            new_query_params[k] = v
        query_params = new_query_params
    else:
        raise ValueError("query_params must be a dictionary or a JSON string")

    # Type-check inputs - body
    if not isinstance(body, str):
        try:
            body = str(body)
        except ValueError:
            raise ValueError("body must be a string")
        
    # Type-check inputs - headers
    if not headers:
        headers = {}
    elif isinstance(headers, str):
        try:
            headers = json.loads(headers)
        except json.JSONDecodeError:
            raise ValueError("headers must be a dictionary")
    elif isinstance(headers, dict):
        new_headers = {}
        for k, v in headers.items():
            if k is None:
                raise ValueError("headers cannot contain None keys")
            if not isinstance(k, str):
                k = str(k)
            if v is not None and not isinstance(v, str):
                v = str(v)
            new_headers[k] = v
        headers = new_headers
    else:
        raise ValueError("headers must be a dictionary or a JSON string")
        
    # Type-check inputs - timeout_secs
    if timeout_secs is None:
        raise ValueError("timeout_secs must be an integer")
    elif not isinstance(timeout_secs, int):
        try:
            timeout_secs = int(timeout_secs)
        except ValueError:
            raise ValueError("timeout_secs must be an integer")

    # Validate URL
    if '?' in host or '&' in host:
        raise ValueError("Invalid URL: Host must not contain query parameters")
    sanitized_host = sanitize(host)
    sanitized_endpoint = sanitize(endpoint)
    if not sanitized_host.startswith(("http://", "https://")):
        sanitized_host = f"https://{sanitized_host}"
    url = urljoin(sanitized_host, sanitized_endpoint)
    if not is_valid_url(url):
        raise ValueError("Invalid URL: " + url)
    
    # Validate method
    allowed_methods = ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]
    sanitized_method = sanitize(method).upper()    
    if sanitized_method not in allowed_methods:
        raise ValueError("Invalid method: " + sanitized_method)

    # Validate timeout_secs
    if not timeout_secs > 0:
        raise ValueError("timeout_secs must be a positive integer")
    
    # Make the request
    try:
        if sanitized_method == "GET":
            response = requests.get(url, params=query_params, headers=headers, timeout=timeout_secs)
        elif sanitized_method == "HEAD":
            response = requests.head(url, params=query_params, headers=headers, timeout=timeout_secs)
        elif sanitized_method == "OPTIONS":
            response = requests.options(url, params=query_params, headers=headers, timeout=timeout_secs)
        elif sanitized_method == "POST":
            response = requests.post(url, params=query_params, json=body, headers=headers, timeout=timeout_secs)
        elif sanitized_method == "PUT":
            response = requests.put(url, params=query_params, json=body, headers=headers, timeout=timeout_secs)
        elif sanitized_method == "DELETE":
            response = requests.delete(url, params=query_params, json=body, headers=headers, timeout=timeout_secs)
        elif sanitized_method == "PATCH":
            response = requests.patch(url, params=query_params, json=body, headers=headers, timeout=timeout_secs)
        else:
            raise ValueError("Invalid method: " + method)
        
        response_text = response.text
        response = {
            "status": "success",
            "status_code": response.status_code,
            "response": response_text
        }

    except requests.exceptions.RequestException as e:
        response = {
            "status": "error",
            "status_code": None,
            "response": str(e)
        }

    return json.dumps(response)
