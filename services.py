import fitz # PyMuPDF
from fastapi import UploadFile

async def process_pdf_file(file: UploadFile) -> tuple[dict, list[dict]]:
    """
    Reads a pdf stream and extracts text per page.
    Returns metadata and list of pages with text.
    """

    content = await file.read()
    doc = fitz.open(stream=content, filetype="pdf")
    pages_data = []

    for index, page in enumerate(doc): #type: ignore
        text = page.get_text()
        clean_text = text.strip()

        pages_data.append({
            "page_number": index + 1,
            "char_count": len(clean_text),
            "text_content": clean_text
            })
    metadata = {
        "filename": file.filename,
        "file_size_bytes": len(content),
        "content_type": file.content_type
    }
    return metadata, pages_data