from gtts import gTTS
import PyPDF2
import os
import logging

# Configure logging
logging.basicConfig(filename='pdf_to_audio.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def is_valid_pdf(file_path):
    """ Check if the file is a PDF and not too large. """
    if not file_path.lower().endswith('.pdf'):
        logging.error("Invalid file type. Expected a PDF.")
        return False
    if os.path.getsize(file_path) > 25 * 1024 * 1024:  # Limit to 25 MB
        logging.error("File size exceeds 25 MB limit.")
        return False
    return True

def pdf_to_text(pdf_path):
    """ Extract text from a PDF file. """
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                page_text = page.extract_text()
                if page_text:
                    text += page_text
    except Exception as e:
        logging.error(f"Error extracting text from PDF: {e}")
        return None
    return text

def sanitize_text(text):
    """ Sanitize text to remove unwanted characters. """
    # Example: Remove non-printable characters
    sanitized_text = ''.join(char for char in text if char.isprintable())
    return sanitized_text

def text_to_audio(text, audio_path):
    """ Convert text to audio and save it as an MP3 file. """
    try:
        tts = gTTS(text=text, lang='en')
        tts.save(audio_path)
    except Exception as e:
        logging.error(f"Error converting text to audio: {e}")
        return False
    return True

def main():
    pdf_path = 'example.pdf'  # Path to your PDF file
    audio_path = 'output.mp3'  # Path to save the audio file
    
    # Validate the input file
    if not is_valid_pdf(pdf_path):
        return
    
    # Convert PDF to text
    logging.info("Extracting text from PDF...")
    text = pdf_to_text(pdf_path)
    
    if text is None or not text.strip():
        logging.error("No text found or an error occurred.")
        return
    
    # Sanitize the extracted text
    sanitized_text = sanitize_text(text)
    
    # Convert text to audio
    logging.info("Converting text to audio...")
    if text_to_audio(sanitized_text, audio_path):
        logging.info(f"Audio file saved as {audio_path}")
    else:
        logging.error("Failed to save the audio file.")

if __name__ == "__main__":
    main()
