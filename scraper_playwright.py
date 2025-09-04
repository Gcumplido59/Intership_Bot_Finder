# In scraper.py
from playwright.sync_api import sync_playwright
import time
from ai_processor import summarize_job_description

URL = "https://www.linkedin.com/jobs/search/?keywords=Software%20Intern&location=Mexico"

def run(playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    print(f"Navigating to LinkedIn Jobs: {URL}")
    page.goto(URL)

    # --- NEW: CLOSE THE LOGIN POP-UP ---
    try:
        print("Looking for the login pop-up to close it...")
        
        # Using the exact locator you found with the Playwright Inspector!
        page.get_by_role("button", name="Descartar").click(timeout=5000)
        
        print("Login pop-up closed successfully.")
        
    except Exception as e:
        # If the pop-up doesn't appear or the click fails, just print a message and continue.
        print(f"Login pop-up did not appear or could not be closed. Continuing anyway. Error: {e}")

    # Proceed with scraping as before
    print("Waiting for job cards to load...")
    page.wait_for_selector("div.base-search-card")
    
    job_cards = page.locator("div.base-search-card").all()
    print(f"\n--- Found {len(job_cards)} Job Listings ---")

    for card in job_cards:
        try:
            card.click()
            page.wait_for_selector("div.show-more-less-html__markup", timeout=5000)

            title = card.locator("h3.base-search-card__title").text_content().strip()
            description_panel = page.locator("div.show-more-less-html__markup")
            raw_description_text = description_panel.text_content().strip()
            
            # --- NEW: PROCESS THE TEXT WITH AI ---
            print(f"\n## {title} ##")
            print("Processing with AI...")
            summary = summarize_job_description(raw_description_text)
            print(summary) # Print the clean summary from the AI
            print("-" * 20)
            time.sleep(1)

        except Exception as e:
            print(f"Could not process a card: {e}")
            continue

    context.close()
    browser.close()
    print("\nScraping complete.")

with sync_playwright() as playwright:
    run(playwright)