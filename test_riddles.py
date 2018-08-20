import unittest, riddles_temp, json


class Testriddles(unittest.TestCase):
    """
    Test suite for riddle game
    """
    
    def test_load_riddles_from_file(self):
        """
        Test to ensure the riddles are loaded
        """
        riddles_temp.get_all_riddles("data/riddles.txt")
        self.assertGreater(len("riddles"), 0)
        
    def test_create_questions_from_file_lines(self):
        """
        Test to ensure the lines are split to create separate questions and answers
        """
        riddles_temp.get_all_riddles("data/riddles.txt")
        self.assertEqual(riddles[0], "The more you take, the more you leave behind. \nWhat am I? footsteps")
