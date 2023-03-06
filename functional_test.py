#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import unittest
import time


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def assert_row_text_in_list_table(self, row_text):
        table = self.browser.find_element(By.ID, "list_table")
        rows = table.find_elements(By.TAG_NAME, "tr")
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # User visits homepage.
        self.browser.get("http://localhost:8000")

        # Check that "To-Do" is in the page title and header.
        self.assertIn("To-Do", self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, "h1").text
        self.assertIn("To-Do", header_text)

        # User is invited to make an entry.
        inputbox = self.browser.find_element(By.ID, "new_item")
        self.assertEqual(inputbox.get_attribute("placeholder"), "Enter a to-do item")

        # User enters "Buy tomatoes".
        inputbox.send_keys("Buy tomatoes")

        # On submission by pressing Enter, the page updates and lists:
        # "1: Buy tomatoes" as an item in a to-do list.
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)  # Await page update after submit

        self.assert_row_text_in_list_table("1: Buy tomatoes")

        # There is still a textbox inviting the user to make another entry.
        # User enters "Make tomato sauce"
        inputbox = self.browser.find_element(By.ID, "new_item")
        inputbox.send_keys("Make tomato sauce")
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # The page updates again, and now shows both items in the to-do list.
        self.assert_row_text_in_list_table("1: Buy tomatoes")
        self.assert_row_text_in_list_table("2: Make tomato sauce")

        # Check that a unique URL for the users list has been generated.

        self.fail("Test not fully implemented - Finish writing the test!")

        # Visit URL and ensure the users to-do list is still there.


if __name__ == "__main__":
    unittest.main(warnings="ignore")
