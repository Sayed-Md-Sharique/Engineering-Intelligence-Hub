import os
from pypdf import PdfReader

SUPPORTED = [
    ".pdf", ".txt", ".md", ".py", ".js", ".ts", ".java",
    ".cpp", ".c", ".h", ".json", ".yaml", ".yml"
]

def load_file(file_path):
    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text

    if extension in SUPPORTED:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
            return file.read()

    raise ValueError("Unsupported file type")
