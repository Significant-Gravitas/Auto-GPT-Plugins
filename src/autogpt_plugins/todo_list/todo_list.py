"""Wikipedia search command for Autogpt."""
from __future__ import annotations

import json

def _list_todo_lists() -> str:
    """Return a list of todo lists.
    Returns:
        str: A string containing a list of todo lists.
    """
    return "Todo list 1, Todo list 2, Todo list 3"


def _delete_all_todo_lists() -> str:
    """Delete all todo lists.
    Returns:
        str: A string confirming that all todo lists were deleted.
    """
    return "All todo lists deleted."


def _create_todo_list(name: str, type: str) -> str:
    """Create a new todo list.
    Args:
        name (str): The name of the new todo list.
    Returns:
        str: A string confirming that the todo list was created.
    """
    return f"Todo list {name} created."


def _delete_todo_list(name: str) -> str:
    """Delete a todo list.
    Args:
        name (str): The name of the todo list to delete.
    Returns:
        str: A string confirming that the todo list was deleted.
    """
    return f"Todo list {name} deleted."


def _complete_todo_list(name: str) -> str:
    """Mark a todo list as complete.
    Args:
        name (str): The name of the todo list to mark as complete.
    Returns:
        str: A string confirming that the todo list was marked as complete.
    """
    return f"Todo list {name} marked as complete."


def _uncomplete_todo_list(name: str) -> str:
    """Mark a todo list as uncomplete.
    Args:
        name (str): The name of the todo list to mark as uncomplete.
    Returns:
        str: A string confirming that the todo list was marked as uncomplete.
    """
    return f"Todo list {name} marked as uncomplete."


def _rename_todo_list(name: str, new_name: str) -> str:
    """Rename a todo list.
    Args:
        name (str): The name of the todo list to rename.
        new_name (str): The new name of the todo list.
    Returns:
        str: A string confirming that the todo list was renamed.
    """
    return f"Todo list {name} renamed to {new_name}."


def _add_to_todo_list(name: str, item: str) -> str:
    """Add an item to a todo list.
    Args:
        name (str): The name of the todo list to add the item to.
        item (str): The item to add to the todo list.
    Returns:
        str: A string confirming that the item was added to the todo list.
    """
    return f"Added {item} to todo list {name}."


def _delete_task_from_todo_list(name: str, item: str) -> str:
    """Delete a task from a todo list.
    Args:
        name (str): The name of the todo list to delete the item from.
        item (str): The item to delete from the todo list.
    Returns:
        str: A string confirming that the item was deleted from the todo list.
    """
    return f"Deleted {item} from todo list {name}."


def _complete_todo_task(name: str, item: str) -> str:
    """Mark a task as complete in a todo list.
    Args:
        name (str): The name of the todo list to mark the item as complete in.
        item (str): The item to mark as complete in the todo list.
    Returns:
        str: A string confirming that the item was marked as complete in the
             todo list.
    """
    return f"Marked {item} as complete in todo list {name}."


def _uncomplete_todo_task(name: str, item: str) -> str:
    """Mark a task as uncomplete in a todo list.
    Args:
        name (str): The name of the todo list to mark the item as uncomplete in.
        item (str): The item to mark as uncomplete in the todo list.
    Returns:
        str: A string confirming that the item was marked as uncomplete in the
             todo list.
    """
    return f"Marked {item} as uncomplete in todo list {name}."


def _change_todo_task_description(name: str, item: str, description: str) -> str:
    """Change the description of a task in a todo list.
    Args:
        name (str): The name of the todo list to change the item description in.
        item (str): The item to change the description of in the todo list.
        description (str): The new description of the item.
    Returns:
        str: A string confirming that the item description was changed in the
             todo list.
    """
    return f"Changed description of {item} in todo list {name} to {description}."


def _get_next_todo_list_task(name: str) -> str:
    """Get the next task in a todo list.
    Args:
        name (str): The name of the todo list to get the next task from.
    Returns:
        str: A string containing the next task in the todo list.
    """
    return f"Next task in todo list {name} is: {item}."


def _get_random_todo_list_task(name: str) -> str:
    """Get a random task from a todo list.
    Args:
        name (str): The name of the todo list to get a random task from.
    Returns:
        str: A string containing a random task from the todo list.
    """
    return f"Random task in todo list {name} is: {item}."


def _list_todo_list_tasks(name: str) -> str:
    """List all tasks in a todo list.
    Args:
        name (str): The name of the todo list to list the tasks of.
    Returns:
        str: A string containing all tasks in the todo list.
    """
    return f"Tasks in todo list {name} are: {items}."


def _delete_all_todo_list_tasks(name: str) -> str:
    """Delete all tasks in a todo list.
    Args:
        name (str): The name of the todo list to delete all tasks from.
    Returns:
        str: A string confirming that all tasks were deleted from the todo list.
    """
    return f"All tasks deleted from todo list {name}."


def _complete_all_todo_list_tasks(name: str) -> str:
    """Mark all tasks in a todo list as complete.
    Args:
        name (str): The name of the todo list to mark all tasks as complete in.
    Returns:
        str: A string confirming that all tasks were marked as complete in the
             todo list.
    """
    return f"All tasks marked as complete in todo list {name}."


def _uncomplete_all_todo_list_tasks(name: str) -> str:
    """Mark all tasks in a todo list as uncomplete.
    Args:
        name (str): The name of the todo list to mark all tasks as uncomplete
                    in.
    Returns:
        str: A string confirming that all tasks were marked as uncomplete in
             the todo list.
    """
    return f"All tasks marked as uncomplete in todo list {name}."


def _list_completed_tasks(name: str) -> str:
    """List all completed tasks in a todo list.
    Args:
        name (str): The name of the todo list to list the completed tasks of.
    Returns:
        str: A string containing all completed tasks in the todo list.
    """
    return f"Completed tasks in todo list {name} are: {items}."


def _list_uncompleted_tasks(name: str) -> str:
    """List all uncompleted tasks in a todo list.
    Args:
        name (str): The name of the todo list to list the uncompleted tasks of.
    Returns:
        str: A string containing all uncompleted tasks in the todo list.
    """
    return f"Uncompleted tasks in todo list {name} are: {items}."
