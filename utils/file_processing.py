import os
import tempfile
from PyPDF2 import PdfReader
from PIL import Image
import pytesseract
from faster_whisper import WhisperModel
from langchain.text_splitter import RecursiveCharacterTextSplitter
from config import CHUNK_SIZE, CHUNK_OVERLAP

# Initialize text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP
)

def extract_text_from_pdf(uploaded_file):
    """Extracts text from a PDF file."""
    try:
        reader = PdfReader(uploaded_file)
        return "".join([page.extract_text() or "" for page in reader.pages])
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return ""

def extract_text_from_image(image_file):
    """Extracts text from an image using OCR."""
    try:
        return pytesseract.image_to_string(Image.open(image_file)).strip()
    except Exception as e:
        print(f"Error with pytesseract: {e}")
        try:
            import easyocr
            reader = easyocr.Reader(['en'])
            return " ".join([res[1] for res in reader.readtext(image_file)]).strip()
        except Exception as e:
            print(f"Error with easyocr: {e}")
            return ""

def extract_text_from_audio(audio_file):
    """Extracts text from audio using faster-whisper with proper file handling."""
    try:
        # Create a temporary file with proper extension
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
            tmp_file.write(audio_file.getvalue())
            tmp_path = tmp_file.name

        # Initialize Whisper model
        model = WhisperModel("base", device="cpu")  # Change to "cuda" if GPU available
        
        # Transcribe audio
        segments, _ = model.transcribe(tmp_path)
        text = " ".join(segment.text for segment in segments)
        
        # Clean up temporary file
        os.unlink(tmp_path)
        
        return text.strip()
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        # Clean up if temp file was created
        if 'tmp_path' in locals() and os.path.exists(tmp_path):
            os.unlink(tmp_path)
        return ""

def process_files(uploaded_files, file_type):
    """Processes uploaded files and returns text chunks."""
    all_texts = []
    for uploaded_file in uploaded_files:
        try:
            if file_type == "pdf":
                raw_text = extract_text_from_pdf(uploaded_file)
            elif file_type == "image":
                raw_text = extract_text_from_image(uploaded_file)
            elif file_type == "audio":
                raw_text = extract_text_from_audio(uploaded_file)
            else:
                continue

            if raw_text.strip():
                all_texts.extend(text_splitter.split_text(raw_text))
        except Exception as e:
            print(f"Error processing {uploaded_file.name}: {e}")
    return all_texts