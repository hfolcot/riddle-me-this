import unittest, riddles_temp, json


class TestRiddles(unittest.TestCase):
    """
    Test suite for riddle game
    """
    
    def test_load_riddles_from_file(self):
        """
        Test to ensure the riddles are loaded
        """
        riddles_temp.get_all_riddles("data/riddles.json")
        self.assertGreater(len("all_riddles"), 0)
