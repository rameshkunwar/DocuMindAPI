from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

#search schemas for vector DB search
class SearchQuery(BaseModel):
    query:str
    top_k:int = 3


class SearchResult(BaseModel):
    text:str
    page_number:int
    score:float #how close the match is, lower is better in Chroma

#metadata schema for documents
class DocumentMetadata(BaseModel):
    filename: str
    file_size_bytes: int
    upload_date: datetime = Field(default_factory=datetime.now)
    content_type: str

# 3. Page Schema
class ExtractedPage(BaseModel):
    page_number: int
    char_count: int
    text_content: str

# 4. API Response Wrapper
class DocumentResponse(BaseModel):
    status: str = "success"
    metadata: DocumentMetadata
    pages: List[ExtractedPage]


