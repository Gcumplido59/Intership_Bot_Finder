# In a new file like debug.py
from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.linkedin.com/jobs/search/?keywords=Software%20Intern&location=Mexico")

    print("Playwright Inspector is running. Find the selector for the 'X' button.")
    page.pause() # This opens the Inspector!

with sync_playwright() as playwright:
    run(playwright)