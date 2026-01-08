from fastapi import FastAPI, UploadFile, File, HTTPException
from schemas import DocumentMetadata, ExtractedPage, DocumentResponse, SearchQuery, SearchResult
from verctor_store import add_documents_to_db, query_documents
from services import process_pdf_file
import uvicorn

app = FastAPI(title="DocuMind PDF Vector Store API + RAG", version="1.0.0")

#updaed ingest endpoint
@app.post("/api/v1/ingest", response_model=DocumentResponse)
async def ingest_document(file:UploadFile=File(...)):
    """
    Ingests a PDF document, extracts text per page, and stores in vector DB.
    """
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
    try:
        #process the PDF file
        metadata_dict, pages_data = await process_pdf_file(file)

        #add documents to vector DB
        text_content = [page["text_content"] for page in pages_data]
        add_documents_to_db(metadata_dict["filename"], text_content)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
    
    #prepare response
    return DocumentResponse(
        metadata=DocumentMetadata(**metadata_dict),
        pages=[ExtractedPage(**page) for page in pages_data]
    )