DocuMind AI 🧠📂
An Intelligent Document Assistant powered by RAG (Retrieval-Augmented Generation) that answers questions from PDFs, images, and audio files.


Replace with actual demo GIF

Features ✨
📄 Multi-Format Support: Process PDFs, images (OCR), and audio (speech-to-text)

🎯 Accurate Answers: DeepSeek-R1 LLM with semantic search

🔒 Secure: Local processing (no data leaves your machine)

🖥️ User-Friendly: Streamlit web interface

Installation ⚙️
bash
Copy
Edit
# Clone the repository
git clone https://github.com/yourusername/DocuMind-AI.git
cd DocuMind-AI

# Install dependencies
pip install -r requirements.txt

# Install Tesseract OCR
# For Ubuntu/Debian
sudo apt install tesseract-ocr

# For macOS
brew install tesseract
Usage 🚀
bash
Copy
Edit
# Start the Streamlit app
streamlit run app.py
Upload documents (PDF/Images/Audio)

Ask questions about your files!

Tech Stack 🔧
Component	Technology Used
Document Processing	PyPDF2, EasyOCR, Whisper
Embeddings	HuggingFace (all-mpnet-base-v2)
Vector Store	FAISS
LLM	Ollama (DeepSeek-R1)
UI	Streamlit

Contributing 🤝
Pull requests are welcome!
Please refer to CONTRIBUTING.md for guidelines.

License 📜
This project is licensed under the MIT License.
See LICENSE for more information.

Customize 🛠️
Replace the demo placeholder image with a real GIF or screenshot.

Add screenshots in the /assets folder.

Include additional setup or environment details if needed.

Update repository URL and paths as necessary.
