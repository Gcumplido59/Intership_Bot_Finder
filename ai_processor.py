# In ai_processor.py
import google.generativeai as genai

# --- CONFIGURATION ---
# Replace "YOUR_API_KEY" with the key you just got from Google AI Studio.
API_KEY = "AIzaSyAU0DS50wzsEb9_bZzArGfwDnwr9V9TXIw"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash') # A fast and capable model

def summarize_job_description(text):
    """
    Sends the job description to the Gemini API and asks it to summarize.
    """
    if not text:
        return "No description provided."

    # This is the instruction we give to the AI.
    prompt = f"""
    Analyze the following job description text and extract the key information.
    Present the output cleanly under the following headings:
    - **Required Skills**: (List the key technical and soft skills as a comma-separated list)
    - **Key Responsibilities**: (Provide a 2-3 bullet point summary of the main tasks)
    - **Location**: (Extract the city and state)

    Here is the job description:
    ---
    {text}
    ---
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Could not process description with AI. Error: {e}"