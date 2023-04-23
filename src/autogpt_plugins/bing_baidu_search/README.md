# Auto-GPT Bing Baidu Search Plugin: Extend Your Search Options with Auto-GPT

Language: [English](https://github.com/ForestLinSen/Auto-GPT-Plugins/blob/master/src/autogpt_plugins/bing_baidu_search/README.md) | [中文](https://github.com/ForestLinSen/Auto-GPT-Plugins/blob/master/src/autogpt_plugins/bing_baidu_search/README.zh.md)

The Auto-GPT Bing Baidu Search Plugin is a useful plugin for the base project, Auto-GPT. With the aim of expand the search experience, this search plugin integrates Bing and Baidu search engines into Auto-GPT, complementing the existing support for Google Search and DuckDuckGo Search provided by the main repository.

## Key Features:
- Bing Search: Perform search queries using the Bing search engine.
- Baidu Search: Conduct search queries using the Baidu search engine.

## How it works
If the Azure API key is set, the search engine will default to Bing. To use Baidu Search, set the environment variable `SEARCH_ENGINE` to "baidu" and provide the `BAIDU_COOKIE`.

## Installation:
1. Download the Auto-GPT Bing Baidu Search Plugin repository as a ZIP file.
2. Copy the ZIP file into the "plugins" folder of your Auto-GPT project.

### Azure API Key and Bing Search Configuration:
1. Go to the [Bing Web Search API](https://www.microsoft.com/en-us/bing/apis/bing-web-search-api) website.
2. Sign into your Microsoft Azure account or create a new account if you don't have one.
3. After setting up your account, go to the "Keys and Endpoint" section.
4. Copy the key from there and add it to the `.env` file in your project directory.
5. Name the environment variable `AZURE_API_KEY`.

![Baidu Cookie](./screenshots/azure_api.png)

Example of the `.env` file:
```
AZURE_API_KEY=your_azure_api_key
```

Remember to replace `your_azure_api_key` with the actual API key you obtained from the Microsoft Azure portal.

### Obtaining Baidu Cookie:
1. Open the Chrome browser and search for something on Baidu.
2. Open Developer Tools (press F12 or right-click and select "Inspect").
3. Go to the "Network" tab.
4. Find the first name file in the list of network requests.
5. On the right side, find the "Cookie" header and copy all of its content.

![Baidu Cookie](./screenshots/baidu_cookie.png)

Set the `BAIDU_COOKIE` in the `.env` file:
```
BAIDU_COOKIE=your-baidu-cookie
```

Remember to replace `your-baidu-cookie` with the actual cookie content you obtained from the Chrome Developer Tools.


