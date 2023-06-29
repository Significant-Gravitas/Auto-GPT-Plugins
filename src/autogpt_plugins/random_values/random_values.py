"""Random Values classes for Autogpt."""

import json
import random
import string
import uuid

import lorem

"""Random Number function for Autogpt."""

class RandomValues:
    """Random Values plugin for Auto-GPT."""

    def __init__(self, plugin):
        self.plugin = plugin


    def random_number(self, min:int|str = 0, max:int|str = 65535, cnt:int|str = 1) -> str:
        """
        Return a random integer between min and max

        Args:
            min (int): The minimum value
            max (int): The maximum value
            cnt (int): The number of random numbers to return

        Returns:
            str: a json array with 1 to "count" random numbers in the format
            ["<random_number>"]
        """

        # Type-check the arguments
        try:
            min = int(min)
        except ValueError:
            raise ValueError("min must be an integer")
        try:
            max = int(max)
        except ValueError:
            raise ValueError("max must be an integer")
        try:
            cnt = int(cnt)
        except ValueError:
            raise ValueError("cnt must be an integer")

        # Ensure min is less than max
        if min > max:
            min, max = max, min
        
        # Test ranges
        if not (1 <= cnt <= 65535):
            raise ValueError("cnt must be between 1 and 65535")
        if not (0 <= min <= 65535):
            raise ValueError("min must be between 0 and 65535")
        if not (0 <= max <= 65535):
            raise ValueError("max must be between 0 and 65535")
        
        # Make random numbers
        random_numbers = []
        if isinstance(min, int) and isinstance(max, int):
            for _ in range(cnt):
                random_numbers.append(random.randint(min, max))
        else:
            for _ in range(cnt):
                random_numbers.append(random.uniform(min, max))

        return json.dumps(random_numbers)

    # End of random_number()


    def make_uuids(self, cnt:int|str = 1) -> str:
        """
        Return a UUID

        Args:
            cnt (int): The number of UUIDs to return

        Returns:
            str: a json array with 1 to "count" UUIDs
            ["<UUID>"]
        """

        # Type-check the arguments
        if not isinstance(cnt, int):
            try:
                cnt = int(cnt)
            except ValueError:
                raise ValueError("cnt must be an integer")

        # Make values sane
        if not (1 <= cnt <= 65535):
            raise ValueError("cnt must be between 1 and 65535")

        # Do the thing
        uuids = []
        for _ in range(cnt):
            uuids.append(str(uuid.uuid4()))

        return json.dumps(uuids)

    # End of make_uuids()


    def generate_string(self, len:int|str = 10, cnt:int|str = 1) -> str:
        """
        Return a random string

        Args:
            len (int): The length of the string
            cnt (int): The number of strings to return
            
        Returns:
            str: a json array with 1 to "count" strings of "length" length
            ["<string>"]
        """

        # Type-check the arguments
        if not isinstance(len, int):
            try:
                len = int(len)
            except ValueError:
                raise ValueError("len must be an integer")
        if not isinstance(cnt, int):
            try:
                cnt = int(cnt)
            except ValueError:
                raise ValueError("cnt must be an integer")

        # Range checks
        if not (1 <= cnt <= 65535):
            raise ValueError("cnt must be between 1 and 65535")
        if not (1 <= len <= 65535):
            raise ValueError("len must be between 1 and 65535")

        # Do the thing
        strings = []
        for _ in range(cnt):
            strings.append(
                "".join(random.choice(string.ascii_letters) for i in range(len))
            )

        return json.dumps(strings)


    def generate_password(self, len:int|str = 16, cnt:int|str = 1) -> str:
        """
        Return a random password of letters, numbers, and punctuation

        Args:
            len (int): The length of the password
            cnt (int): The number of passwords to return
                    
        Returns:
            str: a json array with 1 to "count" passwords of "length" length
            ["<password>"]
        """

        # Type-check the arguments
        if not isinstance(len, int):
            try:
                len = int(len)
            except ValueError:
                raise ValueError("len must be an integer")
        if not isinstance(cnt, int):
            try:
                cnt = int(cnt)
            except ValueError:
                raise ValueError("cnt must be an integer")

        # Make values sane
        if not (6 <= len <= 65535):
            raise ValueError("len must be between 6 and 65535")
        if not (1 <= cnt <= 65535):
            raise ValueError("cnt must be between 1 and 65535")

        # Do the thing
        passwords = []
        for _ in range(cnt):
            passwords.append(
                "".join(
                    random.choice(string.ascii_letters + string.digits + string.punctuation)
                    for i in range(len)
                )
            )

        return json.dumps(passwords)


    def generate_placeholder_text(self, cnt:int|str = 1) -> str:
        """
        Return a random sentence of lorem ipsum text

        Args:
            cnt (int): The number of sentences to return

        Returns:
            str: a json array with 1 to "sentences" strings of lorem ipsum
            ["<string>"]
        """

        # Type-check the arguments
        if not isinstance(cnt, int):
            try:
                cnt = int(cnt)
            except ValueError:
                raise ValueError("cnt must be an integer")

        # Make values sane
        if not (1 <= cnt <= 65535):
            raise ValueError("cnt must be between 1 and 65535")

        # Do the thing
        strings = []
        for _ in range(cnt):
            strings.append(lorem.get_sentence())

        return json.dumps(strings)
