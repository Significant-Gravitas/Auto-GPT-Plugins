"""Random Values classes for Autogpt."""

import json
import random
import uuid
import string
import lorem

"""Random Number function for Autogpt."""

def _random_number(min: int = 0, max: int = 65535, count: int  = 1) -> str:
    """Return a random integer between min and max
    Args:
        min (int): The lowest number in the range
        max (int): The highest number in the range
        count (int): The number of random numbers to return
    Returns:
        str: a json array with 1 to "count" random numbers in the format
        ["<random_number>"]
    """

    # Make values sane
    if not (0 <= min <= 65535):
        raise ValueError("min must be between 0 and 65535")
    if not (0 <= max <= 65535):
        raise ValueError("max must be between 0 and 65535")
    if not (1 <= count <= 65535):
        raise ValueError("count must be between 1 and 65535")

    # Do the thing
    random_numbers = []
    for _ in range(count):
        random_numbers.append(random.randint(min, max))

    return json.dumps(random_numbers)

"""Random UUID function for Autogpt."""

def _make_uuids(count: int = 1) -> str:
    """Return a UUID
    Args:
        count (int): The number of UUIDs to return
    Returns:
        str: a json array with 1 to "count" UUIDs
        ["<UUID>"]
    """

    # Make values sane
    if not (1 <= count <= 65535):
        raise ValueError("count must be between 1 and 65535")

    # Do the thing
    uuids = []
    for _ in range(count):
        uuids.append(str(uuid.uuid4()))

    return json.dumps(uuids)

"""Random String function for Autogpt."""

def _generate_string(length: int = 10, count: int = 1) -> str:
    """Return a random string
    Args:
        length (int): The length of the string
        count (int): The number of strings to return
    Returns:
        str: a json array with 1 to "count" strings of "length" length
        ["<string>"]
    """

    # Make values sane
    if not (2 <= length <= 65535):
        raise ValueError("length must be between 2 and 65535")
    if not (1 <= count <= 65535):
        raise ValueError("count must be between 1 and 65535")

    # Do the thing
    strings = []
    for _ in range(count):
        strings.append(''.join(random.choice(string.ascii_letters) for i in range(length)))

    return json.dumps(strings)

"""Random Password function for Autogpt."""

def _generate_password(length: int = 16, count: int = 1) -> str:
    """Return a random password of letters, numbers, and punctuation
    Args:
        length (int): The length of the password
        count (int): The number of passwords to return
    Returns:
        str: a json array with 1 to "count" passwords of "length" length
        ["<password>"]
    """
    
    # Make values sane
    if not (6 <= length <= 65535):
        raise ValueError("length must be between 6 and 65535")
    if not (1 <= count <= 65535):
        raise ValueError("count must be between 1 and 65535")

    # Do the thing
    passwords = []
    for _ in range(count):
        passwords.append(''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for i in range(length)))

    return json.dumps(passwords)

"""Random Lorem Ipsum function for Autogpt."""

def _generate_placeholder_text(count: int = 1) -> str:
    """Return a random sentence of lorem ipsum text
    Args:
        count (int): The number of strings to return
    Returns:
        str: a json array with 1 to "count" strings of lorem ipsum
        ["<string>"]
    """

    # Make values sane
    if not (1 <= count <= 65535):
        raise ValueError("count must be between 1 and 65535")

    # Do the thing
    strings = []
    for _ in range(count):
        strings.append(lorem.get_sentence())

    return json.dumps(strings)