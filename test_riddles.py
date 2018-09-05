import unittest, run, json


class TestRiddles(unittest.TestCase):
    """
    Test suite for riddle game
    """
    
    def test_load_riddles_from_file(self):
        """
        Test to ensure the riddles are loaded
        """
        run.get_all_riddles("data/riddles.json")
        self.assertGreater(len("all_riddles"), 0)

    def test_get_next_riddle(self):
        """ 
        Test to ensure the current riddle is returned
        """
        riddle_count=2
        all_riddles = run.get_all_riddles("data/riddles.json")
        riddle = run.get_next_riddle(all_riddles, riddle_count)
        self.assertEqual(riddle["question"], "What has a head, a tail, is brown, and has no legs?")
        self.assertEqual(riddle["answer"], "penny")