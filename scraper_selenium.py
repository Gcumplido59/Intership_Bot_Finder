# In scraper.py
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# LinkedIn URL for "Software Intern" jobs in Mexico
URL = "https://www.linkedin.com/jobs/search/?keywords=Software%20Intern&location=Mexico"

def dismiss_login_popup(driver, wait_time=5):
    """
    Attempt to dismiss LinkedIn's login popup if it appears.
    
    Args:
        driver: Selenium WebDriver instance
        wait_time: Maximum time to wait for popup (seconds)
    
    Returns:
        bool: True if popup was found and dismissed, False otherwise
    """
    try:
        print("Looking for login popup to dismiss...")
        wait = WebDriverWait(driver, wait_time)
        
        # List of possible selectors for the dismiss/close button
        # Based on Playwright script that uses "Descartar" (Spanish for "Dismiss")
        dismiss_selectors = [
            # Text-based selectors (most reliable)
            "//button[contains(text(), 'Descartar')]",  # Spanish
            "//button[contains(text(), 'Dismiss')]",    # English
            "//button[contains(text(), 'Close')]",      # English alternative
            "//button[contains(text(), '×')]",          # Close symbol
            
            # Aria-label based selectors
            "//button[@aria-label='Dismiss']",
            "//button[@aria-label='Close']",
            
            # Class-based selectors for LinkedIn modals
            ".artdeco-modal__dismiss",
            ".modal__dismiss",
            "[data-test-modal-close-btn]",
            
            # Generic modal close buttons
            ".artdeco-modal .artdeco-button--secondary"
        ]
        
        popup_dismissed = False
        for selector in dismiss_selectors:
            try:
                if selector.startswith("//"):
                    # XPath selector
                    element = wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                else:
                    # CSS selector
                    element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                
                element.click()
                print(f"Successfully dismissed popup using selector: {selector}")
                popup_dismissed = True
                break
                
            except TimeoutException:
                # This selector didn't find anything, try the next one
                continue
            except Exception as e:
                print(f"Error with selector {selector}: {e}")
                continue
        
        if popup_dismissed:
            # Give a moment for the popup to disappear
            time.sleep(1)
            return True
        else:
            print("No login popup found or could not dismiss it.")
            return False
            
    except Exception as e:
        print(f"Error while trying to dismiss popup: {e}")
        return False

# 1. Set up the WebDriver
print("Setting up the browser...")
driver = webdriver.Chrome()

try:
    # 2. Go to the URL
    print(f"Opening LinkedIn Jobs: {URL}")
    driver.get(URL)

    # 3. Handle login popup if it appears
    dismiss_login_popup(driver)

    # 4. Wait for the page to load its content
    # LinkedIn loads jobs with JavaScript, so we need to give it a moment.
    print("Waiting for jobs to load...")
    time.sleep(5) # Wait for 5 seconds

    # 5. Find all job title elements
    # After inspecting the site, job titles are in <h3> tags inside a specific div.
    print("Finding job titles...")
    job_elements = driver.find_elements(By.CSS_SELECTOR, "div.base-search-card__info h3")

    print(f"\n--- Found {len(job_elements)} Job Titles ---")
    for element in job_elements:
        title = element.text.strip()
        if title:  # Only print non-empty titles
            print(title)
            
    if len(job_elements) == 0:
        print("No job listings found. This might indicate that the login popup is still blocking access.")

finally:
    # 6. Close the browser
    driver.quit()