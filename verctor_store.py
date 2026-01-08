import chromadb
from chromadb.utils import embedding_functions
import uuid
#initialize the client
client = chromadb.PersistentClient(path="./chroma_db")

#embedding model. utomatically downloads a small, free model (all-MiniLM-L6-v2)
default_ef = embedding_functions.DefaultEmbeddingFunction()

# create collection
collection = client.get_or_create_collection(
    name="documind_collections",
    embedding_function=default_ef #type: ignore
)

def add_documents_to_db(filename:str, pages_text:list[str]):
   """
    Takes a list of page texts, turns them into vectors, and saves them
   """
   ids=[]
   metadatas=[]

   for i, text in enumerate(pages_text):
       # create a unique id for each page
       id = f"{filename}_page_{i+1}"
       ids.append(id)
       #store metadata so we know where this page came from
       metadatas.append({"filename": filename, "page_number": i+1})

       #chroma handles the vectorization automatically

       collection.add(
           documents=pages_text,
           metadatas=metadatas,
           ids=ids
       )

       print(f"Stored {len(pages_text)} pages from {filename} to the vector database.")

def query_documents(query_text:str, n_results:int=2):
           """
           Query the vector database for similar texts
           """
           results = collection.query(
               query_texts=[query_text],
               n_results=n_results
           )
           return results
