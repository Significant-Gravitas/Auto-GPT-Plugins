"""Chat With User Class for the plugin."""
import queue
import tkinter as tk
import threading
import time

class ChatWithUserPluginWindow:

    def __init__(
        self,
        agent_name,
        on_message,
        on_close
    ):
        """Create a chat window.
        Args:
            agent_name (str): The name of the agent.
            on_message (function): The on message function.
            on_close (function): The on close function.
        """

        self.window = tk.Tk()
        self.agent_name = agent_name
        self.on_message = on_message
        self.text_widget = tk.Text(self.window)
        self.entry_widget = tk.Entry(self.window)
        self.send_button = tk.Button(self.window, text="Send", command=self.send_message)
        self.text_widget.pack()
        self.entry_widget.pack()
        self.send_button.pack()
        self.window.bind("<Destroy>", lambda e: on_close())
        self.message_queue = queue.Queue()
        self.process_incoming_messages()

    # End of __init__


    def process_incoming_messages(
        self
    ) -> None:
        """Process the incoming messages."""

        while not self.message_queue.empty():
            message = self.message_queue.get()
            self.text_widget.insert(tk.END, self.agent_name + ": " + message + "\n")
        self.window.after(100, self.process_incoming_messages)

    # End of process_incoming_messages


    def send_message(
        self
    ) -> None:
        """Send a message."""

        message = self.entry_widget.get()
        self.entry_widget.delete(0, tk.END)
        self.text_widget.insert(tk.END, "User: " + message + "\n")
        self.on_message(message)

    # End of send_message


    def receive_message(
        self, 
        message
    ) -> None:
        """Receive a message."""

        self.message_queue.put(message)

    # End of receive_message

    
    def run(
        self
    ) -> None:
        """Run the window."""

        self.process_incoming_messages()
        self.window.mainloop()

    # End of run


class ChatWithUserPlugin:
    """Chat With User Plugin Class."""

    def __init__(
        self, 
        plugin
    ):
        """Init the plugin."""

        # Save the plugin
        self.plugin = plugin

        # Create a window
        self.window = None
        self.message_event = threading.Event()
        self.message = None

    # End of __init__


    def handle_new_message(
        self,
        message
    ) -> None:
        """Handle a new message from the user."""

        self.message = message
        self.message_event.set()

    # End of handle_new_message


    def handle_window_close(
        self
    ):
        """Handle the window closing."""

        self.window = None

    # End of handle_window_close


    def run_chat_window(
        self, 
        agent_name
    ) -> None:
        """Run the chat window in the main thread."""

        if self.window is None:
            self.window = ChatWithUserPluginWindow(agent_name, self.handle_new_message, self.handle_window_close)
            self.window.run()

    # End of run_chat_window


    def chat_with_user(
        self,
        agent_name = 'AutoGPT',
        message = '',
        timeout = 120
    ) -> str:
        """Use a desktop window to chat with the user.
        Args:
            agent_name (str): The name of the agent.
            message (str): The message to send.
        Returns:
            str: The resulting response.
        """

        """Chat With User Class for the plugin."""
import tkinter as tk
import threading
import queue

class ChatWithUserPluginWindow:

    def __init__(
        self,
        agent_name,
        on_message,
        on_close
    ):
        """Create a chat window.
        Args:
            agent_name (str): The name of the agent.
            on_message (function): The on message function.
            on_close (function): The on close function.
        """

        self.window = tk.Tk()
        self.agent_name = agent_name
        self.on_message = on_message
        self.text_widget = tk.Text(self.window)
        self.entry_widget = tk.Entry(self.window)
        self.send_button = tk.Button(self.window, text="Send", command=self.send_message)
        self.text_widget.pack()
        self.entry_widget.pack()
        self.send_button.pack()
        self.window.bind("<Destroy>", lambda e: on_close())
        self.message_queue = queue.Queue()
        self.process_incoming_messages()

    # End of __init__


    def process_incoming_messages(
        self
    ) -> None:
        """Process the incoming messages."""

        while not self.message_queue.empty():
            message = self.message_queue.get()
            self.text_widget.insert(tk.END, self.agent_name + ": " + message + "\n")
        self.window.after(100, self.process_incoming_messages)

    # End of process_incoming_messages


    def send_message(
        self
    ) -> None:
        """Send a message."""

        message = self.entry_widget.get()
        self.entry_widget.delete(0, tk.END)
        self.text_widget.insert(tk.END, "User: " + message + "\n")
        self.on_message(message)

    # End of send_message


    def receive_message(
        self, 
        message
    ) -> None:
        """Receive a message."""

        self.message_queue.put(message)

    # End of receive_message

    
    def run(
        self
    ) -> None:
        """Run the window."""

        self.process_incoming_messages()
        self.window.mainloop()

    # End of run


class ChatWithUserPlugin:
    """Chat With User Plugin Class."""

    def __init__(
        self, 
        plugin
    ):
        """Init the plugin."""

        # Save the plugin
        self.plugin = plugin

        # Create a window
        self.window = None
        self.message_event = threading.Event()
        self.message = None

    # End of __init__


    def handle_new_message(
        self,
        message
    ) -> None:
        """Handle a new message from the user."""

        self.message = message
        self.message_event.set()

    # End of handle_new_message


    def handle_window_close(
        self
    ):
        """Handle the window closing."""

        self.window = None

    # End of handle_window_close


    def run_chat_window(
        self, 
        agent_name
    ) -> None:
        """Run the chat window in the main thread."""
        
        if self.window is None:
            self.window = ChatWithUserPluginWindow(agent_name, self.handle_new_message, self.handle_window_close)
            self.window.run()

    # End of run_chat_window


    def chat_with_user(
        self,
        agent_name = 'AutoGPT',
        message = '',
        timeout = 120
    ) -> str:
        """Use a desktop window to chat with the user.
        Args:
            agent_name (str): The name of the agent.
            message (str): The message to send.
        Returns:
            str: The resulting response.
        """

        # Run the chat window in the main thread
        threading.Thread(target=self.run_chat_window, args=(agent_name,), daemon=True).start()

        # Wait for the window to be created
        while self.window is None:
            time.sleep(0.3)  # Introduce a short sleep interval

        # Display the agent's message in the chat window
        self.window.receive_message(message)

        # Wait for the message event and return the message
        self.message_event.wait(timeout)
        self.message_event.clear()
        return self.message if self.message else "No response"
    
    # End of chat_with_user


    
    # End of chat_with_user

