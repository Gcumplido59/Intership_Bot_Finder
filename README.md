# Internship Bot Finder

This project is a Python-based bot that automatically scrapes LinkedIn for internship opportunities, uses a generative AI to format the listings, and sends them to a Telegram channel.

## Purpose

The main goal of this project is to automate the process of finding and filtering internship opportunities. By using a bot, you can receive timely notifications about new internships that match your criteria, directly in your Telegram.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/dani-fpad/Intership_Bot_Finder
    cd Intership_Bot_Finder
    ```

2.  **Install dependencies:**
    This project uses `playwright` for web scraping and `python-telegram-bot` for sending notifications. It is recommended to use a virtual environment.
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install playwright python-telegram-bot google-generativeai
    playwright install
    ```

3.  **Configure the bot:**
    You need to provide API keys and other configuration details in the `src/notifier.py` and `src/ai_processor.py` files.

    -   **`src/ai_processor.py`**:
        -   `API_KEY`: Your Google Generative AI API key.

    -   **`src/notifier.py`**:
        -   `TELEGRAM_TOKEN`: Your Telegram bot token.
        -   `CHAT_ID`: The ID of the Telegram chat where you want to receive notifications.
        -   `JOB_QUERY`: The search query for the job listings (e.g., "Software engineer internship").

## Usage

To run the bot, execute the `src` package as a module from the root directory of the project:

```bash
python -m src
```

The bot will then start scraping for jobs. If it finds any new listings, it will format them and send them to your configured Telegram channel.