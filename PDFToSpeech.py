
import PyPDF2
from gtts import gTTS

def pdf_to_text(pdf_path):
    """Extract text from a PDF file."""
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

def text_to_speech(text, output_file="audiobook.mp3", language="en"):
    """Convert text to speech and save as MP3."""
    tts = gTTS(text=text, lang=language)
    tts.save(output_file)
    print(f"Audiobook saved as {output_file}")

if __name__ == "__main__":
    pdf_path = "sample.pdf"  # Replace with your PDF file path
    extracted_text = pdf_to_text(pdf_path)
    print("Text extracted successfully. Converting to speech...")
    text_to_speech(extracted_text)

# ✅ How to Run

# Install dependencies:
# pip install PyPDF2 gTTS

# Place your PDF file in the same directory and update pdf_path in the script.
# Run the script:
# python pdf_to_speech.py

# Your audiobook will be saved as audiobook.mp3.