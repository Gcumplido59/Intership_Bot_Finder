"""Scrapes job listings from LinkedIn."""

from playwright.async_api import async_playwright
import asyncio
from ai_processor import format_job_listing
from urllib.parse import quote

async def scrape_linkedin_jobs(query: str) -> list:
    """Scrapes LinkedIn for job listings based on a search query.

    This function uses Playwright to launch a headless browser, navigate to
    LinkedIn, and scrape job listings. It then formats the results using
    the AI processor.

    Args:
        query: The job search query.

    Returns:
        A list of formatted job listing strings.
    """
    formatted_query = quote(query)
    URL = f"https://www.linkedin.com/jobs/search/?keywords={formatted_query}&location=Mexico&f_TPR=r172800"
    
    formatted_results = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        page = await context.new_page()

        try:
            await page.goto(URL, timeout=60000)

            job_card_selector = "div.job-search-card"
            await page.wait_for_selector(job_card_selector, timeout=20000)
            job_cards = await page.locator(job_card_selector).all()
            print(f"Found {len(job_cards)} job cards.")

            for card in job_cards[:7]:
                job_page = None
                try:
                    title = await card.locator("h3.base-search-card__title").text_content()
                    company = await card.locator("h4.base-search-card__subtitle").text_content()
                    location = await card.locator("span.job-search-card__location").text_content()
                    link = await card.locator("a.base-card__full-link").get_attribute("href")

                    job_page = await context.new_page()
                    await job_page.goto(link, timeout=60000)
                    description_text = await job_page.locator("div.show-more-less-html__markup").text_content(timeout=5000)
                    await job_page.close()
                    
                    summary = format_job_listing(title.strip(), company.strip(), location.strip(), link, description_text.strip())
                    formatted_results.append(summary)
                    
                except Exception as e:
                    print(f"Could not process a card: {e}")
                    if job_page and not job_page.is_closed():
                        await job_page.close() # Ensure the new tab is closed on error
                    continue
        except Exception as e:
            print(f"An error occurred during scraping: {e}")
        finally:
            await browser.close()

    return formatted_results