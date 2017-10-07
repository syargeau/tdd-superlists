import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


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
        header_text = self.browser.find_element_by_tag_name("h1").text
        self.assertIn("To-Do", header_text)

        # He is invited to enter a to-do list right away.
        inputbox = self.browser.find_element_by_id("id_new_item")
        self.assertEqual(
            inputbox.get_attribute("placeholder"),
            "Enter a to-do item"
        )

        # He types "Call Mom and Dad".
        inputbox.send_keys("Call Mom and Dad")

        # When he hits enter, the page updates and the to-do list now states:
        # "1. Call Mom and Dad" as an item in the to-do list
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        table = self.browser.find_element_by_id("id_list_table")
        rows = table.find_elements_by_tag_name("tr")
        self.assertTrue(
            any(row.text == "1. Call Mom and Dad" for row in rows)
        )

        # There is still a text box inviting him to enter another item. He enters "Call Brother".
        self.fail("Finish the test!")

        # The page updates again, and now shows both items

        # The site has generated a unique URL for Bob. There's some text mentioning that his list
        # will be saved.

        # Bob vists that URL. His list is still there.

        # Bob can now sleep peacefully, knowing he will remember to contact his family.

if __name__ == "__main__":
    unittest.main()
