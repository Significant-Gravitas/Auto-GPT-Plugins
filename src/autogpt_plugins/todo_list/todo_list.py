"""Todo List Plugin Commands."""

import json

class AutoGPTTodoListPluginCommands:

    def create_todo_list(
            name = '',
            style = 'ordered'
    ):
        """Create a new todo list.

        Args:
            name (str):     The name of the todo list.
            style (str):    The style of the todo list. Can be 'ordered' or 'unordered'.

        Returns:
            str:    A JSON string containing the todo list ID and status code.
                    {"status": "success|fail", "todo_list_id": "todo_list_id"}
        """

        # Type-check name
        if not isinstance(name, str):
            try:
                name = str(name)
            except:
                raise TypeError('name must be a string.')
        if name is None or name == '':
            raise ValueError('name cannot be empty.')
        
        # Type-check style
        if not isinstance(style, str):
            try:
                style = str(style)
            except:
                raise TypeError('style must be a string.')
        if style is None or style == '':
            raise ValueError('style cannot be empty.')
        style = style.lower()
        if style not in ['ordered', 'unordered']:
            raise ValueError('style must be "ordered" or "unordered".')
        
        


        # Return the todo list ID and status code.
        return json.dumps({
            'status': 'success',
            'todo_list_id': todo_list_id
        })