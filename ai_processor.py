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
    """
    Sends structured job data and the full description to the Gemini API and asks it to format it.
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