# Auto-GPT SerpApi Search Plugin

This search plugin integrates [SerpApi](https://serpapi.com) into Auto-GPT, allowing users to choose a broader range of
search engines supported by SerpApi, and get much more information than the default search engine in Auto-GPT.

## Key Features:
- Perform search queries with engine of your choice supported by SerpApi, including Google, Bing, Baidu, Yahoo, DuckDuckGo, Yandex and so on.

## Installation

- Follow the instructions as per the [Auto-GPT-Plugins/README.md](https://github.com/Significant-Gravitas/Auto-GPT-Plugins/blob/master/README.md)

- Append the following configuration settings to the `.env` file within AutoGPT, see [Configuration](#configuration) for details:

    ```ini
    ################################################################################
    ### SerpApi
    ################################################################################

    SERPAPI_API_KEY=
    SERPAPI_ENGINE=
    SERPAPI_NO_CACHE=
    SERPAPI_RESULT_FILTER=
    ```


- In the `.env` file, search for `ALLOWLISTED_PLUGINS` and add this plugin:

    ```ini
    ################################################################################
    ### ALLOWLISTED PLUGINS
    ################################################################################

    #ALLOWLISTED_PLUGINS - Sets the listed plugins that are allowed (Example: plugin1,plugin2,plugin3)
    ALLOWLISTED_PLUGINS=AutoGPTSerpApiSearch
    ```

## Configuration

| Variable | Required | Description |
| ---- | ---- | ---- |
| SERPAPI_API_KEY | Yes | Your API key for the SerpApi. You can obtain a key by following the steps:<br>- Sign up for a free account at [SerpApi](https://serpapi.com).<br>- Navigate to the [Dashboard](https://serpapi.com/dashboard) page and find "Your Private API Key". |
| SERPAPI_ENGINE | No | The engine you want to use for web searches performed by Auto-GPT.<br>- You can find valid engine values from [SerpApi Documentation](https://serpapi.com/search-api).<br>- Typical values are: `google`, `bing`, `baidu`, `yahoo`, `duckduckgo`, `yandex`, ...<br>- The default value is `google` if not set. |
| SERPAPI_NO_CACHE | No | Set to `true` if you want to force SerpApi to fetch the results even if a cached version is already present. Defaulted to `false`. |
| SERPAPI_RESULT_FILTER | No | SerpApi can return JSON results that is too large for Auto-GPT to process. This variable allows you to pick certain fields from the returned JSON to reduce the size. Defaulted to `organic_results(title,link,snippet)`. See [Result Filter](#result-filter) for details.|

### Result Filter
This plugin supports filtering fields up to a depth of 2. The syntax of the filter is `<t>(<s>,<s>,...),<t>(<s>,<s>,...),...`, where `<t>` is top level field, and `<s>` is second level field. `<s>` is optional. Set to `<none>` to disable filtering. Here are some examples:
- `<none>`
  - Filter disabled. The whole JSON output will be the input of the current command.
- `organic_results`:
  - Pick only `organic_results` from the top level fields of JSON output.
- `organic_results, knowledge_graph`:
  - Pick only `organic_results` and `knowledge_graph` from the top level fields of JSON output.
- `organic_results(title, link, snippet)`:
  - Pick only `organic_results` from the top level fields of JSON output.
  - Pick only `title`, `link` and `snippet` from `organic_results`.
    - If `organic_results` is an object, applies to itself.
    - If `organic_results` is an array, applies to all its containing objects.
    - Otherwise, the second level filter is ignored.
- `organic_results(title,link,snippet), knowledge_graph(website, description)`:
  - Pick only `organic_results` and `knowledge_graph` from the top level fields of JSON output.
  - Pick only `title`, `link` and `snippet` from `organic_results`.
    - If `organic_results` is an object, applies to itself.
    - If `organic_results` is an array, applies to all its containing objects.
    - Otherwise, the second level filter is ignored.
  - Pick only `website`, and `description` from `knowledge_graph`.
    - If `knowledge_graph` is an object, applies to itself.
    - If `knowledge_graph` is an array, applies to all its containing objects.
    - Otherwise, the second level filter is ignored.

### Filter Tuning
Sometimes too much input can make Auto-GPT confused, failing to extract the correct information. Other than [organic_results](https://serpapi.com/organic-results), SerpApi extracts more fields such as [answer_box](https://serpapi.com/direct-answer-box-api), [knowledge_graph](https://serpapi.com/knowledge-graph) and [related_questions](https://serpapi.com/related-questions), which are more straightforward and easier to make sense of, but not always present. You can always check if those exist through the [Dashboard](https://serpapi.com/searches) and add/remove fields to the filter according to your needs.

### Example
Here's an example to let Auto-GPT search on Google and get information from "Answer Box" and "Knowledge Graph"

```ini
SERPAPI_API_KEY=your_api_key
SERPAPI_ENGINE=google
SERPAPI_RESULT_FILTER=answer_box,knowledge_graph
```

## How it works
When `SERPAPI_API_KEY` is set. The plugin will add a new command `serpapi_search` to Auto-GPT. The `google` command will be intercepted to use `serpapi_search` instead. Auto-GPT can also use `serpapi_search` command directly. Therefore, all web searches performed by Auto-GPT are routed to SerpApi.