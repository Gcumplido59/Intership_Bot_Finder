# In bot.py
import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from Bot.scraper import scrape_linkedin_jobs # Import our scraper function

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# This function runs when the user sends /findinternships <query>
async def find_internships(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Get the search query from the user's message
    if not context.args:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Please provide a search query. Example: `/findinternships Software Intern Zapopan`"
        )
        return
    
    query = ' '.join(context.args)
    
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"On it! Searching for '{query}' jobs... This might take a moment. ⏳"
    )

    try:
        # Run the synchronous scraper function in a separate thread
        # This prevents the bot from freezing while it's scraping.
        summaries = await asyncio.to_thread(scrape_linkedin_jobs, query)

        if not summaries:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Sorry, I couldn't find any job listings for that query."
            )
            return

        # Send the results back to the user
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Found {len(summaries)} results! Here they are:"
        )
        for summary in summaries:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=summary,
                parse_mode='Markdown' # Allows for bold text
            )
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Sorry, something went wrong while scraping. Please try again later."
        )

def main():
    TOKEN = "8365574938:AAEbhWF5iObXnBMpx_b51nu0vcoNvHKNyJM"
    application = Application.builder().token(TOKEN).build()

    # Register the /findinternships command handler
    find_handler = CommandHandler('findinternships', find_internships)
    application.add_handler(find_handler)
    
    print("Bot is running... Press Ctrl+C to stop.")
    application.run_polling()

if __name__ == '__main__':
    main()