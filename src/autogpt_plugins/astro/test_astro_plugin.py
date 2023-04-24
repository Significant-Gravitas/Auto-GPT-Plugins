from email_plugin import (
    get_num_astronauts
)
import unittest

class TestAstroPlugin(unittest.TestCase):
    def test_astro(self):
        self.assertTrue(type(get_num_astronauts())===int)

if __name__ == "__main__":
    unittest.main()
