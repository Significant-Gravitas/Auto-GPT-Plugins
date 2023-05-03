"""Item List Plugin Commands."""

import json
import os
import random
import string
import sys

class AutoGPTItemListPluginCommands:

    def __init__(self, plugin):
        """Initialize the plugin commands.

        Args:
            plugin (AutoGPTItemList):  The plugin.
        """

        # Store the plugin.
        self.plugin = plugin
        
        # Constants
        self.LIST_ID_LENGTH = 6
        self.LIST_TYPE_ORDERED = 'sequential'
        self.LIST_TYPE_UNORDERED = 'random'
        self.LIST_ITEM_STATUS_INCOMPLETE = 'todo'
        self.LIST_ITEM_STATUS_COMPLETE = 'done'
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
        self.RESPONSE_LIST_ITEMS_JSON = {
            'status': None,
            'message': None,
            'list_id': None,
            'items': None,
        }

        # Get the workspace path
        current_dir = os.getcwd()
        self.WORKSPACE_PATH = os.path.join(current_dir, "auto_gpt_workspace")


    def write_list_file(
            self,
            file_path: str,
            list_content: dict
        ) -> bool:
        """Write a todo list file.
        Args:
            file_path (str):    The path to the todo list file.
            list_content (dict):    The content of the todo list file.
        Returns:
            bool:   True if the file was written successfully, False otherwise.
        """

        # Content check file_path
        if not isinstance(file_path, str):
            raise TypeError('file_path must be a string.')
        if file_path is None or file_path == '':
            raise ValueError('file_path cannot be empty.')
        
        # Connect check list_content
        if not isinstance(list_content, dict):
            raise TypeError('list_content must be a dictionary.')
        if list_content is None or list_content == {}:
            raise ValueError('list_content cannot be empty.')

        # Write the todo list file, replacing if it already exists
        try:
            with open(file_path, 'w') as f:
                json.dump(list_content, f)
            return True
        except:
            return False
        

    def read_list_file(
            self,
            file_path: str
        ) -> dict:
        """Read a todo list file.
        Args:
            file_path (str):    The path to the todo list file.
        Returns:
            dict:   The content of the todo list file.
        """

        # Content check file_path
        if not isinstance(file_path, str):
            raise TypeError('file_path must be a string.')
        if file_path is None or file_path == '':
            raise ValueError('file_path cannot be empty.')
        
        # Read the todo list file
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except:
            return None
        

    def build_file_path(
            self,
            list_id: str
        ) -> str:  
        """Build a file path.
        Args:
            list_id (str):    The ID of the list.
        Returns:
            str:   The file path.
        """
    
        # Type-check list_id
        if not isinstance(list_id, str):
            try:
                list_id = str(list_id)
            except:
                raise TypeError('list_id must be a string.')   
            
        # Build the file path
        list_file_name = 'list-' + list_id + '.json'
        return os.path.join(self.WORKSPACE_PATH, list_file_name + '.json')
    

    def make_list(
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
        list_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=self.LIST_ID_LENGTH))
        list_file_path = self.build_file_path(list_id)

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
        write_to_file = self.write_list_file(list_file_path, list_content)
        if not write_to_file:
            response['status'] = 'fail'
            response['message'] = 'Unable to create the list.'
            response['list_id'] = None
        else:
            response['status'] = 'success'
            response['message'] = 'List savaed as ' + list_file_name + '. Use list_id to modify the list.'
            response['list_id'] = list_id

        return json.dumps(response)
    

    def add_item_to_list(
            self,
            list_id = '',
            description = ''    
        ):
        """Add an item to a todo list.
        Args:
            list_id (str):      The ID of the todo list.
            description (str):  The description of the todo list item.
            Returns:
            str:    A JSON string confirming the add in this format:
                    {"status": "<success|fail:str>", "message": "<message:str>",
                    "list_id": "<list_id:str>", "item_id": "<item_id:str>"}
        """

        # Variables
        response = self.RESPONSE_ITEM_JSON.copy()

        # Type-check list_id
        if not isinstance(list_id, str):
            try:
                list_id = str(list_id)
            except:
                raise TypeError('list_id must be a string.')
            
        # Type-check description
        if not isinstance(description, str):
            try:
                description = str(description)
            except:
                raise TypeError('description must be a string.')
            
        # Build file name and path
        list_file_path = self.build_file_path(list_id)

        # Load the list
        list_content = self.read_list_file(list_file_path)
        if list_content is None:
            response['status'] = 'fail'
            response['message'] = 'Unable to load the list.'
            response['list_id'] = list_id
            return json.dumps(response)
        
        # Add the item to the end of the list
        list_item = self.LIST_ITEM.copy()
        list_item['id'] = len(list_content['items']) + 1
        list_item['description'] = description
        list_content['items'].append(list_item)

        # Write the list
        write_to_file = self.write_list_file(list_file_path, list_content)
        if not write_to_file:
            response['status'] = 'fail'
            response['message'] = 'Unable to add the item.'
            response['list_id'] = list_id
            response['item_id'] = None
        else:
            response['status'] = 'success'
            response['message'] = 'Item added to list.'
            response['list_id'] = list_id
            response['item_id'] = list_item['id']


    def mark_item_as_done(
            self,
            list_id = '',
            item_id = 0
        ) -> str:
        """Mark an item as done.
        Args:
            list_id (str):  The ID of the todo list.
            item_id (int):  The ID of the todo list item.
        Returns:
            str:    A JSON string confirming the mark in this format:
                    {"status": "<success|fail:str>", "message": "<message:str>",
                    "list_id": "<list_id:str>", "item_id": "<item_id:int>"}
        """
        
        # Variables
        response = self.RESPONSE_ITEM_JSON.copy()

        # Type-check list_id
        if not isinstance(list_id, str):
            try:
                list_id = str(list_id)
            except:
                raise TypeError('list_id must be a string.')
        
        # Type-check item_id
        if not isinstance(item_id, int):
            try:
                item_id = int(item_id)
            except:
                raise TypeError('item_id must be an integer.')
            
        # Build file name and path
        list_file_path = self.build_file_path(list_id)

        # Load the list
        list_content = self.read_list_file(list_file_path)
        if list_content is None:
            response['status'] = 'fail'
            response['message'] = 'Unable to load the list.'
            response['list_id'] = list_id
            response['item_id'] = item_id
            return json.dumps(response)
        
        # Mark the item as done
        for i in range(len(list_content['items'])):
            if list_content['items'][i]['id'] == item_id:
                list_content['items'][i]['status'] = self.LIST_ITEM_STATUS_COMPLETE
                break

        # Write the list
        write_to_file = self.write_list_file(list_file_path, list_content)

        if not write_to_file:
            response['status'] = 'fail'
            response['message'] = 'Unable to mark the item as done.'
            response['list_id'] = list_id
            response['item_id'] = item_id
        else:
            response['status'] = 'success'
            response['message'] = 'Item marked as done.'
            response['list_id'] = list_id
            response['item_id'] = item_id
        

    def mark_item_as_not_done(
            self,
            list_id = '',
            item_id = 0
        ) -> str:
        """Mark an item as not done.
        Args:
            list_id (str):  The ID of the todo list.
            item_id (int):  The ID of the todo list item.
        Returns:
            str:    A JSON string confirming the mark in this format:
                    {"status": "<success|fail:str>", "message": "<message:str>",
                    "list_id": "<list_id:str>", "item_id": "<item_id:int>"}
        """

        # Variables
        response = self.RESPONSE_ITEM_JSON.copy()

        # Type-check list_id
        if not isinstance(list_id, str):
            try:
                list_id = str(list_id)
            except:
                raise TypeError('list_id must be a string.')
        
        # Type-check item_id
        if not isinstance(item_id, int):
            try:
                item_id = int(item_id)
            except:
                raise TypeError('item_id must be an integer.')
            
        # Build file name and path
        list_file_path = self.build_file_path(list_id)

        # Load the list
        list_content = self.read_list_file(list_file_path)
        if list_content is None:
            response['status'] = 'fail'
            response['message'] = 'Unable to load the list.'
            response['list_id'] = list_id
            response['item_id'] = item_id
            return json.dumps(response)
        
        # Mark the item as not done
        for i in range(len(list_content['items'])):
            if list_content['items'][i]['id'] == item_id:
                list_content['items'][i]['status'] = self.LIST_ITEM_STATUS_INCOMPLETE
                break

        # Write the list
        write_to_file = self.write_list_file(list_file_path, list_content)

        if not write_to_file:
            response['status'] = 'fail'
            response['message'] = 'Unable to mark the item as not done.'
            response['list_id'] = list_id
            response['item_id'] = item_id
        else:
            response['status'] = 'success'
            response['message'] = 'Item marked as not done.'
            response['list_id'] = list_id
            response['item_id'] = item_id


    def delete_item_from_list(
            self,
            list_id = '',
            item_id = 0
        ) -> str:
        """Delete an item from a list.
        Args:
            list_id (str):  The ID of the todo list.
            item_id (int):  The ID of the todo list item.
        Returns:
            str:    A JSON string confirming the deletion in this format:
                    {"status": "<success|fail:str>", "message": "<message:str>",
                    "list_id": "<list_id:str>", "item_id": "<item_id:int>"}
        """

        # Variables
        response = self.RESPONSE_ITEM_JSON.copy()

        # Type-check list_id
        if not isinstance(list_id, str):
            try:
                list_id = str(list_id)
            except:
                raise TypeError('list_id must be a string.')
            
        # Type-check item_id
        if not isinstance(item_id, int):
            try:
                item_id = int(item_id)
            except:
                raise TypeError('item_id must be an integer.')
            
        # Build file name and path
        list_file_path = self.build_file_path(list_id)

        # Load the list
        list_content = self.read_list_file(list_file_path)

        if list_content is None:
            response['status'] = 'fail'
            response['message'] = 'Unable to load the list.'
            response['list_id'] = list_id
            response['item_id'] = item_id
            return json.dumps(response)
        
        # Delete the item
        for i in range(len(list_content['items'])):
            if list_content['items'][i]['id'] == item_id:
                del list_content['items'][i]
                break
        
        # Write the list
        write_to_file = self.write_list_file(list_file_path, list_content)

        if not write_to_file:
            response['status'] = 'fail'
            response['message'] = 'Unable to delete the item.'
            response['list_id'] = list_id
            response['item_id'] = item_id
        else:
            response['status'] = 'success'
            response['message'] = 'Item deleted.'
            response['list_id'] = list_id
            response['item_id'] = item_id


    def get_list_items(
            self,
            list_id = ''
        ) -> str:
        """Get all items in a list.
        Args:
            list_id (str):  The ID of the todo list.
        Returns:
            str:    A JSON string containing the list items in this format:
                    {"status": "<success|fail:str>", "message": "<message:str>",
                    "list_id": "<list_id:str>", "items": [
                        {"id": "<item_id:int>", "name": "<item_name:str>",
                        "status": "<item_status:str>"},
                        ...
                    ]}
        """

        # Variables
        response = self.RESPONSE_LIST_ITEMS_JSON.copy()

        # Type-check list_id
        if not isinstance(list_id, str):
            try:
                list_id = str(list_id)
            except:
                raise TypeError('list_id must be a string.')
        
        # Build file name and path
        list_file_path = self.build_file_path(list_id)

        # Load the list
        list_content = self.read_list_file(list_file_path)

        if list_content is None:
            response['status'] = 'fail'
            response['message'] = 'Unable to load the list.'
            response['list_id'] = list_id
            return json.dumps(response)
        
        # Test for list items
        if 'items' not in list_content or len(list_content['items']) == 0:
            response['status'] = 'success'
            response['message'] = 'List has no items.'
            response['list_id'] = list_id
            response['items'] = []
            return json.dumps(response)
        else:
            response['status'] = 'success'
            response['message'] = 'List items loaded.'
            response['list_id'] = list_id
            response['items'] = list_content['items']
            return json.dumps(response)
        

    def get_next_list_item(
            self,
            list_id = ''
        ) -> str:
        """Get the next available list item ID.
        Args:
            list_id (str):  The ID of the todo list.
        Returns:
            str:    A JSON string containing the next available list item ID
                    in this format:
                    {"status": "<success|fail:str>", "message": "<message:str>",
                    "list_id": "<list_id:str>", "item_id": "<item_id:int>"}
        """

        # Variables
        response = self.RESPONSE_ITEM_JSON.copy()

        # Type-check list_id
        if not isinstance(list_id, str):
            try:
                list_id = str(list_id)
            except:
                raise TypeError('list_id must be a string.')
            
        # Build file name and path
        list_file_path = self.build_file_path(list_id)

        # Load the list
        list_content = self.read_list_file(list_file_path)

        if list_content is None:
            response['status'] = 'fail'
            response['message'] = 'Unable to load the list.'
            response['list_id'] = list_id
            return json.dumps(response)
        
        # Test for list items
        if 'items' not in list_content or len(list_content['items']) == 0:
            response['status'] = 'success'
            response['message'] = 'List has no items.'
            response['list_id'] = list_id
            response['item_id'] = None
            return json.dumps(response)
        else:
            # If the list order is self.LIST_TYPE_ORDERED, get the first
            # available item. if the list order is self.LIST_TYPE_UNORDERED,
            # get a random available item. Otherwise, return an error.
            if list_content['order'] == self.LIST_TYPE_ORDERED:
                # get the first item
                response['status'] = 'success'
                response['message'] = 'Description: ' + list_content['items'][0]['description']
                response['list_id'] = list_id
                response['item_id'] = list_content['items'][0]['id']
                return json.dumps(response)
            elif list_content['order'] == self.LIST_TYPE_UNORDERED:
                # get a random item, and delete it from the list
                item_index = random.randint(0, len(list_content['items']) - 1)
                response['status'] = 'success'
                response['message'] = 'Description: ' + list_content['items'][item_index]['description']
                response['list_id'] = list_id
                response['item_id'] = list_content['items'][item_index]['id']
                return json.dumps(response)
            else:
                response['status'] = 'fail'
                response['message'] = 'Invalid list order.'
                response['list_id'] = list_id
                response['item_id'] = None
                return json.dumps(response)


    def mark_list_as_done(
            self,
            list_id = ''
        ) -> str:
        """Mark a list as done.
        Args:
            list_id (str):  The ID of the todo list.
        Returns:
            str:    A JSON string containing the list ID in this format:
                    {"status": "<success|fail:str>", "message": "<message:str>",
                    "list_id": "<list_id:str>"}
        """

        # Variables
        response = self.RESPONSE_LIST_JSON.copy()

        # Type-check list_id
        if not isinstance(list_id, str):
            try:
                list_id = str(list_id)
            except:
                raise TypeError('list_id must be a string.')
            
        # Build file name and path
        list_file_path = self.build_file_path(list_id)

        # Load the list
        list_content = self.read_list_file(list_file_path)
        if list_content is None:
            response['status'] = 'fail'
            response['message'] = 'Unable to load the list.'
            response['list_id'] = list_id
            return json.dumps(response)
        
        # Iterate through all items and set as self.LIST_ITEM_STATUS_COMPLETE
        for item in list_content['items']:
            item['status'] = self.LIST_ITEM_STATUS_COMPLETE

        # Write the list
        write_to_file = self.write_list_file(list_file_path, list_content)

        if write_to_file is False:
            response['status'] = 'fail'
            response['message'] = 'Unable to write to the list.'
            response['list_id'] = list_id
            return json.dumps(response)
        else:
            response['status'] = 'success'
            response['message'] = 'List marked as done.'
            response['list_id'] = list_id
            return json.dumps(response)

