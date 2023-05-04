"""Chat With User Class for the plugin."""
from __future__ import annotations

import json
import re
import tkinter as tk
import threading
import time

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
        self.message = None
        self.timer = None
        self.is_message_received = False

        # Configure the widgets
        self.text_widget.pack()
        self.entry_widget.pack()
        self.send_button.pack()

    # End of __init__


    def handle_new_message(self) -> None:
        """Handle a new message from the user."""

        self.message = self.entry_widget.get()
        self.text_widget.insert(tk.END, "User: " + self.message + "\n")
        self.entry_widget.delete(0, tk.END)
        self.timer.cancel()
        self.is_message_received = True

    # End of handle_new_message


    def handle_new_message(self) -> None:
        """Handle a new message from the user."""

        self.message = self.entry_widget.get()
        self.text_widget.insert(tk.END, "User: " + self.message + "\n")
        self.entry_widget.delete(0, tk.END)
        self.timer.cancel()
        self.window.quit()

    # End of handle_new_message


    def handle_window_close(self):
        """Handle the window closing."""

        self.window = None
        self.entry_widget = None
        self.text_widget = None
        self.send_button = None

    # End of handle_window_close


    def create_chat_window(self):
        """Create a chat window."""

        if not self.is_window_open:
            self.window = tk.Tk()
            self.entry_widget = tk.Entry(self.window)
            self.text_widget = tk.Text(self.window)
            self.send_button = tk.Button(self.window, text="Send", command=self.handle_new_message)
            self.text_widget.pack()
            self.entry_widget.pack()
            self.send_button.pack()
            self.window.bind("<Destroy>", self.handle_window_close)
            self.is_window_open = True

    # End of create_chat_window


    def timer_expired(self):
        self.is_message_received = False

    # End of timer_expired


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
        Args:
            agent_name (str): The name of the agent.
            message (str): The message to send.
        Returns:
            str: The resulting response.
        """

        self.message = None

        if not self.is_window_open:
            self.create_chat_window()

        self.text_widget.insert(tk.END, agent_name + ": " + message + "\n")
        self.timer = threading.Timer(120, self.timer_expired)
        self.timer.start()

        while not self.is_message_received:
            self.window.update()
            time.sleep(0.2)
            
        self.is_message_received = False

        return self.message if self.message else "No response"

    # End of chat_with_user

        
