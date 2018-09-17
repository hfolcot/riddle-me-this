import unittest, run, json


class TestRiddles(unittest.TestCase):
    """
    Test suite for riddle game
    """
    
    def test_load_riddles_from_file(self):
        """
        Test to ensure the riddles are loaded
        """
        all_riddles = run.get_data("data/riddles.json")
        self.assertGreater(len(all_riddles), 0)
    
    def test_create_new_user(self):
        """
        Ensure that a new user is created when a user name is input
        """
        players = run.create_new_user("TestPlayer43")
        self.assertEqual(players["TestPlayer43"]["name"], "TestPlayer43")

    def test_get_next_riddle(self):
        """ 
        Test to ensure the current riddle is returned
        """
        riddle_count=2
        all_riddles = run.get_data("data/riddles.json")
        riddle = run.get_next_riddle(all_riddles, riddle_count)
        self.assertEqual(riddle["question"], "What has a head, a tail, is brown, and has no legs?")
        self.assertEqual(riddle["answer"], "penny")
    
       
    def test_reset_game(self):
        """
        Ensure all game variables have been reset
        """
        run.create_new_user("TestingPlayer42")
        run.all_users["TestingPlayer42"]["current_riddle"] +=3
        run.all_users["TestingPlayer42"]["score"] +=3
        run.reset_game("TestingPlayer42")
        self.assertEqual(run.all_users["TestingPlayer42"]["current_riddle"], 1)
        self.assertEqual(run.all_users["TestingPlayer42"]["score"], 0)
         
    
    def test_high_score_created(self):
        """
        Ensure that sample data is added to the json file.
        add_to_scores must include the line 
        `return entry`
        for this test to pass, due to the need to create a unique key at each run
        """
        username = run.add_to_scores("data/scores.json", "TestingPlayer47", "12")
        all_scores = run.get_data("data/scores.json")
        self.assertEqual(all_scores[username]["score"], "12")

    
    def test_scores_loaded_from_file(self):
        """
        Test to ensure the high scores are loaded
        """
        all_scores = run.get_data("data/scores.json")
        self.assertGreater(len(all_scores), 0)