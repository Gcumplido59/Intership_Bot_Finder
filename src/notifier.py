"""Handles the notification of job listings to a Telegram channel."""

import asyncio
import telegram
from .scraper import scrape_linkedin_jobs

#CONFIGURATION
TELEGRAM_TOKEN = ""
CHAT_ID = ""

JOB_QUERY = "Software engineer internship"

async def main():
    """Runs the job scraper and sends notifications to Telegram.

    This is the main function of the application. It scrapes for jobs,
    and if any are found, sends them to the specified Telegram channel.
    """
    print(f"Starting scraper for query: '{JOB_QUERY}'...")
    
    summaries = await scrape_linkedin_jobs(JOB_QUERY)
    
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    
    if not summaries:
        print("Scraper finished but found no results.")
        await bot.send_message(chat_id=CHAT_ID, text=f"No new internships found for '{JOB_QUERY}' in the last 48 hours.")
        return

    print(f"Found {len(summaries)} results. Sending to Telegram...")
    
    await bot.send_message(
        chat_id=CHAT_ID,
        text=f"🚀 Found {len(summaries)} new internships for '{JOB_QUERY}' in the last 48 hours:"
    )
    
    for summary in summaries:
        try:
            await bot.send_message(
                chat_id=CHAT_ID,
                text=summary,
                parse_mode='Markdown',
                disable_web_page_preview=True
            )
            await asyncio.sleep(1)
        except Exception as e:
            print(f"Could not send message: {e}")

    print("All messages sent successfully!")
