"""This is the Bing and Baidu search engines plugin for Auto-GPT."""
import json
import os
from typing import Any, Dict, List, Optional, Tuple, TypedDict, TypeVar
from bs4 import BeautifulSoup
import re

import requests
from auto_gpt_plugin_template import AutoGPTPluginTemplate

PromptGenerator = TypeVar("PromptGenerator")

def baidu_search(query: str, num_results=8):
    '''
    Perform a Baidu search and return the results as a JSON string.
    '''

    headers = {
        'Cookie': os.getenv("BAIDU_COOKIE"),
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:112.0) Gecko/20100101 Firefox/112.0"
    }
    url = f'https://www.baidu.com/s?wd={query}&rn={num_results}'
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    search_results = []

    for result in soup.find_all('div', class_=re.compile('^result c-container ')):
        title = result.find('h3', class_='t').get_text()
        link = result.find('a', href=True)['href']
        snippet = result.find('span', class_=re.compile('^content-right_8Zs40'))
        if snippet:
            snippet = snippet.get_text()
        else:
            snippet = ''
        search_results.append({
            'title': title,
            'href': link,
            'snippet': snippet
        })

    return json.dumps(search_results, ensure_ascii=False, indent=4)


def _bing_search(query: str, num_results=8) -> str:
    """
    Perform a Bing search and return the results as a JSON string.
    """
    subscription_key = os.getenv("AZURE_API_KEY")

    # Bing Search API endpoint
    search_url = "https://api.bing.microsoft.com/v7.0/search"

    headers = {"Ocp-Apim-Subscription-Key": subscription_key}
    params = {
        "q": query,
        "count": num_results,
        "textDecorations": True,
        "textFormat": "HTML",
    }
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()

    # Extract the search result items from the response
    web_pages = search_results.get("webPages", {})
    search_results = web_pages.get("value", [])

    # Create a list of search result dictionaries with 'title', 'href', and 'body' keys
    search_results_list = [
        {"title": item["name"], "href": item["url"], "body": item["snippet"]}
        for item in search_results
    ]

    # Return the search results as a JSON string
    return json.dumps(search_results_list, ensure_ascii=False, indent=4)


class Message(TypedDict):
    role: str
    content: str


class AutoGPTBingBaiduSearch(AutoGPTPluginTemplate):
    def __init__(self):
        super().__init__()
        self._name = "Bing-Baidu-Search-Plugin"
        self._version = "0.1.0"
        self._description = (
            "This plugin performs Bing and Baidu searches using the provided query."
        )
        self._query = ""
        self.able_to_handle_post_command = True

    def can_handle_on_planning(self) -> bool:
        return False

    def on_planning(
        self, prompt: PromptGenerator, messages: List[Message]
    ) -> Optional[str]:
        pass

    def can_handle_pre_command(self) -> bool:
        return True

    def can_handle_on_response(self) -> bool:
        return False

    def on_response(self, response: str, *args, **kwargs) -> str:
        pass

    def can_handle_post_prompt(self) -> bool:
        return False

    def post_prompt(self, prompt: PromptGenerator) -> PromptGenerator:
        pass

    def can_handle_post_planning(self) -> bool:
        return False

    def post_planning(self, response: str) -> str:
        pass

    def can_handle_pre_instruction(self) -> bool:
        return False

    def pre_instruction(self, messages: List[Message]) -> List[Message]:
        pass

    def can_handle_on_instruction(self) -> bool:
        return False

    def on_instruction(self, messages: List[Message]) -> Optional[str]:
        pass

    def can_handle_post_instruction(self) -> bool:
        return False

    def post_instruction(self, response: str) -> str:
        pass

    def can_handle_pre_command(self) -> bool:
        return True

    def pre_command(
        self, command_name: str, arguments: Dict[str, Any]
    ) -> Tuple[str, Dict[str, Any]]:
        if command_name == "google":
            if (os.getenv("AZURE_API_KEY") is not None) or (os.getenv("SEARCH_ENGINE") == "baidu" and os.getenv("BAIDU_COOKIE") is not None):
                self._query = arguments["query"]
                # this command does nothing but it is required to continue performing the post_command function
                return "execute_shell", {"command_line": "pwd"}
            else:
                self.able_to_handle_post_command = False
                return command_name, arguments
        else:
            self.able_to_handle_post_command = False
            return command_name, arguments

    def can_handle_post_command(self) -> bool:
        return self.able_to_handle_post_command

    def post_command(self, command_name: str, response: str) -> str:
        if self._query != "":
            result = ""
            if os.getenv("AZURE_API_KEY") is not None:
                result = _bing_search(self._query)
                self._query = ""
            elif os.getenv("SEARCH_ENGINE") == "baidu":
                result = baidu_search(self._query)
                self._query = ""
            return result

    def can_handle_chat_completion(
        self, messages: Dict[Any, Any], model: str, temperature: float, max_tokens: int
    ) -> bool:
        return False

    def handle_chat_completion(
        self, messages: List[Message], model: str, temperature: float, max_tokens: int
    ) -> str:
        pass
