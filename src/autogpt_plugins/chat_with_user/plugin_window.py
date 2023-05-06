import tkinter as tk
import queue
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
        if not agent_name or agent_name.strip() == '':
            agent_name = 'AutoGPT'

        # Window stuff
        self.agent_name = agent_name
        self.on_message = on_message
        self.on_close = on_close

        # Window stuff
        self.window = tk.Tk()
        self.window.title("Chat with User")
        self.window.configure(bg="white")

        self.text_frame = tk.Frame(self.window, padx=10, pady=10)
        self.text_frame.pack(fill="both", expand=True)

        self.text_widget = tk.Text(
            self.text_frame,
            font=("Arial", 12),
            wrap="word",
            bg="white",
            fg="black",
            insertbackground="black"
        )
        self.text_widget.pack(fill="both", expand=True)

        self.entry_frame = tk.Frame(self.window, padx=10, pady=10)
        self.entry_frame.pack(fill="x")

        self.entry_widget = tk.Entry(self.entry_frame, font=("Arial", 12))
        self.entry_widget.pack(side="left", fill="x", expand=True)

        self.send_button = tk.Button(
            self.entry_frame,
            text="Send",
            command=self.send_message,
            cursor="hand2"
        )
        self.send_button.pack(side="left")

        # Window bindings
        self.window.protocol("WM_DELETE_WINDOW", self.window_destroy)
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

        self.on_close()
        self.window.destroy()
        self.window.quit()

    # End of window_destroy method


# End of ChatWithUserPluginWindow class