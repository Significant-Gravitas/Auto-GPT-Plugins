import json
import pytest
import string
from unittest.mock import Mock
from unittest import TestCase
from .random_values import RandomValues

class TestRandomValueCommands(TestCase):
    # _random_number Tests

    def setUp(self):
        self.random_values = RandomValues(Mock())


    def test_random_number(self):
        result = json.loads(self.random_values.random_number(min=10, max=20, cnt=5))
        self.assertEqual(len(result), 5)
        for num in result:
            self.assertTrue(10 <= num <= 20)

    def test_random_number_using_strings(self):
        result = json.loads(self.random_values.random_number(min="10", max="20", cnt="5"))
        self.assertEqual(len(result), 5)
        for num in result:
            self.assertTrue(10 <= num <= 20)

    def test_random_number_using_missing_min(self):
        result = json.loads(self.random_values.random_number(max=20, cnt=5))
        self.assertEqual(len(result), 5)
        for num in result:
            self.assertTrue(0 <= num <= 20)

    def test_random_number_using_missing_max(self):
        result = json.loads(self.random_values.random_number(min=10, cnt=5))
        self.assertEqual(len(result), 5)
        for num in result:
            self.assertTrue(10 <= num <= 65535)

    def test_random_number_using_missing_count(self):
        result = json.loads(self.random_values.random_number(min=10, max=20))
        self.assertEqual(len(result), 1)
        for num in result:
            self.assertTrue(10 <= num <= 20)

    def test_random_number_min_using_garbage(self):
        with pytest.raises(ValueError) as e:
            self.random_values.random_number(min="foo", max="20", cnt="5")
        assert str(e.value) == "min must be an integer"

    def test_random_number_max_using_garbage(self):
        with pytest.raises(ValueError) as e:
            self.random_values.random_number(min="10", max="bar", cnt="5")
        assert str(e.value) == "max must be an integer"

    def test_random_number_count_using_garbage(self):
        with pytest.raises(ValueError) as e:
            self.random_values.random_number(min="10", max="20", cnt="baz")
        assert str(e.value) == "cnt must be an integer"

    # _make_uuids Tests

    def test_make_uuids(self):
        result = json.loads(self.random_values.make_uuids(cnt=5))
        assert len(result) == 5
        for uid in result:
            assert isinstance(uid, str)
            assert len(uid) == 36  # UUIDs have 36 characters

    def test_make_uuids_using_strings(self):
        result = json.loads(self.random_values.make_uuids(cnt="5"))
        assert len(result) == 5
        for uid in result:
            assert isinstance(uid, str)
            assert len(uid) == 36

    def test_make_uuids_using_missing_count(self):
        # If missing, count defaults to 1
        result = json.loads(self.random_values.make_uuids())
        assert len(result) == 1
        for uid in result:
            assert isinstance(uid, str)
            assert len(uid) == 36

    def test_make_uuids_using_garbage(self):
        with pytest.raises(ValueError) as e:
            self.random_values.make_uuids(cnt="foo")
        assert str(e.value) == "cnt must be an integer"

    # _generate_string Tests

    def test_generate_string(self):
        result = json.loads(self.random_values.generate_string(len=10, cnt=5))
        assert len(result) == 5
        for string in result:
            assert len(string) == 10
            # Strings should only contain letters and numbers
            assert string.isalnum()

    def test_generate_string_using_strings(self):
        result = json.loads(self.random_values.generate_string(len="10", cnt="5"))
        assert len(result) == 5
        for string in result:
            assert len(string) == 10
            # Strings should only contain letters and numbers
            assert string.isalnum()

    def test_generate_string_using_missing_length(self):
        # If missing, length defaults to 10
        result = json.loads(self.random_values.generate_string(cnt=5))
        assert len(result) == 5
        for string in result:
            assert len(string) == 10
            # Strings should only contain letters and numbers
            assert string.isalnum()

    def test_generate_string_using_missing_count(self):
        # If missing, count defaults to 1
        result = json.loads(self.random_values.generate_string(len=10))
        assert len(result) == 1
        for string in result:
            assert len(string) == 10
            # Strings should only contain letters and numbers
            assert string.isalnum()

    def test_generate_string_using_garbage(self):
        with pytest.raises(ValueError) as e:
            self.random_values.generate_string(len="foo", cnt="bar")
        assert str(e.value) == "len must be an integer"

    # _generate_password Tests

    def test_generate_password(self):
        result = json.loads(self.random_values.generate_password(len=10, cnt=5))
        assert len(result) == 5
        for password in result:
            assert len(password) == 10
            # Passwords should contain letters, numbers, and symbols
            assert self.is_password(password)

    def test_generate_password_using_strings(self):
        result = json.loads(self.random_values.generate_password(len="10", cnt="5"))
        assert len(result) == 5
        for password in result:
            assert len(password) == 10
            # Passwords should contain letters, numbers, and symbols
            assert self.is_password(password)

    def test_generate_password_using_missing_length(self):
        # If missing, length defaults to 10
        result = json.loads(self.random_values.generate_password(cnt=5))
        assert len(result) == 5
        for password in result:
            assert len(password) == 16
            # Passwords should contain letters, numbers, and symbols
            assert self.is_password(password)

    def test_generate_password_using_missing_count(self):
        # If missing, count defaults to 1
        result = json.loads(self.random_values.generate_password(len=10))
        assert len(result) == 1
        for password in result:
            assert len(password) == 10
            # Passwords should contain letters, numbers, and symbols
            assert self.is_password(password)

    def test_generate_password_using_garbage(self):
        with pytest.raises(ValueError) as e:
            self.random_values.generate_password(len="foo", cnt="bar")
        assert str(e.value) == "len must be an integer"

    # _generate_placeholder_text Tests

    def test_generate_placeholder_text(self):
        result = json.loads(self.random_values.generate_placeholder_text(cnt=5))
        assert len(result) == 5
        for text in result:
            assert len(text) > 3

    def test_generate_placeholder_text_using_strings(self):
        result = json.loads(self.random_values.generate_placeholder_text(cnt="5"))
        assert len(result) == 5
        for text in result:
            assert len(text) > 3

    def test_generate_placeholder_text_using_empty_string(self):
        with pytest.raises(ValueError) as e:
            self.random_values.generate_placeholder_text(cnt="")
        assert str(e.value) == "cnt must be an integer"

    def test_generate_placeholder_text_using_garbage(self):
        with pytest.raises(ValueError) as e:
            self.random_values.generate_placeholder_text(cnt="foo")
        assert str(e.value) == "cnt must be an integer"

    # checks that the given string only contains ascii letters, digits & punctuation
    def is_password(self, input_str):
        characters = string.ascii_letters + string.digits + string.punctuation
        for character in input_str:
            if character not in characters:
                return False
        return True
