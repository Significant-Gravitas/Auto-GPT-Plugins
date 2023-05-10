"""Wikipedia search command for Autogpt."""
from __future__ import annotations

import json
import sqlite3

class MemoryGraphPlugin:

    def __init__(self, plugin) -> None:
        """Initialize the plugin."""

        super().__init__()
        self.plugin = plugin

        # Create the database
        self.connection = sqlite3.connect("memory_graph.db")
        self.cursor = self.connection.cursor()
        self.create_memory()

    # End of __init__


    def create_memory(self) -> str:
        """Create the database"""

                # Table setup
        self.cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY,
            subject TEXT)
            '''
        )
        self.cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS predicates (
            id INTEGER PRIMARY KEY,
            subject TEXT)
            '''
        )
        self.cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS direction (
            id INTEGER PRIMARY KEY,
            in_id INTEGER,
            out_id INTEGER,
            predicate_id INTEGER,
            FOREIGN KEY (in_id) REFERENCES subjects(id),
            FOREIGN KEY (out_id) REFERENCES subjects(id),
            FOREIGN KEY (predicate_id) REFERENCES predicates(id))
            '''
        )

    # End of create_memory


    def save_data(query:str, value:list) -> int:
        """
        Save data to the database.
        Args:
            query (str): The query to execute.
            value (list): The list of values.
        Returns:
            str: Status message.
        """

        


    def add_memory(self, memories = []) -> str:
        """
        Add memories to the database.
        Args:
            memories (list): The list of memories.
        Returns:
            str: Status message.
        """

        for memory in memories:
            # Make sure values exist
            if not memory["subj"]:
                raise ValueError("Missing subject")
            if not memory["pred"]:
                raise ValueError("Missing predicate")
            if not memory["obj"]:
                raise ValueError("Missing object")

            # Add the memory
            subj = memory["subj"]
            self.cursor.execute("INSERT INTO subjects (subject) VALUES (?)", (subj,))
            subj_jd = self.cursor.fetchone()[0]

            pred = memory["pred"]
            self.cursor.execute("INSERT INTO predicates (predicate) VALUES (?)", (pred,))
            pred_id = self.cursor.fetchone()[0]

            obj = memory["obj"]
            self.cursor.execute("INSERT INTO direction (in_id, out_id, predicate_id) VALUES (?, ?, ?)", (subj_id, pred_id, obj_id))

    # End of add_memory

    def recall_memory(self) -> str:
        pass

    def forget_memory(self) -> str:
        pass
