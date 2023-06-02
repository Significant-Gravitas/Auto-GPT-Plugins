import json
import string
from unittest.mock import Mock
from unittest import TestCase
try:
    from .random_values import RandomValues
except ImportError:
    from random_values import RandomValues

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
        with self.assertRaises(ValueError) as e:
            self.random_values.random_number(min="foo", max="20", cnt="5")
        self.assertEqual(str(e.exception), "min must be an integer")

    def test_random_number_max_using_garbage(self):
        with self.assertRaises(ValueError) as e:
            self.random_values.random_number(min="10", max="bar", cnt="5")
        self.assertEqual(str(e.exception), "max must be an integer")

    def test_random_number_count_using_garbage(self):
        with self.assertRaises(ValueError) as e:
            self.random_values.random_number(min="10", max="20", cnt="baz")
        self.assertEqual(str(e.exception), "cnt must be an integer")

    def test_make_uuids(self):
        result = json.loads(self.random_values.make_uuids(cnt=5))
        self.assertEqual(len(result), 5)
        for uid in result:
            self.assertIsInstance(uid, str)
            self.assertEqual(len(uid), 36)  # UUIDs have 36 characters

    def test_make_uuids_using_strings(self):
        result = json.loads(self.random_values.make_uuids(cnt="5"))
        self.assertEqual(len(result), 5)
        for uid in result:
            self.assertIsInstance(uid, str)
            self.assertEqual(len(uid), 36)

    def test_make_uuids_using_missing_count(self):
        # If missing, count defaults to 1
        result = json.loads(self.random_values.make_uuids())
        self.assertEqual(len(result), 1)
        for uid in result:
            self.assertIsInstance(uid, str)
            self.assertEqual(len(uid), 36)

    def test_make_uuids_using_garbage(self):
        with self.assertRaises(ValueError) as e:
            self.random_values.make_uuids(cnt="foo")
        self.assertEqual(str(e.exception), "cnt must be an integer")

    # _generate_string Tests

    def test_generate_string(self):
        result = json.loads(self.random_values.generate_string(len=10, cnt=5))
        self.assertEqual(len(result), 5)
        for string in result:
            self.assertEqual(len(string), 10)
            # Strings should only contain letters and numbers
            self.assertTrue(string.isalnum())

    def test_generate_string_using_strings(self):
        result = json.loads(self.random_values.generate_string(len="10", cnt="5"))
        self.assertEqual(len(result), 5)
        for string in result:
            self.assertEqual(len(string), 10)
            # Strings should only contain letters and numbers
            self.assertTrue(string.isalnum())

    def test_generate_string_using_missing_length(self):
        # If missing, length defaults to 10
        result = json.loads(self.random_values.generate_string(cnt=5))
        self.assertEqual(len(result), 5)
        for string in result:
            self.assertEqual(len(string), 10)
            # Strings should only contain letters and numbers
            self.assertTrue(string.isalnum())

    def test_generate_string_using_missing_count(self):
        # If missing, count defaults to 1
        result = json.loads(self.random_values.generate_string(len=10))
        self.assertEqual(len(result), 1)
        for string in result:
            self.assertEqual(len(string), 10)
            # Strings should only contain letters and numbers
            self.assertTrue(string.isalnum())

    def test_generate_string_using_garbage(self):
        with self.assertRaises(ValueError) as e:
            self.random_values.generate_string(len="foo", cnt="bar")
        self.assertEqual(str(e.exception), "len must be an integer")

    # _generate_password Tests

    def test_generate_password(self):
        result = json.loads(self.random_values.generate_password(len=10, cnt=5))
        self.assertEqual(len(result), 5)
        for password in result:
            self.assertEqual(len(password), 10)
            # Passwords should contain letters, numbers, and symbols
            self.assertTrue(self.is_password(password))

    def test_generate_password_using_strings(self):
        result = json.loads(self.random_values.generate_password(len="10", cnt="5"))
        self.assertEqual(len(result), 5)
        for password in result:
            self.assertEqual(len(password), 10)
            # Passwords should contain letters, numbers, and symbols
            self.assertTrue(self.is_password(password))

    def test_generate_password_using_missing_length(self):
        # If missing, length defaults to 10
        result = json.loads(self.random_values.generate_password(cnt=5))
        self.assertEqual(len(result), 5)
        for password in result:
            self.assertEqual(len(password), 16)
            # Passwords should contain letters, numbers, and symbols
            self.assertTrue(self.is_password(password))

    def test_generate_password_using_missing_count(self):
        # If missing, count defaults to 1
        result = json.loads(self.random_values.generate_password(len=10))
        self.assertEqual(len(result), 1)
        for password in result:
            self.assertEqual(len(password), 10)
            # Passwords should contain letters, numbers, and symbols
            self.assertTrue(self.is_password(password))

    def test_generate_password_using_garbage(self):
        with self.assertRaises(ValueError) as e:
            self.random_values.generate_password(len="foo", cnt="bar")
        self.assertEqual(str(e.exception), "len must be an integer")

    # _generate_placeholder_text Tests

    def test_generate_placeholder_text(self):
        result = json.loads(self.random_values.generate_placeholder_text(cnt=5))
        self.assertEqual(len(result), 5)
        for text in result:
            self.assertGreater(len(text), 3)

    def test_generate_placeholder_text_using_strings(self):
        result = json.loads(self.random_values.generate_placeholder_text(cnt="5"))
        self.assertEqual(len(result), 5)
        for text in result:
            self.assertGreater(len(text), 3)

    def test_generate_placeholder_text_using_empty_string(self):
        with self.assertRaises(ValueError) as e:
            self.random_values.generate_placeholder_text(cnt="")
        self.assertEqual(str(e.exception), "cnt must be an integer")

    def test_generate_placeholder_text_using_garbage(self):
        with self.assertRaises(ValueError) as e:
            self.random_values.generate_placeholder_text(cnt="foo")
        self.assertEqual(str(e.exception), "cnt must be an integer")

    # checks that the given string only contains ascii letters, digits & punctuation
    def is_password(self, input_str):
        characters = string.ascii_letters + string.digits + string.punctuation
        for character in input_str:
            if character not in characters:
                return False
        return True
