# Item List Plugin

If your agent has lists to keep track of, use the item list to save, read and modify the list from a JSON file.

## Key Features:
- Create, delete, manage task lists
- Create, delete, manage tasks

### Commands
- make_list: {"name": "`<name:str>`", "items": "`<items:list>`", "order": "`<sequential|random:str>`"}
- add_item_to_list: {"list_id": "`<list_id:str>`", "description": "`<description:str>`"},
- mark_item_as_done": {"list_id": "`<list_id:str>`", "item_id": "`<item_id:int>`"},
- mark_item_as_not_done: {"list_id": "`<list_id:str>`", "item_id": "`<item_id:int>`"},
- delete_item_from_list: {"list_id": "`<list_id:str>`", "item_id": "`<item_id:int>`"}
- get_list_items: {"list_id": "`<list_id:str>"`},
- get_next_list_item: {"list_id": "`<list_id:str>"`},
- mark_list_as_done: {"list_id": "`<list_id:str>"`},

## Installation:
As part of the AutoGPT plugins package, follow the [installation instructions](https://github.com/Significant-Gravitas/Auto-GPT-Plugins) on the Auto-GPT-Plugins GitHub reporistory README page.

## AutoGPT Configuration
Set `ALLOWLISTED_PLUGINS=autogpt-item-list,example-plugin1,example-plugin2,etc` in your AutoGPT `.env` file.
