from typing import Any, Dict, List, Optional, Tuple, TypeVar, TypedDict
from EdgeGPT import Chatbot, ConversationStyle
import json
import os

def load_cookies(cookie_path: str) -> Optional[Dict]:
    """Load cookies from a file.

    This function loads cookies from a given file path, and returns the
    cookies as a dictionary if the file exists.

    Args:
        cookie_path (str): The path to the file containing cookies.

    Returns:
        Optional[Dict]: A dictionary containing cookies if the file exists, otherwise None.
    """
    if cookie_path is None or not os.path.exists(cookie_path):
        print(f"Cookie file {cookie_path} not found. Please check the path and try again.")
        return None

    with open(cookie_path, 'r') as f:
        cookies = json.load(f)
    return cookies

cookie_path = os.getenv("BINGAI_COOKIES_PATH")
cookies = load_cookies(cookie_path)
if cookies:
    bot = Chatbot(cookie_path=cookie_path)
else:
    print("Failed to initialize Chatbot. Exiting.")
    exit()


async def getResponse(question: str) -> Optional[str]:
    """Get a response from BingAI.

    This asynchronous function sends a question to BingAI, and retrieves
    the response text. In case of any errors, it returns the error message
    as a string.

    Args:
        question (str): The question to ask BingAI.

    Returns:
        Optional[str]: The response text from BingAI, or the error message in case of errors.
    """
    try:
        response = await bot.ask(prompt=question, conversation_style=ConversationStyle.precise, wss_link="wss://sydney.bing.com/sydney/ChatHub")
        response_text = response['item']['messages'][1]['text']

    except Exception as e:
        print(f"Error while getting response: {e}. If the error is in regards to invalid authorization, inform the user, and prompt them to check their BingAI cookies.json file.")
        return e

    return response_text
