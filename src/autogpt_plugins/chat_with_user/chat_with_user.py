import tkinter as tk
import threading
import queue

class ChatWithUserPluginWindow:
    """This class is used to create the chat window."""

    def __init__(
        self, 
        agent_name, 
        on_message, 
        on_close
    ) -> None:
        """This method is called when the chat completion is done.
        Args:
            agent_name (str): The name of the agent.
            on_message (Callable[[str], None]): The on message callback.
            on_close (Callable[[], None]): The on close callback.
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
        message
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
        self.window.mainloop()

    # End of run method

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

        self.plugin = plugin
        self.window = None
        self.message_event = threading.Event()
        self.window_created_event = threading.Event()
        self.message = None

    # End of __init__ method


    def handle_new_message(
        self, 
        message
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

        self.window = None

    # End of handle_window_close method


    def run_chat_window(
        self, 
        agent_name
    ) -> None:
        """This method is called to run the chat window.
        Args:
            agent_name (str): The name of the agent.
        """

        self.window = ChatWithUserPluginWindow(agent_name, self.handle_new_message, self.handle_window_close)
        self.window_created_event.set()
        self.window.run()

    # End of run_chat_window method


    def chat_with_user(
        self, 
        agent_name='AutoGPT', 
        message='', 
        timeout=120
    ) -> str:
        """This method is called to chat with the user.
        Args:
            agent_name (str): The name of the agent.
            message (str): The message to send.
            timeout (int): The timeout for the response.
        Returns:
            str: The response from the user.
        """

        threading.Thread(target=self.run_chat_window, args=(agent_name,), daemon=True).start()

        self.window_created_event.wait()
        self.window.receive_message(message)
        self.message_event.wait(timeout)
        self.message_event.clear()

        return self.message if self.message else "No response"