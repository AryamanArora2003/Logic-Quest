import unittest
import landingPage

class TestLandingPage(unittest.TestCase):

    # Test if the button is clicked
    def test_leaderboard_button(self):
        # Create a LandingPage object
        page = landingPage.LandingPage()

        # Simulate a button click
        page.leaderboard()

        # Check the state of the page after the button click
        self.assertEqual(page.state, 'leaderboard')

    def test_start_button(self):
        button = landingPage.Button("Start Game", '#89CFF0', 320, 80, (0, 0), 6, landingPage.play_game)
        button.pressed = True  # Simulate a click
        button.checkClick()  # Trigger the click check
        self.assertEqual(button.get_state(), "play_game")
        


if __name__ == '__main__':
    unittest.main()