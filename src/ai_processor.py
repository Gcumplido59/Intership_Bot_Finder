"""Handles the processing of job listings using a generative AI model."""

import google.generativeai as genai

# CONFIGURATION
API_KEY = ""

try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    print(f"Error configuring AI model: {e}")
    model = None

def format_job_listing(title: str, company: str, location: str, link: str, description: str) -> str:
    """Formats a job listing using a generative AI model.

    This function takes job listing details, sends them to a generative AI model,
    and returns a formatted string suitable for display.

    Args:
        title: The title of the job.
        company: The name of the company.
        location: The location of the job.
        link: The URL to the job posting.
        description: The full description of the job.

    Returns:
        A formatted string containing the job listing details, or a fallback
        string if the AI model fails.
    """
    if not model:
        return "AI Model is not configured. Please check your API key."

    prompt = f"""
    Format the following job information into a clean, well-spaced summary for a Telegram message.
    The output must follow this exact order and use Markdown formatting:
    1.  *Title*: (The job title)
    2.  *Company*: (The company name)
    3.  *Location*: (The location)
    4.  *Info*: (A concise 1-2 sentence summary based on the provided job description)
    5.  *Link*: (The URL to the job posting)
    
    Add a newline for spacing after the Location and Info sections.

    **Job Data:**
    - Title: {title}
    - Company: {company}
    - Location: {location}
    - Link: {link}
    - Full Description: {description}
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text.strip().replace('**', '*')
    except Exception as e:
        return f"*{title}*\n\n*Company:* {company}\n\n*Location:* {location}\n\n*Link:* {link}"