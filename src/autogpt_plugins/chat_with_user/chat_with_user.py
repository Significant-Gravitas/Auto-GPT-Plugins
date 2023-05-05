import tkinter as tk
import threading
import queue
import string
from typing import Callable

class ChatWithUserPluginWindow:
    """This class is used to create the chat window."""

    def __init__(
        self, 
        agent_name:str,
        on_message:Callable[[str], None],
        on_close:Callable[[], None]
    ) -> None:
        """This method is called when the chat completion is done.
        Args:
            agent_name (str): The name of the agent.
            on_message (Callable[[str], None]): The on message callback.
            on_close (Callable[[], None]): The on close callback.
        """

        # Check values of agent_name
        if agent_name is None or agent_name == '':
            agent_name = 'AutoGPT'

        # Window stuff
        self.agent_name = agent_name
        self.on_message = on_message

        # Window stuff
        self.window = tk.Tk()
        self.text_widget = tk.Text(self.window)
        self.entry_widget = tk.Entry(self.window)
        self.send_button = tk.Button(self.window, text="Send", command=self.send_message)
        self.text_widget.pack()
        self.entry_widget.pack()
        self.send_button.pack()

        # Window bindings
        self.window.bind("<Destroy>", lambda e: on_close())
        self.message_queue = queue.Queue()
        self.process_incoming_messages()
        self.window.protocol("WM_DELETE_WINDOW", on_close)

    # End of __init__ method


    def process_incoming_messages(
        self
    ) -> None:
        """This method is called to process the incoming messages."""

        while not self.message_queue.empty():
            message = self.message_queue.get()
            self.text_widget.insert(tk.END, self.agent_name + ": " + message + "\n")
        self.window.after(100, self.process_incoming_messages)

    # End of process_incoming_messages method


    def send_message(
        self
    ) -> None:
        """This method is called to send the message."""

        message = self.entry_widget.get()
        self.entry_widget.delete(0, tk.END)
        self.text_widget.insert(tk.END, "User: " + message + "\n")
        self.on_message(message)

    # End of send_message method


    def receive_message(
        self, 
        message:str = ''
    ) -> None:
        """This method is called to receive the message.
        Args:
            message (str): The message.
        """

        self.message_queue.put(message)

    # End of receive_message method


    def run(
        self
    ) -> None:
        """This method is called to run the chat window."""

        self.process_incoming_messages()
        self.window.protocol("WM_DELETE_WINDOW", self.window_destroy)
        self.window.mainloop()

    # End of run method


    def window_destroy(
        self
    ) -> None:
        """This method is called to destroy the window."""

        self.window.destroy()
        self.window.quit()

    # End of window_destroy method


# End of ChatWithUserPluginWindow class


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
            timeout (int): The timeout for the response.
        Returns:
            str: The response from the user.
        """

        # Type-check and clean agent_name
        if not agent_name:
            agent_name = self.DEFAULT_AGENT_NAME.copy()
        elif not isinstance(agent_name, str):
            agent_name = str(agent_name)
        agent_name = self.clean_string(agent_name)

        # Type-check and clean message
        if not message:
            message = self.DEFAULT_MESSAGE.copy()
        elif not isinstance(message, str):
            message = str(message)
        message = self.clean_string(message)

        # Type-check timeout
        if not timeout:
            timeout = self.DEFAULT_TIMEOUT.copy()
        elif not isinstance(timeout, int):
            try:
                timeout = int(timeout)
            except:
                timeout = self.DEFAULT_TIMEOUT.copy()
        

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
            return "User closed the window."
        return self.message if self.message else "No response from user."
    
    # End of chat_with_user method

# End of ChatWithUserPlugin class