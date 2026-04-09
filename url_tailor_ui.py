# --- My Personal AI Resume Tailor ---
# Built by Dylan (with a lot of help from AI)
# Last updated: Oct 2025
#
# This script:
# 1. Grabs a job description from a URL.
# 2. Grabs a job title.
# 3. Asks my local Ollama AI to brainstorm buzzwords for that title.
# 4. Reads my MASTER_RESUME.docx file.
# 5. Asks Ollama to rewrite my Summary, Bullet Points, and Skills
#    using the job info, *without lying* (this part is super important).
# 6. Shows it all in a simple UI.
#

# --- Imports ---
import re
import requests
from bs4 import BeautifulSoup
from docx import Document
import ollama
import sys
import threading

# Import the UI libraries (this makes the window)
import tkinter as tk
from tkinter import scrolledtext, messagebox

# --- CONFIGURATION ---
OLLAMA_MODEL = 'llama3' # Make sure this model is downloaded!

# --- STOP WORDS ---
# A list of boring words to ignore. I can add more to this list later.
STOP_WORDS = set([
    'a', 'an', 'and', 'the', 'in', 'on', 'of', 'for', 'with', 'to', 'is', 'are', 'was', 'were',
    'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them',
    'my', 'your', 'his', 'its', 'our', 'their', 'at', 'by', 'from', 'about',
    'be', 'have', 'has', 'do', 'does', 'did', 'will', 'can', 'should', 'would',
    'years', 'experience', 'required', 'responsibilities', 'skills', 'etc',
    'including', 'such', 'as', 'role', 'work', 'new', 'team', 'company', 'job',
    'about', 'description', 'requirements', 'preferred', 'qualifications'
])

# --- HELPER FUNCTIONS ---
# These are just the backend tools, no need to edit these.

def get_text_from_url(url):
    """
    Goes to the URL and tries to grab all the text.
    It pretends to be a browser so it doesn't get blocked.
    """
    try:
        # A common user-agent to look like a real browser
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        response = requests.get(url, headers=headers)
        response.raise_for_status() # This will error if the page is 404 or 500
        
        # Use BeautifulSoup to parse the messy HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Nuke all the script and style tags, we don't want that text
        for script_or_style in soup(["script", "style"]):
            script_or_style.decompose()
            
        # Get all the text, nice and clean
        text = soup.get_text()
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        if not text:
            return None, "Couldn't find any text on that page, even after parsing."
        return text, None
        
    except requests.exceptions.RequestException as e:
        print(f"DEBUG: get_text_from_url failed: {e}") # A print for my terminal
        return None, f"Error fetching URL: {e}"

def get_text_from_docx(file_name):
    """
    Pulls all the text out of my MASTER_RESUME.docx file.
    """
    try:
        doc = Document(file_name)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        return '\n'.join(full_text), None
    except Exception as e:
        print(f"DEBUG: get_text_from_docx failed: {e}") # A print for my terminal
        return None, f"Error reading '{file_name}': {e}\nMake sure 'MASTER_RESUME.docx' is in the same folder."

def process_text(text):
    """
    This just takes a big blob of text and splits it into a list of
    unique keywords, minus all the boring stop-words.
    """
    if not text: return set()
    words = re.findall(r'\b[a-zA-Z0-9-]{2,}\b', text.lower())
    unique_words = set(words) - STOP_WORDS
    return unique_words

def call_ollama(prompt):
    """
    The "magic" function. Sends a prompt to my local Ollama.
    """
    print(f"--- Sending new prompt to {OLLAMA_MODEL} ---") # A print for my terminal
    try:
        response = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[{'role': 'user', 'content': prompt}],
        )
        print("--- Got response from Ollama ---") # A print for my terminal
        return response['message']['content'], None
    except Exception as e:
        print(f"DEBUG: call_ollama FAILED: {e}") # A print for my terminal
        return None, f"OLLAMA ERROR: {e}\nIs 'ollama serve' running? Do you have '{OLLAMA_MODEL}' installed?"

