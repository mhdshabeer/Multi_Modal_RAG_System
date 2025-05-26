# DocuMind AI 🧠📂

**An Intelligent Document Assistant** powered by RAG (Retrieval-Augmented Generation) that answers questions from PDFs, images, and audio files.

![Demo](https://via.placeholder.com/800x400?text=DocuMind+AI+Demo)  
*Replace with actual demo GIF*

---

## Features ✨

- 📄 **Multi-Format Support**: Process PDFs, images (OCR), and audio (speech-to-text)  
- 🎯 **Accurate Answers**: DeepSeek-R1 LLM with semantic search  
- 🔒 **Secure**: Local processing (no data leaves your machine)  
- 🖥️ **User-Friendly**: Streamlit web interface  

---

## Installation ⚙️

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/DocuMind-AI.git
cd DocuMind-AI
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Tesseract OCR

For Ubuntu/Debian:

```bash
sudo apt install tesseract-ocr
```

For macOS:

```bash
brew install tesseract
```

---

## Usage 🚀

Start the Streamlit app:

```bash
streamlit run app.py
```

Then:

1. Upload documents (PDF, image, or audio files)  
2. Ask questions about your content using the chat interface  

---

## Tech Stack 🔧

| Component           | Technology Used                 |
|---------------------|---------------------------------|
| Document Processing | PyPDF2, EasyOCR, Whisper        |
| Embeddings          | HuggingFace (all-mpnet-base-v2) |
| Vector Store        | FAISS                           |
| LLM                 | Ollama (DeepSeek-R1)            |
| UI                  | Streamlit                       |

---

## Contributing 🤝

Contributions are welcome!  
Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## License 📜

This project is licensed under the MIT License.  
See the [LICENSE](LICENSE) file for details.

---

## Customize 🛠️

- Replace the placeholder image with a real demo GIF or screenshot  
- Add screenshots to the `/assets` folder  
- Update the repo link and dependencies if needed  
- Include environment setup if applicable (e.g., `.env`, configs)
