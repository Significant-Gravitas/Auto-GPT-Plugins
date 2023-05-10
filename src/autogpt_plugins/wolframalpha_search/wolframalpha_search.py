from . import AutoGPTWolframAlphaSearch

plugin = AutoGPTWolframAlphaSearch()


def _wolframalpha_search(query: str) -> str | list[str]:
    res = ""
    try:
        ans = plugin.api.query(query)
        res = next(ans.results).text
    except Exception as e:
        return f"'_wolframalpha_search' on query: '{query}' raised exception: '{e}'"
    return res
