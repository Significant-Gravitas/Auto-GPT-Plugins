from unittest.mock import Mock
import pytest
import json
from .random_values import _random_number
from .random_values import _make_uuids
from .random_values import _generate_string
from .random_values import _generate_password
from .random_values import _generate_placeholder_text

class TestRandomValueCommands():

   def test_random_number(self):
      result = json.loads(_random_number(min=10, max=20, count=5))
      assert len(result) == 5
      for num in result:
         assert 10 <= num <= 20

   def test_make_uuids(self):
      result = json.loads(_make_uuids(count=5))
      assert len(result) == 5
      for uid in result:
         assert isinstance(uid, str)
         assert len(uid) == 36  # UUIDs have 36 characters

   def test_generate_string(self):
      result = json.loads(_generate_string(length=10, count=5))
      assert len(result) == 5
      for string in result:
         assert len(string) == 10

   def test_generate_password(self):
      result = json.loads(_generate_password(length=10, count=5))
      assert len(result) == 5
      for password in result:
         assert len(password) == 10

   def test_generate_placeholder_text(self):
      result = json.loads(_generate_placeholder_text(count=5))
      assert len(result) == 5
      for text in result:
         assert len(text.split()) >= 4

   def test_random_number_invalid(self):
    with pytest.raises(ValueError):
        _random_number(min=20, max=10)

   def test_make_uuids_invalid(self):
    with pytest.raises(ValueError):
        _make_uuids(count=0)

   def test_generate_string_invalid(self):
    with pytest.raises(ValueError):
        _generate_string(length=0)

   def test_generate_password_invalid(self):
    with pytest.raises(ValueError):
        _generate_password(length=0)

   def test_generate_placeholder_text_invalid(self):
    with pytest.raises(ValueError):
        _generate_placeholder_text(count=0)
