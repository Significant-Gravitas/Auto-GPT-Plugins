"""Random Values classes for Autogpt."""

import json
import random
import uuid
import string
import lorem

"""Random Number function for Autogpt."""

class RandomValues:

    def __init__(
        self,
        plugin
    ) -> None:
        """Initialize the plugin"""

        self.plugin = plugin

    # End of __init__()


    def random_number(
        self,
        min = 0, 
        max = 65535, 
        count = 1
    ) -> str:
        """Return count random numbers between min and max
        Args:
            min (int|float): The lowest number in the range
            max (int|float): The highest number in the range
            count (int): The number of random numbers to return
        Returns:
            str: a json array with 1 to "count" random numbers in the format
            ["<random_number>"]
        """

        # Type-check the arguments
        if not isinstance(min, (int, float)):
            raise ValueError("min must be an integer or float")
        if not isinstance(max, (int, float)):
            raise ValueError("max must be an integer or float")
        if not isinstance(count, int):
            try:
                count = int(count)
            except ValueError:
                raise ValueError("count must be an integer")

        # Ensure min is less than max
        if min > max:
            min, max = max, min
        
        # Test ranges
        if not (1 <= count <= 65535):
            raise ValueError("count must be between 1 and 65535")
        if not (0 <= min <= 65535):
            raise ValueError("min must be between 0 and 65535")
        if not (0 <= max <= 65535):
            raise ValueError("max must be between 0 and 65535")
        
        # Make random numbers
        random_numbers = []
        if isinstance(min, int) and isinstance(max, int):
            for _ in range(count):
                random_numbers.append(random.randint(min, max))
        else:
            for _ in range(count):
                random_numbers.append(random.uniform(min, max))

        return json.dumps(random_numbers)
    
    # End of random_number()


    """Random UUID function for Autogpt."""

    def make_uuids(
        self,
        count = 1
    ) -> str:
        """Return a UUID
        Args:
            count (int): The number of UUIDs to return
        Returns:
            str: a json array with 1 to "count" UUIDs
            ["<UUID>"]
        """

        # Type-check the arguments
        if not isinstance(count, int):
            try:
                count = int(count)
            except ValueError:
                raise ValueError("count must be an integer")

        # Make values sane
        if not (1 <= count <= 65535):
            raise ValueError("count must be between 1 and 65535")

        # Do the thing
        uuids = []
        for _ in range(count):
            uuids.append(str(uuid.uuid4()))

        return json.dumps(uuids)
    
    # End of make_uuids()


    """Random String function for Autogpt."""

    def make_string(
        self,
        type: str,
        len = 10, 
        count = 1
    ) -> str:
        """Return a random string
        Args:
            length (int): The length of the string
            count (int): The number of strings to return
        Returns:
            str: a json array with 1 to "count" strings of "length" length
            ["<string>"]
        """

        # Type-check the arguments
        if not isinstance(type, str):
            raise ValueError("type must be one of txt, pwd, or lipsum")
        if not isinstance(len, int):
            try:
                len = int(len)
            except ValueError:
                raise ValueError("length must be an integer")
        if not isinstance(count, int):
            try:
                count = int(count)
            except ValueError:
                raise ValueError("count must be an integer")

        # Range checks
        if not (1 <= count <= 65535):
            raise ValueError("count must be between 1 and 65535")
        if not (1 <= len <= 65535):
            raise ValueError("length must be between 1 and 65535")

        # Do the thing
        strings = []
        if type == "txt":
            for _ in range(count):
                strings.append(''.join(random.choice(string.ascii_letters + string.digits) for i in range(len)))
        elif type == "pwd":
            for _ in range(count):
                strings.append(''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for i in range(len)))
        elif type == "sentence":
            for _ in range(count):
                strings.append(lorem.sentence())
        else:
            raise ValueError("type must be one of txt, pwd, or lipsum")

        return json.dumps(strings)
    
    # End of make_string()
