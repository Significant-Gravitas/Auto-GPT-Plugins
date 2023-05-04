"""Chat With User Class for the plugin."""
import tkinter as tk
import threading

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
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    # End of __init__


    def run(
        self
    ):
        """Run the window."""

        self.window.mainloop()

    # End of run


    def send_message(
        self
    ):
        """Send a message."""

        message = self.entry_widget.get()
        self.entry_widget.delete(0, tk.END)
        self.text_widget.insert(tk.END, "User: " + message + "\n")
        self.on_message(message)

    # End of send_message


    def receive_message(
        self, 
        message
    ):
        """Receive a message."""

        self.text_widget.insert(tk.END, self.agent_name + ": " + message + "\n")

    # End of receive_message


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
        self
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

        if self.window is None:
            self.window = ChatWithUserPluginWindow(agent_name, self.handle_new_message, self.handle_window_close)

        self.window.receive_message(message)

        self.message_event.wait(timeout)
        self.message_event.clear()

        return self.message if self.message else "No response"

    # End of chat_with_user

        
