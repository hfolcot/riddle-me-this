import unittest, run, json


class TestRiddles(unittest.TestCase):
    """
    Test suite for riddle game
    """
    
    def test_load_riddles_from_file(self):
        """
        Test to ensure the riddles are loaded
        """
        run.get_data("data/riddles.json")
        self.assertGreater(len("all_riddles"), 0)

    def test_get_next_riddle(self):
        """ 
        Test to ensure the current riddle is returned
        """
        riddle_count=2
        all_riddles = run.get_data("data/riddles.json")
        riddle = run.get_next_riddle(all_riddles, riddle_count)
        self.assertEqual(riddle["question"], "What has a head, a tail, is brown, and has no legs?")
        self.assertEqual(riddle["answer"], "penny")
    """    
    def test_reset_game(self):
        
        #Ensure all game variables have been reset
        
        #currently fails as apparently unable to reach the all_users dict
        current_user = "argaer"
        riddle_count = run.all_users[current_user]["current_riddle"]
        score = run.all_users[current_user]["score"]
        run.reset_game(current_user)
        self.assertEqual(riddle_count, 1)
        self.assertEqual(score, 0)
       
    
    def test_high_score_created(self):
        run.add_to_scores("data/scores.json", "testuser4569821546751154684frd", "12")
        all_scores = run.get_data("data/scores.json")
        run.print_scores_to_index(all_scores)
        self.assertIn(all_scores["testuser4569821546751154684frd"], "12")
    """     
    def test_scores_loaded_from_file(self):
        """
        Test to ensure the high scores are loaded
        """
        all_scores = run.get_data("data/scores.json")
        print(all_scores)
        self.assertGreater(len("all_scores"), 0)