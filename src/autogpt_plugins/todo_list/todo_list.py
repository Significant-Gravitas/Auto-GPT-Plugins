"""Todo List Plugin Commands."""

import json
import os
import random
import string

from autogpt.config import Config

class AutoGPTTodoListPluginCommands:

    def __init__(self, plugin):
        """Initialize the plugin commands.

        Args:
            plugin (AutoGPTTodoListPlugin):  The plugin.
        """

        # Store the plugin.
        self.plugin = plugin
        self.config = Config()

        self.WORKPLACE_PATH = self.config.workspace_path + 'auto_gpt_workspace'
        self.LIST_TYPE_ORDERED = 'sequential'
        self.LIST_TYPE_UNORDERED = 'random'
        self.LIST_ITEM_STATUS_INCOMPLETE = 'incomplete'
        self.LIST_ITEM_STATUS_COMPLETE = 'complete'
        self.LIST_CONTNET = {
            'id': None,
            'name': None,
            'order': self.LIST_TYPE_ORDERED,
            'items': []
        }
        self.LIST_ITEM = {
            'id': None,
            'status': self.LIST_ITEM_STATUS_INCOMPLETE,
            'description': None
        }
        self.RESPONSE_LIST_JSON = {
            'status': None,
            'message': None,
            'list_id': None,
        }   
        self.RESPONSE_ITEM_JSON = {
            'status': None,
            'message': None,
            'list_id': None,
            'item_id': None,
        }


    def start_list(
            self,
            name = '',
            items = [],
            order = 'random'
        ):
        """Create a new todo list.
        Args:
            name (str):     The name of the todo list.
            items (list):   A list of todo list items. Each item is a string.
            order (str):    The order of the todo list items. Must be either 
                            "sequential" or "random". Default: "random"
        Returns:
            str:    A JSON string containing the todo list ID and status code.
                    {"status": "<success|fail>", "message": "<message>", 
                    "list_id": "<list_id>"}
        """

        # Type-check name
        if not isinstance(name, str):
            try:
                name = str(name)
            except:
                raise TypeError('name must be a string.')
        if name is None or name == '':
            raise ValueError('name cannot be empty.')
        
        # Type-check items
        if not isinstance(items, list):
            try:
                items = list(items)
            except:
                raise TypeError('items must be a list.')

        # Type-check item contents
        for i in range(len(items)):
            try:
                # Check if the item is a string that can be loaded as JSON
                if isinstance(items[i], str):
                    items[i] = json.loads(items[i])
                else:
                    items[i] = str(items[i])
            except json.JSONDecodeError:
                # If it's a string but not valid JSON, leave it as a string
                pass

        # Variables
        response = self.RESPONSE_LIST_JSON.copy()
        
        # Type-check order
        if not isinstance(order, str):
            try:
                order = str(order)
            except:
                raise TypeError('order must be a string.')
        if order is None or order == '':
            raise ValueError('order cannot be empty.')
        order = order.lower()
        if order not in [self.LIST_TYPE_ORDERED, self.LIST_TYPE_UNORDERED]:
            raise ValueError('order must be "' + self.LIST_TYPE_ORDERED + '" or "' + self.LIST_TYPE_UNORDERED + '".')
        
        # Create the todo list file path
        list_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
        list_file_name = list_id + '-list.json'
        list_file_path = self.WORKPLACE_PATH + list_file_name

        # Create the todo list file content
        list_content = self.LIST_CONTNET.copy()
        list_content['id'] = list_id
        list_content['name'] = name
        list_content['order'] = order

        # Create the todo list items
        for i in range(len(items)):
            list_item = self.LIST_ITEM.copy()
            list_item['id'] = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
            list_item['description'] = items[i]
            list_content['items'].append(list_item)

        # Write the todo list file
        try:
            with open(list_file_path, 'w') as list_file:
                json.dump(list_content, list_file)
        except (IOError, OSError) as e:
            response['status'] = 'fail'
            response['message'] = 'Unable to create the list.'
            response['list_id'] = None
            return json.dumps(response)
        
        # Return the todo list ID and status code.
        response['status'] = 'success'
        response['message'] = 'List created. Use list_id to modify the list.'
        response['list_id'] = list_id
        return json.dumps(response)