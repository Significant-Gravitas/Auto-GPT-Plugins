import queue
import time
import tkinter as tk
import tkinter.font as tkFont
from typing import Callable


class ChatWithUserPluginWindow:
    """This class is used to create the chat window."""

    def __init__(self, agent_name:str, on_message:Callable[[str], None], on_close:Callable[[], None], allow_close:bool = True) -> None:
        """
        This method is called when the chat completion is done.
        Args:
            agent_name (str)                      : The name of the agent.
            on_message (Callable[[str], None])    : The on message callback.
            on_close (Callable[[], None])         : The on close callback.
        """

        # Constants
        self.DEFAULT_CHAT_LIMIT = 300

        # Check values of agent_name
        if not agent_name or agent_name.strip() == '':
            agent_name = 'AutoGPT'

        # Variables
        self.agent_name = agent_name
        self.on_message = on_message
        self.on_close = on_close
        self.allow_close = allow_close

        # Window stuff
        self.window = tk.Tk()
        self.window.title("Chat with " + self.agent_name)
        self.window.configure(bg="white")

        # AFK Toggle
        self.afk_var = tk.IntVar()
        afk_frame = tk.Frame(self.window)
        afk_frame.pack(side="top", fill="x")
        self.afk_checkbutton = tk.Checkbutton(afk_frame, text="Enable AFK", variable=self.afk_var)
        self.afk_checkbutton.pack(side="left")

        # Text widget
        self.text_frame = tk.Frame(self.window, padx=10, pady=10)
        self.text_frame.pack(fill="both", expand=True)
        self.text_widget = tk.Text(
            self.text_frame,
            font                = ("Arial", 12),
            wrap                = "word",
            bg                  = "#F5F5F5",
            fg                  = "black",
            insertbackground    = "black"
        )
        self.text_widget.pack(fill="both", expand=True)

        # Frame setup
        self.entry_frame = tk.Frame(self.window, padx=10, pady=10)
        self.entry_frame.pack(fill="x")

        # Fonts for chat
        self.entry_widget = tk.Text(self.entry_frame, font=("Arial", 12), height=3)
        self.entry_widget.pack(side="left", fill="x", expand=True)

        # User labels
        self.bold_font = tkFont.Font(family="Arial", size=12, weight="bold")
        self.text_widget.tag_configure('user', font=self.bold_font)
        self.text_widget.tag_configure('agent', font=self.bold_font)

        # Send button
        self.send_button = tk.Button(
            self.entry_frame,
            text="✈️",
            command=self.send_message,
            cursor="hand2"
        )
        self.send_button.pack(side="left")

        # Window bindings
        self.window.protocol("WM_DELETE_WINDOW", self.window_destroy)
        self.message_queue = queue.Queue()
        self.process_incoming_messages()
        self.entry_widget.bind("<KeyRelease>", self.limit_chars)
        self.entry_widget.bind("<Return>", self.handle_return_key)

        # Time stuff
        self.message_received_time = None

    # End of __init__ method


    def allow_window_close(self) -> None:
        """Allow the window to be closed."""

        self.allow_close = True

    # End of allow_window_close method


    def limit_chars(self, event:tk.Event) -> None:
        """Limit text in entry widget to 200 characters"""

        value = self.entry_widget.get("1.0", "end-1c")
        if len(value) > self.DEFAULT_CHAT_LIMIT:
            self.entry_widget.delete("1.0", "end")
            self.entry_widget.insert("end", value[:self.DEFAULT_CHAT_LIMIT])

    # End of limit_chars method


    def handle_return_key(self, event:tk.Event) -> str:
        """Handle the Return key press event."""
        
        # Send the message
        self.send_message()
        
        # Stop the default behavior of creating a new line
        return "break"
    
    # End of handle_return_key method


    def process_incoming_messages(self) -> None:
        """This method is called to process the incoming messages."""

        while not self.message_queue.empty():
            message = self.message_queue.get()

            # Insert agent's name with 'agent' tag
            self.text_widget.insert(tk.END, "\n» ", 'agent')
            self.text_widget.insert(tk.END, self.agent_name + ": ", 'agent')
            self.text_widget.insert(tk.END, message + "\n")

            self.text_widget.see(tk.END)

        self.window.after(100, self.process_incoming_messages)

    # End of process_incoming_messages method


    def send_message(self) -> None:
        """This method is called to send the message."""

        # Time stuff
        if isinstance(self.message_received_time, float):
            response_time = time.time() - self.message_received_time
        else:
            response_time = 0
        hours, rem = divmod(response_time, 3600)
        minutes, seconds = divmod(rem, 60)
        timestamp = f"Elapsed: {int(hours)}hr {int(minutes)}min {seconds:.2f}sec"

        # Get message from entry widget
        message = self.entry_widget.get('1.0', 'end-1c')
        self.entry_widget.delete("1.0", tk.END)

        # Insert 'User' with 'user' tag
        self.text_widget.insert(tk.END, "\n« ", 'user')
        self.text_widget.insert(tk.END, "User: ", 'user')
        self.text_widget.insert(tk.END, message + "\n")

        # Scroll to the end of the text widget
        self.text_widget.see(tk.END)

        # Send the message
        self.on_message('"' + message + '" \n' + timestamp)

    # End of send_message method


    def receive_message(self, message:str='', message_received_time:float|None = None) -> None:
        """
        This method is called to receive the message.
        Args:
            message (str)                   : The message.
            message_received_time (float)   : The time the message was received.
        """

        if message_received_time is not None:
            self.message_received_time = message_received_time
        else:
            self.message_received_time = time.time()
        self.message_queue.put(message)

        # Handle AFK
        if self.afk_var.get() == 1:
            self.entry_widget.delete('1.0', tk.END)
            self.entry_widget.insert(tk.END, "<User is AFK>")
            self.send_message()

    # End of receive_message method


    def run(self) -> None:
        """This method is called to run the chat window."""

        self.process_incoming_messages()
        self.window.protocol("WM_DELETE_WINDOW", self.window_destroy)
        self.window.mainloop()

    # End of run method


    def update_agent_name(self, new_name: str) -> None:
        """Update the agent name and the window title."""

        self.agent_name = new_name
        self.window.title(f"Chat with {new_name}")

    # End of update_agent_name method


    def window_destroy(self) -> None:
        """This method is called to destroy the window."""

        if self.allow_close:
            self.on_close()
            self.window.destroy()
            self.window.quit()

    # End of window_destroy method


# End of ChatWithUserPluginWindow class