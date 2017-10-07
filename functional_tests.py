from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):
    """
    Test expected outcomes for a new visitor.
    """

    def setUp(self):
        """
        Starts the web browser.
        """
        self.browser = webdriver.Firefox()

    def tearDown(self):
        """
        Quits the browser.
        """
        self.browser.quit()
    
    def test_start_and_retrieve_list(self):
        """
        Tests that user can both start and retrieve lists after logging in.
        """
        # Bob wants to check out our app. He goes to our homepage.
        self.browser.get("http://localhost:8000")

        # He notices the page title and header mention to-do lists.
        self.assertIn("To-Do", self.browser.title)
        self.fail("Finish the test!")

        # He is invited to enter a to-do list right away.

        # He types "Call Mom and Dad".

        # When he hits enter, the page updates and the to-do list now states:
        # "1. Call Mom and Dad" as an item in the to-do list

        # There is still a text box inviting him to enter another item. He enters "Call Brother".

        # The page updates again, and now shows both items

        # The site has generated a unique URL for Bob. There's some text mentioning that his list
        # will be saved.

        # Bob vists that URL. His list is still there.

        # Bob can now sleep peacefully, knowing he will remember to contact his family.

if __name__ == "__main__":
    unittest.main()