# --- MAIN LOGIC FUNCTION ---
# This is what runs when I click the button.
def start_tailoring_logic():
    
    # 1. Get the text from the UI boxes
    url = job_url_entry.get()
    job_title = job_title_entry.get() 
    
    # A little validation
    if not url:
        messagebox.showerror("Oops", "Please paste a job URL.")
        return
    if not job_title:
        messagebox.showerror("Oops", "Please enter the job title (e.g., 'Software Developer').")
        return
    
    # Get the output box ready
    output_box.config(state=tk.NORMAL)
    output_box.delete('1.0', tk.END)
    
    # A little helper to make writing to the UI easier
    def write_to_output(message):
        output_box.insert(tk.END, message + "\n")
        output_box.see(tk.END) # <-- THIS IS THE FIXED LINE (added a parenthesis)
        window.update_idletasks() # Refresh the window

    # 2. Let's get started!
    write_to_output(f"--- Okay, let's tailor your resume for: {job_title} ---")
    
    write_to_output("Reading job description from URL...")
    job_text, err = get_text_from_url(url)
    if err:
        write_to_output(f"FATAL ERROR: {err}")
        output_box.config(state=tk.DISABLED)
        return
    write_to_output("✓ Got it. Job description looks good.")

    write_to_output("Reading your MASTER_RESUME.docx...")
    resume_text, err = get_text_from_docx('MASTER_RESUME.docx')
    if err:
        write_to_output(f"FATAL ERROR: {err}")
        output_box.config(state=tk.DISABLED)
        return
    write_to_output("✓ Found your resume. All good.")
    
    # --- 3. The new AI Buzzword step ---
    write_to_output(f"\n--- Step 0: Asking AI for buzzwords for '{job_title}' ---")
    
    buzzword_prompt = f"""
    What are 10-15 key buzzwords and important phrases for a '{job_title}' role?
    I just want a single line of comma-separated values, nothing else.
    Example: Python, SQL, Data Analysis, Project Management
    """
    
    ai_buzzword_text, err = call_ollama(buzzword_prompt)
    if err:
        write_to_output(f"FATAL ERROR: {err}")
        output_box.config(state=tk.DISABLED)
        return
        
    # Tidy up the AI's response
    ai_buzzwords = [b.strip() for b in ai_buzzword_text.split(',')]
    write_to_output(f"✓ AI Buzzwords generated: {', '.join(ai_buzzwords[:5])}...")

    # 4. Keyword analysis (this is just for the prompt)
    job_keywords = process_text(job_text)
    resume_keywords = process_text(resume_text)
    missing_keywords = job_keywords - resume_keywords
    
    # This is the "inspiration list" we'll give to the AI prompts
    inspiration_list = list(ai_buzzwords) + list(missing_keywords)[:15]
    inspiration_context = ", ".join(inspiration_list)


    # 5. Call Ollama (Summary)
    write_to_output(f"\n--- Step 1: Rewriting your Professional Summary ---")
    summary_prompt = f"""
    You are a professional resume writer. Your task is to rewrite a 2-3 sentence professional summary for my resume.
    
    **The Goal:** Rephrase my existing experience to match the Job Description.
    
    **My Master Resume:**
    {resume_text}
    
    **The Job Description:**
    {job_text}
    
    **Inspiration Keywords (use these if they fit):**
    {inspiration_context}
    
    **CRITICAL RULE:** Do not add any skills, metrics, facts, or experiences that are not in my resume.
    Do not lie or exaggerate. Your goal is to rephrase my truth, not invent new truths.
    
    Now, write *only* the new, tailored professional summary.
    """
    
    new_summary, err = call_ollama(summary_prompt)
    if err:
        write_to_output(f"FATAL ERROR: {err}")
        output_box.config(state=tk.DISABLED)
        return
    write_to_output("--- YOUR NEW SUMMARY (Copy this) ---")
    write_to_output(new_summary)
    write_to_output("-------------------------------------")

    # 6. Call Ollama (Bullet Points)
    write_to_output(f"\n--- Step 2: Rewriting your Bullet Points ---")
    bullets_prompt = f"""
    You are a professional resume writer. Your task is to rewrite 3-5 of the *most relevant* bullet points from my resume.
    
    **The Goal:** Make my existing bullet points sound more impactful for *this specific* Job Description.
    
    **My Master Resume:**
    {resume_text}
    
    **The Job Description:**
    {job_text}
    
    **Inspiration Keywords (use these if they fit):**
    {inspiration_context}
    
    **CRITICAL RULE:** Do not invent new metrics, numbers, or responsibilities. You must only rephrase my existing accomplishments.
    Stick to the facts provided in my resume.
    
    Now, write *only* the 3-5 new, rewritten bullet points.
    """
    
    new_bullets, err = call_ollama(bullets_prompt)
    if err:
        write_to_output(f"FATAL ERROR: {err}")
        output_box.config(state=tk.DISABLED)
        return
    write_to_output("--- YOUR NEW BULLET POINTS (Copy these) ---")
    write_to_output(new_bullets)
    write_to_output("-----------------------------------------")

    # 7. Call Ollama (Skills Section)
    write_to_output(f"\n--- Step 3: Rewriting your Skills Section ---")
    skills_prompt = f"""
    You are a professional resume writer. Your task is to create a new, tailored 'Skills' section for my resume.

    **The Goal:** Re-organize my *existing* skills to highlight what this job wants.
    
    **CRITICAL RULE (No Lies):** You *must only* use skills that are present in my **Master Resume**.
    Do not invent *any* new skills.
    
    **Instructions:**
    1.  Read my **Master Resume** to find all my skills.
    2.  Read the **Job Description** and **Inspiration Keywords** to see what's most important.
    3.  Create a new 'Skills' section, categorized and prioritized, using *only* my existing skills.
    
    **My Master Resume (contains all my skills):**
    ---
    {resume_text}
    ---
    
    **The Job Description (what they want):**
    ---
    {job_text}
    ---

    **Inspiration Keywords (for prioritization):**
    ---
    {inspiration_context}
    ---
    
    Now, write *only* the new, tailored Skills section.
    """
    
    new_skills, err = call_ollama(skills_prompt)
    if err:
        write_to_output(f"FATAL ERROR: {err}")
        output_box.config(state=tk.DISABLED)
        return
    write_to_output("--- YOUR NEW SKILLS SECTION (Copy this) ---")
    write_to_output(new_skills)
    write_to_output("-----------------------------------------")
    
    # 8. All done!
    write_to_output("\n--- All Done! AI Tailoring Complete ---")
    output_box.config(state=tk.DISABLED)

