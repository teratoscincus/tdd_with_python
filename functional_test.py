from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # User visits homepage.
        self.browser.get("http://localhost:8000")

        # Check that "To-Do" is in the page title.
        self.assertIn("To-Do", self.browser.title)
        self.fail("Finish the test!")

        # User is invited to make an entry.

        # User enters "Buy tomatoes".

        # On submission, the page updates and lists:
        # "1: Buy tomatoes" as an item in a to-do list.

        # There is still a textbox inviting the user to make another entry.

        # User enters "Make tomato sauce"

        # The page updates again, and now shows both items in the to-do list.

        # Check that a unique URL for the user has been generated.

        # Visit URL and ensure the users to-do list is still there.


if __name__ == "__main__":
    unittest.main(warnings="ignore")
