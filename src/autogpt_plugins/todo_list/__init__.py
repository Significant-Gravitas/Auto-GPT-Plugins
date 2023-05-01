"""Todo List for Agents."""

from typing import Any, Dict, List, Optional, Tuple, TypedDict, TypeVar

from auto_gpt_plugin_template import AutoGPTPluginTemplate
from .todo_list import _todo_list

PromptGenerator = TypeVar("PromptGenerator")


class Message(TypedDict):
    role: str
    content: str


class AutoGPTTodoList(AutoGPTPluginTemplate):
    """
    Todo List Agent Tool.
    """

    def __init__(self):
        super().__init__()
        self._name = "autogpt-todo-list"
        self._version = "0.1.0"
        self._description = "AutoGPT can track tasks in a structured JSON file."

    def can_handle_on_response(self) -> bool:
        """This method is called to check that the plugin can
        handle the on_response method.
        Returns:
            bool: True if the plugin can handle the on_response method."""
        return False

    def on_response(self, response: str, *args, **kwargs) -> str:
        """This method is called when a response is received from the model."""
        pass

    def can_handle_post_prompt(self) -> bool:
        """This method is called to check that the plugin can
        handle the post_prompt method.
        Returns:
            bool: True if the plugin can handle the post_prompt method."""
        return True

    def can_handle_on_planning(self) -> bool:
        """This method is called to check that the plugin can
        handle the on_planning method.
        Returns:
            bool: True if the plugin can handle the on_planning method."""
        return False

    def on_planning(
            self, prompt: PromptGenerator, messages: List[str]
    ) -> Optional[str]:
        """This method is called before the planning chat completeion is done.
        Args:
            prompt (PromptGenerator): The prompt generator.
            messages (List[str]): The list of messages.
        """
        pass

    def can_handle_post_planning(self) -> bool:
        """This method is called to check that the plugin can
        handle the post_planning method.
        Returns:
            bool: True if the plugin can handle the post_planning method."""
        return False

    def post_planning(self, response: str) -> str:
        """This method is called after the planning chat completeion is done.
        Args:
            response (str): The response.
        Returns:
            str: The resulting response.
        """
        pass

    def can_handle_pre_instruction(self) -> bool:
        """This method is called to check that the plugin can
        handle the pre_instruction method.
        Returns:
            bool: True if the plugin can handle the pre_instruction method."""
        return False

    def pre_instruction(self, messages: List[str]) -> List[str]:
        """This method is called before the instruction chat is done.
        Args:
            messages (List[str]): The list of context messages.
        Returns:
            List[str]: The resulting list of messages.
        """
        pass

    def can_handle_on_instruction(self) -> bool:
        """This method is called to check that the plugin can
        handle the on_instruction method.
        Returns:
            bool: True if the plugin can handle the on_instruction method."""
        return False

    def on_instruction(self, messages: List[str]) -> Optional[str]:
        """This method is called when the instruction chat is done.
        Args:
            messages (List[str]): The list of context messages.
        Returns:
            Optional[str]: The resulting message.
        """
        pass

    def can_handle_post_instruction(self) -> bool:
        """This method is called to check that the plugin can
        handle the post_instruction method.
        Returns:
            bool: True if the plugin can handle the post_instruction method."""
        return False

    def post_instruction(self, response: str) -> str:
        """This method is called after the instruction chat is done.
        Args:
            response (str): The response.
        Returns:
            str: The resulting response.
        """
        pass

    def can_handle_pre_command(self) -> bool:
        """This method is called to check that the plugin can
        handle the pre_command method.
        Returns:
            bool: True if the plugin can handle the pre_command method."""
        return False

    def pre_command(
            self, command_name: str, arguments: Dict[str, Any]
    ) -> Tuple[str, Dict[str, Any]]:
        """This method is called before the command is executed.
        Args:
            command_name (str): The command name.
            arguments (Dict[str, Any]): The arguments.
        Returns:
            Tuple[str, Dict[str, Any]]: The command name and the arguments.
        """
        pass

    def can_handle_post_command(self) -> bool:
        """This method is called to check that the plugin can
        handle the post_command method.
        Returns:
            bool: True if the plugin can handle the post_command method."""
        return False

    def post_command(self, command_name: str, response: str) -> str:
        """This method is called after the command is executed.
        Args:
            command_name (str): The command name.
            response (str): The response.
        Returns:
            str: The resulting response.
        """
        pass

    def can_handle_chat_completion(
            self,
            messages: list[Dict[Any, Any]],
            model: str,
            temperature: float,
            max_tokens: int,
    ) -> bool:
        """This method is called to check that the plugin can
        handle the chat_completion method.
        Args:
            messages (Dict[Any, Any]): The messages.
            model (str): The model name.
            temperature (float): The temperature.
            max_tokens (int): The max tokens.
        Returns:
            bool: True if the plugin can handle the chat_completion method."""
        return False

    def handle_chat_completion(
            self,
            messages: list[Dict[Any, Any]],
            model: str,
            temperature: float,
            max_tokens: int,
    ) -> str:
        """This method is called when the chat completion is done.
        Args:
            messages (Dict[Any, Any]): The messages.
            model (str): The model name.
            temperature (float): The temperature.
            max_tokens (int): The max tokens.
        Returns:
            str: The resulting response.
        """
        return None

    def post_prompt(self, prompt: PromptGenerator) -> PromptGenerator:
        """This method is called just after the generate_prompt is called,
            but actually before the prompt is generated.
        Args:
            prompt (PromptGenerator): The prompt generator.
        Returns:
            PromptGenerator: The prompt generator.
        """

        # All todo lists
        prompt.add_command(
            "list_todo_lists",
            "List Todo Lists",
            {},
            _list_todo_lists
        )
        prompt.add_command(
            "delete_all_todo_lists",
            "Delete All Todo Lists",
            {},
            _delete_all_todo_lists
        )

        # Todo list functions
        prompt.add_command(
            "create_todo_list",
            "Create Todo List",
            {"name": "<name>", "type": "<style>"},
            _create_todo_list
        )
        prompt.add_command(
            "delete_todo_list",
            "Delete Todo List",
            {"todolist_id": "<todolist_id>"},
            _delete_todo_list
        )
        prompt.add_command(
            "complete_todo_list",
            "Complete Todo List",
            {"todolist_id": "<todolist_id>"},
            _complete_todo_list
        )
        prompt.add_command(
            "uncomplete_todo_list",
            "Uncomplete Todo List",
            {"todolist_id": "<todolist_id>"},
            _uncomplete_todo_list
        )
        prompt.add_command(
            "rename_todo_list",
            "Rename Todo List",
            {"todolist_id": "<todolist_id>", "name": "<name>"},
            _rename_todo_list
        )

        # Todo task functions
        prompt.add_command(
            "add_to_todo_list",
            "Add to Todo List",
            {"todolist_id": "<todolist_id>", "description": "<description>"},
            _add_to_todo_list
        )
        prompt.add_command(
            "delete_task_from_todo_list",
            "Delete Task from Todo List",
            {"todolist_id": "<todolist_id>", "task_id": "<task_id>"},
            _delete_task_from_todo_list
        )
        prompt.add_command(
            "complete_todo_task",
            "Complete Todo Task",
            {"todolist_id": "<todolist_id>", "task_id": "<task_id>"},
            _complete_todo_task
        )
        prompt.add_command(
            "uncomplete_todo_task",
            "Uncomplete Todo Task",
            {"todolist_id": "<todolist_id>", "task_id": "<task_id>"},
            _uncomplete_todo_task
        )
        prompt.add_command(
            "change_todo_task_description",
            "Change Todo Task Description",
            {"todolist_id": "<todolist_id>", "task_id": "<task_id>", "description": "<description>"},
            _change_todo_task_description
        )
        prompt.add_command(
            "get_next_todo_list_task",
            "Get Next Todo List Task",
            {"todolist_id": "<todolist_id>"},
            _get_next_todo_list_task
        )
        prompt.add_command(
            "get_random_todo_list_task",
            "Get Random Todo List Task",
            {"todolist_id": "<todolist_id>"},
            _get_random_todo_list_task
        )

        # Todo list bulk task functions
        prompt.add_command(
            "list_todo_list_tasks",
            "List Todo List Tasks",
            {"todolist_id": "<todolist_id>"},
            _list_todo_list_tasks
        )
        prompt.add_command(
            "delete_all_todo_list_tasks",
            "Delete All Todo List Tasks",
            {"todolist_id": "<todolist_id>"},
            _delete_all_todo_list_tasks
        )
        prompt.add_command(
            "complete_all_todo_list_tasks",
            "Complete All Todo List Tasks",
            {"todolist_id": "<todolist_id>"},
            _complete_all_todo_list_tasks
        )
        prompt.add_command(
            "uncomplete_all_todo_list_tasks",
            "Uncomplete All Todo List Tasks",
            {"todolist_id": "<todolist_id>"},
            _uncomplete_all_todo_list_tasks
        )
        prompt_add_command(
            "list_completed_tasks",
            "List Completed Tasks",
            {"todolist_id": "<todolist_id>"},
            _list_completed_tasks
        )
        prompt.add_command(
            "list_uncompleted_tasks",
            "List Uncompleted Tasks",
            {"todolist_id": "<todolist_id>"},
            _list_uncompleted_tasks
        )

        return prompt
