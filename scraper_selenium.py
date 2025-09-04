# In scraper.py
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

# LinkedIn URL for "Software Intern" jobs in Mexico
URL = "https://www.linkedin.com/jobs/search/?keywords=Software%20Intern&location=Mexico"

# 1. Set up the WebDriver
print("Setting up the browser...")
driver = webdriver.Chrome()

# 2. Go to the URL
print(f"Opening LinkedIn Jobs: {URL}")
driver.get(URL)

# 3. Wait for the page to load its content
# LinkedIn loads jobs with JavaScript, so we need to give it a moment.
print("Waiting for jobs to load...")
time.sleep(5) # Wait for 5 seconds

# 4. Find all job title elements
# After inspecting the site, job titles are in <h3> tags inside a specific div.
print("Finding job titles...")
job_elements = driver.find_elements(By.CSS_SELECTOR, "div.base-search-card__info h3")

print("\n--- Found Job Titles ---")
for element in job_elements:
    print(element.text.strip())

# 5. Close the browser
driver.quit()