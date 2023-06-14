"""API Call command for Autogpt."""

import json
import re
import requests
from typing import Dict, Optional
from urllib.parse import urljoin, urlparse
from urllib.parse import urljoin
from validators import url as is_valid_url

class ApiCallCommand:
    """
    A class used to make API calls.
    """

    def sanitize_string(self, input_string: str) -> str:
        """
        Remove potentially harmful characters from the string.

        Args:
            input_string (str): The string to sanitize.

        Returns:
            str: The sanitized string.
        """

        return re.sub(r'[^a-zA-Z0-9_: -{}[\],"]', '', input_string)
    
    # End of sanitize_string()


    def sanitize_json(self, input_string: str) -> str:
        """
        Sanitize all the values in a JSON string.
        
        Args:
            input_string (str): The JSON string to sanitize.
            
        Returns:
            str: The sanitized JSON string.
        """

        data = json.loads(input_string)
        sanitized_data = {self.sanitize_string(k): self.sanitize_string(str(v)) for k, v in data.items()}
        return json.dumps(sanitized_data)
    
    # End of sanitize_json()


    def sanitize(self, input_string: str) -> str:
        """
        Remove potentially harmful characters from the input string.
        
        Args:
            input_string (str): The string to sanitize.
            
        Returns:
            str: The sanitized string.
        """

        try:
            sanitized_string = self.sanitize_json(input_string)
        except json.JSONDecodeError:
            sanitized_string = self.sanitize_string(input_string)
        return sanitized_string

    # End of sanitize()


    def make_api_call(self, host = "", endpoint = "", mthd = "GET", params = {}, body = "", 
                      hdrs = {"Content-Type": "application/json"}, timeout = 60) -> str:
        """
        Return the results of an API call
        
        Args:
            host (str): The host to call.
            endpoint (str): The endpoint to call.
            mthd (str): The HTTP method to use.
            params (dict): The query parameters to use.
            body (str): The body to use.
            hdrs (dict): The headers to use.
            timeout (int): The timeout to use.

        Returns:
            str: A JSON string containing the results of the API 
                call in the format
                {"status": "success|error", "status_code": int, "response": str, "response": str}
        """

        # Initialize variables  
        response = {}

        # Type-check inputs - host
        if not isinstance(host, str):
            raise ValueError("host must be a string")
        
        # Type-check inputs - endpoint
        if not isinstance(endpoint, str):
            raise ValueError("endpoint must be a string")
        
        # Type-check inputs - method
        if not isinstance(mthd, str):
            raise ValueError("method must be a string")
        
        # Type-check inputs - query_params
        if not params:
            params = {}
        elif isinstance(params, str):
            try:
                params = json.loads(params)
            except json.JSONDecodeError:
                raise ValueError("query_params must be a dictionary")
        elif isinstance(params, dict):
            new_query_params = {}
            for k, v in params.items():
                if k is None:
                    raise ValueError("query_params cannot contain None keys")
                if not isinstance(k, str):
                    k = str(k)
                if v is not None and not isinstance(v, str):
                    v = str(v)
                new_query_params[k] = v
            params = new_query_params
        else:
            raise ValueError("query_params must be a dictionary or a JSON string")

        # Type-check inputs - body
        if not isinstance(body, str):
            try:
                body = str(body)
            except ValueError:
                raise ValueError("body must be a string")
            
        # Type-check inputs - headers
        if not hdrs:
            hdrs = {}
        elif isinstance(hdrs, str):
            try:
                hdrs = json.loads(hdrs)
            except json.JSONDecodeError:
                raise ValueError("headers must be a dictionary")
        elif isinstance(hdrs, dict):
            new_headers = {}
            for k, v in hdrs.items():
                if k is None:
                    raise ValueError("headers cannot contain None keys")
                if not isinstance(k, str):
                    k = str(k)
                if v is not None and not isinstance(v, str):
                    v = str(v)
                new_headers[k] = v
            hdrs = new_headers
        else:
            raise ValueError("headers must be a dictionary or a JSON string")
            
        # Type-check inputs - timeout_secs
        if timeout is None:
            raise ValueError("timeout_secs must be an integer")
        elif not isinstance(timeout, int):
            try:
                timeout = int(timeout)
            except ValueError:
                raise ValueError("timeout_secs must be an integer")

        # Validate URL
        if '?' in host or '&' in host:
            raise ValueError("Invalid URL: Host must not contain query parameters")
        sanitized_host = self.sanitize(host)
        sanitized_endpoint = self.sanitize(endpoint)
        if not sanitized_host.startswith(("http://", "https://")):
            sanitized_host = f"https://{sanitized_host}"
        url = urljoin(sanitized_host, sanitized_endpoint)
        if not is_valid_url(url): # type: ignore
            raise ValueError("Invalid URL: " + url)
        
        # Validate method
        allowed_methods = ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]
        sanitized_method = self.sanitize(mthd).upper()    
        if sanitized_method not in allowed_methods:
            raise ValueError("Invalid method: " + sanitized_method)

        # Validate timeout_secs
        if not timeout > 0:
            raise ValueError("timeout_secs must be a positive integer")
        
        # Make the request
        try:
            if sanitized_method == "GET":
                response = requests.get(url, params=params, headers=hdrs, timeout=timeout)
            elif sanitized_method == "HEAD":
                response = requests.head(url, params=params, headers=hdrs, timeout=timeout)
            elif sanitized_method == "OPTIONS":
                response = requests.options(url, params=params, headers=hdrs, timeout=timeout)
            elif sanitized_method == "POST":
                response = requests.post(url, params=params, json=body, headers=hdrs, timeout=timeout)
            elif sanitized_method == "PUT":
                response = requests.put(url, params=params, json=body, headers=hdrs, timeout=timeout)
            elif sanitized_method == "DELETE":
                response = requests.delete(url, params=params, json=body, headers=hdrs, timeout=timeout)
            elif sanitized_method == "PATCH":
                response = requests.patch(url, params=params, json=body, headers=hdrs, timeout=timeout)
            else:
                raise ValueError("Invalid method: " + mthd)
            
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
    
    # End of call_api()

# End of class ApiCallCommand
