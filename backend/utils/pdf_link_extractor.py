import fitz  # PyMuPDF
import io

def extract_links_from_bytes(file_bytes: bytes):
    links = []

    doc = fitz.open(stream=file_bytes, filetype="pdf")

    for page in doc:
        for link in page.get_links():
            if "uri" in link:
                links.append(link["uri"])

    return links