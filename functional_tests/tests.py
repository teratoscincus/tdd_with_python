#!/usr/bin/env python3

import time

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


class NewVisitorTest(LiveServerTestCase):
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
        # User1 visits homepage.
        self.browser.get(self.live_server_url)

        # Check that "To-Do" is in the page title and header.
        self.assertIn("To-Do", self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, "h1").text
        self.assertIn("To-Do", header_text)

        # User1 is invited to make an entry.
        inputbox = self.browser.find_element(By.ID, "new_item")
        self.assertEqual(inputbox.get_attribute("placeholder"), "Enter a to-do item")

        # User1 enters "Buy tomatoes".
        inputbox.send_keys("Buy tomatoes")

        # On submission by pressing Enter, the page updates and lists:
        # "1: Buy tomatoes" as an item in a to-do list.
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)  # Await page update after submit

        # User1 get a unique URL for their list.
        user1_list_url = self.browser.current_url
        self.assertRegex(user1_list_url, "/lists/.+")

        self.assert_row_text_in_list_table("1: Buy tomatoes")

        # There is still a textbox inviting the user1 to make another entry.
        # User1 enters "Make tomato sauce"
        inputbox = self.browser.find_element(By.ID, "new_item")
        inputbox.send_keys("Make tomato sauce")
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # The page updates again, and now shows both items in the to-do list.
        self.assert_row_text_in_list_table("1: Buy tomatoes")
        self.assert_row_text_in_list_table("2: Make tomato sauce")

        # A new user checks out the site.
        ## Using a new browser session to ensure no info or cookies are shared.
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # User2 visits the site.
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertNotIn("Buy tomatoes", page_text)
        self.assertNotIn("Make tomato sauce", page_text)

        # User2 starts a new list by entering a new item.
        inputbox = self.browser.find_element(By.ID, "new_item")
        inputbox.send_keys("Write a test that fails")
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # User2 get their own unique URL.
        user2_list_url = self.browser.current_url
        self.assertRegex(user2_list_url, "/lists/.+")
        self.assertNotEqual(user1_list_url, user2_list_url)

        # User2 can only see their own list.
        page_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertNotIn("Buy tomatoes", page_text)
        self.assertIn("Write a test that fails", page_text)

        # Both users leave the web site.

    def test_layout_and_styling(self):
        # User1 goes to the index page.
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1644, 752)

        # Check centering of input box.
        inputbox = self.browser.find_element(By.ID, "new_item")
        self.assertAlmostEqual(
            inputbox.location["x"] + inputbox.size["width"] / 2, 822, delta=5
        )

        self.fail("Test not fully implemented - Finish writing the test!")
