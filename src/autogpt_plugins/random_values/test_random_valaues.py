import json
from unittest.mock import Mock
import string

import pytest

from .random_values import (
    _generate_password,
    _generate_placeholder_text,
    _generate_string,
    _make_uuids,
    _random_number,
)


class TestRandomValueCommands:
    # _random_number Tests

    def test_random_number(self):
        result = json.loads(_random_number(min=10, max=20, count=5))
        assert len(result) == 5
        for num in result:
            assert 10 <= num <= 20

    def test_random_number_using_strings(self):
        result = json.loads(_random_number(min="10", max="20", count="5"))
        assert len(result) == 5
        for num in result:
            assert 10 <= num <= 20

    def test_random_number_using_missing_min(self):
        # If missing, min defaults to zero
        result = json.loads(_random_number(max=20, count=5))
        assert len(result) == 5
        for num in result:
            assert 0 <= num <= 20

    def test_random_number_using_missing_max(self):
        # If missing, max defaults to 65535
        result = json.loads(_random_number(min=10, count=5))
        assert len(result) == 5
        for num in result:
            assert 10 <= num <= 65535

    def test_random_number_using_missing_count(self):
        # If missing, count defaults to 1
        result = json.loads(_random_number(min=10, max=20))
        assert len(result) == 1
        for num in result:
            assert 10 <= num <= 20

    def test_random_number_min_using_garbage(self):
        with pytest.raises(ValueError) as e:
            _random_number(min="foo", max="20", count="5")
        assert str(e.value) == "min must be an integer"

    def test_random_number_max_using_garbage(self):
        with pytest.raises(ValueError) as e:
            _random_number(min="10", max="bar", count="5")
        assert str(e.value) == "max must be an integer"

    def test_random_number_count_using_garbage(self):
        with pytest.raises(ValueError) as e:
            _random_number(min="10", max="20", count="baz")
        assert str(e.value) == "count must be an integer"

    # _make_uuids Tests

    def test_make_uuids(self):
        result = json.loads(_make_uuids(count=5))
        assert len(result) == 5
        for uid in result:
            assert isinstance(uid, str)
            assert len(uid) == 36  # UUIDs have 36 characters

    def test_make_uuids_using_strings(self):
        result = json.loads(_make_uuids(count="5"))
        assert len(result) == 5
        for uid in result:
            assert isinstance(uid, str)
            assert len(uid) == 36

    def test_make_uuids_using_missing_count(self):
        # If missing, count defaults to 1
        result = json.loads(_make_uuids())
        assert len(result) == 1
        for uid in result:
            assert isinstance(uid, str)
            assert len(uid) == 36

    def test_make_uuids_using_garbage(self):
        with pytest.raises(ValueError) as e:
            _make_uuids(count="foo")
        assert str(e.value) == "count must be an integer"

    # _generate_string Tests

    def test_generate_string(self):
        result = json.loads(_generate_string(length=10, count=5))
        assert len(result) == 5
        for string in result:
            assert len(string) == 10
            # Strings should only contain letters and numbers
            assert string.isalnum()

    def test_generate_string_using_strings(self):
        result = json.loads(_generate_string(length="10", count="5"))
        assert len(result) == 5
        for string in result:
            assert len(string) == 10
            # Strings should only contain letters and numbers
            assert string.isalnum()

    def test_generate_string_using_missing_length(self):
        # If missing, length defaults to 10
        result = json.loads(_generate_string(count=5))
        assert len(result) == 5
        for string in result:
            assert len(string) == 10
            # Strings should only contain letters and numbers
            assert string.isalnum()

    def test_generate_string_using_missing_count(self):
        # If missing, count defaults to 1
        result = json.loads(_generate_string(length=10))
        assert len(result) == 1
        for string in result:
            assert len(string) == 10
            # Strings should only contain letters and numbers
            assert string.isalnum()

    def test_generate_string_using_garbage(self):
        with pytest.raises(ValueError) as e:
            _generate_string(length="foo", count="bar")
        assert str(e.value) == "length must be an integer"

    # _generate_password Tests

    def test_generate_password(self):
        result = json.loads(_generate_password(length=10, count=5))
        assert len(result) == 5
        for password in result:
            assert len(password) == 10
            # Passwords should contain letters, numbers, and symbols
            assert is_password(password)

    def test_generate_password_using_strings(self):
        result = json.loads(_generate_password(length="10", count="5"))
        assert len(result) == 5
        for password in result:
            assert len(password) == 10
            # Passwords should contain letters, numbers, and symbols
            assert is_password(password)

    def test_generate_password_using_missing_length(self):
        # If missing, length defaults to 10
        result = json.loads(_generate_password(count=5))
        assert len(result) == 5
        for password in result:
            assert len(password) == 16
            # Passwords should contain letters, numbers, and symbols
            assert is_password(password)

    def test_generate_password_using_missing_count(self):
        # If missing, count defaults to 1
        result = json.loads(_generate_password(length=10))
        assert len(result) == 1
        for password in result:
            assert len(password) == 10
            # Passwords should contain letters, numbers, and symbols
            assert is_password(password)

    def test_generate_password_using_garbage(self):
        with pytest.raises(ValueError) as e:
            _generate_password(length="foo", count="bar")
        assert str(e.value) == "length must be an integer"

    # _generate_placeholder_text Tests

    def test_generate_placeholder_text(self):
        result = json.loads(_generate_placeholder_text(sentences=5))
        assert len(result) == 5
        for text in result:
            assert len(text) > 3

    def test_generate_placeholder_text_using_strings(self):
        result = json.loads(_generate_placeholder_text(sentences="5"))
        assert len(result) == 5
        for text in result:
            assert len(text) > 3

    def test_generate_placeholder_text_using_empty_string(self):
        with pytest.raises(ValueError) as e:
            _generate_placeholder_text(sentences="")
        assert str(e.value) == "sentences must be an integer"

    def test_generate_placeholder_text_using_garbage(self):
        with pytest.raises(ValueError) as e:
            _generate_placeholder_text(sentences="foo")
        assert str(e.value) == "sentences must be an integer"

# checks that the given string only contains ascii letters, digits & punctuation
def is_password(input_str):
    characters = string.ascii_letters + string.digits + string.punctuation
    for character in input_str:
        if character not in characters:
            return False
    return True
