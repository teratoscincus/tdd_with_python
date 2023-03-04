from selenium import webdriver

browser = webdriver.Firefox()
browser.get("http://localhost:8000")

installation_success = "The install worked successfully! Congratulations!"
assert installation_success in browser.title
print("TEST: OK")