# --- Threading ---
# This function wraps the main logic in a "thread".
# It just means the UI won't freeze while the AI is "thinking".
def on_tailor_button_click():
    
    # Disable button so I don't click it twice
    tailor_button.config(state=tk.DISABLED, text="Tailoring... Please Wait")
    
    # This function-inside-a-function is a bit weird,
    # but it's the standard way to do threading in tkinter.
    def run_in_thread():
        # Try to run the main logic
        try:
            start_tailoring_logic()
        except Exception as e:
            # If anything *really* breaks, show it
            print(f"DEBUG: Uncaught error in thread: {e}")
            messagebox.showerror("Fatal Error", f"Something went wrong: {e}")
        finally:
            # Always re-enable the button when done
            tailor_button.config(state=tk.NORMAL, text="Tailor Resume")
        
    # Start the thread
    threading.Thread(target=run_in_thread, daemon=True).start()

# --- THE UI (User Interface) SETUP ---
# This is just the code to draw the window and buttons.

# 1. Create the main window
window = tk.Tk()
window.title("My AI Resume Tailor")
window.geometry("700x550") # A little taller for the new box

# 2. Create the widgets
frame = tk.Frame(window, padx=10, pady=10)
frame.pack(fill=tk.BOTH, expand=True)

job_url_label = tk.Label(frame, text="Paste Job URL:")
job_url_label.pack(anchor=tk.W) # anchor=W means 'West' (align left)

job_url_entry = tk.Entry(frame, width=80)
job_url_entry.pack(fill=tk.X, expand=True) 

# New widgets for the Job Title
job_title_label = tk.Label(frame, text="Enter Job Title (e.g., 'Product Manager'):")
job_title_label.pack(anchor=tk.W, pady=(10,0)) # (top, bottom) padding

job_title_entry = tk.Entry(frame, width=80)
job_title_entry.pack(fill=tk.X, expand=True)

# The main button
tailor_button = tk.Button(frame, text="Tailor Resume", command=on_tailor_button_click)
tailor_button.pack(pady=10) # A little padding on top/bottom

# The big output box
output_box = scrolledtext.ScrolledText(frame, wrap=tk.WORD, height=25, state=tk.DISABLED)
output_box.pack(fill=tk.BOTH, expand=True)

# 3. Start the UI!
# This line is what actually opens the window and waits for me to click.
window.mainloop()