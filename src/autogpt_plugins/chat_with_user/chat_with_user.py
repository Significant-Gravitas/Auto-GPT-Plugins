"""Chat With User Class for the plugin."""
from __future__ import annotations

import json
import re
import tkinter as tk

class ChatWithUserPlugin:
    """Chat With User Plugin Class."""


    def __init__(self, plugin):

        # Save the plugin
        self.plugin = plugin

        # Create a window
        self.window = None
        self.entry_widget = None
        self.text_widget = None
        self.send_button = None
        self.is_window_open = False

        # Configure the widgets
        self.text_widget.pack()
        self.entry_widget.pack()
        self.send_button.pack()

    # End of __init__


    def handle_new_message(self) -> None:
        """Handle a new message from the user."""

        # Get the message from the entry widget
        message = self.entry_widget.get()

        # Add the message to the text widget
        self.text_widget.insert(tk.END, "User: " + message + "\n")

        # Clear the entry widget
        self.entry_widget.delete(0, tk.END)

    # End of handle_new_message


    def handle_window_close(self):
        """Handle the window closing."""

        self.is_window_open = False

    # End of handle_window_close


    def create_chat_window(self):
        """Create a chat window."""

        if not self.is_window_open:
            self.window = tk.Tk()
            self.entry_widget = tk.Entry(self.window)
            self.text_widget = tk.Text(self.window)
            self.send_button = tk.Button(self.window, text="Send", command=self.handle_new_message)

            # Configure the widgets
            self.text_widget.pack()
            self.entry_widget.pack()
            self.send_button.pack()

            # Bind the window's <Destroy> event to handle_window_close
            self.window.bind("<Destroy>", self.handle_window_close)
            self.is_window_open = True

    # End of create_chat_window


    def handle_window_close(self, event):
        """Handle the window closing.
        Args:
            event (tkinter.Event): The event.
        """

        self.window = None
        self.entry_widget = None
        self.text_widget = None
        self.send_button = None

    # End of handle_window_close


    def chat_with_user(
        self,
        agent_name = 'AutoGPT',
        message = ''
    ) -> str:
        """Use a desktop window to chat with the user.
        Returns:
            str: The resulting response.
        """

        if not self.is_window_open:
            self.create_chat_window()
            self.window.mainloop()

        self.text_widget.insert(tk.END, agent_name + ": " + message + "\n")

    # End of chat_with_user

        
