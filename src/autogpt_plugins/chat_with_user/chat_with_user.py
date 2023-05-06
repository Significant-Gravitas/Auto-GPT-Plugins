import threading

from .plugin_window import ChatWithUserPluginWindow

class ChatWithUserPlugin:
    """This class is used to create the chat window."""

    def __init__(
        self, 
        plugin
    ) -> None:
        """This method is called when the chat completion is done.
        Args:
            plugin (AutoGPTPlugin): The plugin.
        """

        # Constants
        self.DEFAULT_AGENT_NAME = 'AutoGPT'
        self.DEFAULT_MESSAGE = ''
        self.DEFAULT_TIMEOUT = 120

        # Variables
        self.plugin = plugin
        self.window = None
        self.window_open = False
        self.message_event = threading.Event()
        self.window_created_event = threading.Event()
        self.message = None

    # End of __init__ method


    def handle_new_message(
        self, 
        message:str = ''
    ) -> None:
        """This method is called to handle the new message.
        Args:
            message (str): The message.
        """

        self.message = message
        self.message_event.set()

    # End of handle_new_message method


    def handle_window_close(
        self
    ) -> None:
        """This method is called to handle the window close."""

        self.window_open = False
        self.window = None
        self.message = "User closed the window."
        self.message_event.set()
        self.window_created_event.clear()

    # End of handle_window_close method


    def run_chat_window(
        self, 
        agent_name:str = 'AutoGPT'
    ) -> None:
        """This method is called to run the chat window.
        Args:
            agent_name (str): The name of the agent.
        """

        self.message = None
        self.message_event.clear()
        self.window = ChatWithUserPluginWindow(agent_name, self.handle_new_message, self.handle_window_close)
        self.window_open = True
        self.window_created_event.set()
        self.window.run()
        
    # End of run_chat_window method


    def clean_string(
        self,
        string:str = ''
    ) -> str:
        """Strip control code characters and other nasty
        bits from the string.
        Args:
            string (str): The string to clean.
        Returns:
            str: The cleaned string.
        """

        remove_chars = dict.fromkeys(range(32), None)
        table = str.maketrans(remove_chars)

        return string.translate(table)

    # End of clean_string method


    def chat_with_user(
        self, 
        agent_name = 'AutoGPT', 
        message = '', 
        timeout = 120
    ) -> str:
        """This method is called to chat with the user.
        Args:
            agent_name (str): The name of the agent.
            message (str): The message to send.
            timeout (int|False): The timeout for the response.
        Returns:
            str: The response from the user.
        """

        # Type-check and clean agent_name
        if not agent_name:
            agent_name = self.DEFAULT_AGENT_NAME
        elif not isinstance(agent_name, str):
            agent_name = str(agent_name)
        agent_name = self.clean_string(agent_name)

        # Type-check and clean message
        if not message:
            message = self.DEFAULT_MESSAGE
        elif not isinstance(message, str):
            message = str(message)
        message = self.clean_string(message)

        # Type-check timeout
        if timeout in [False, '']:
            timeout = None
        else:
            if not isinstance(timeout, int):
                try:
                    timeout = int(timeout)
                except:
                    timeout = self.DEFAULT_TIMEOUT
        

        if not self.window_open:
            # If the window is not open, create a new one.
            threading.Thread(target=self.run_chat_window, args=(agent_name,), daemon=True).start()
            self.window_created_event.wait()

        # Send the message to the existing window.
        if self.window_open:
            self.window.receive_message(message)
            self.message_event.wait(timeout)
            self.message_event.clear()

        # Send the message to the existing window.
        if not self.window_open:
            return '"User closed the window. Re-open to continue conversation?"'
        return f'"{self.message}"' if self.message else '"No response from user. Timeout too short?"'
    
    # End of chat_with_user method

# End of ChatWithUserPlugin class