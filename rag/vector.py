import os
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from utils.preprocess_docs import preprocess_pdf_documents

db_location = "./vectorstore"
collection_name = "riscv_spec"

embeddings = OllamaEmbeddings(model="mxbai-embed-large") # Model for embeddings

# Define Vector Database
vector_store = Chroma(
    collection_name=collection_name,
    persist_directory=db_location,
    embedding_function=embeddings
)

# Only if Vector Database does not exist yet
if vector_store._collection.count() == 0:
    print("⚙️ Initializing vectorstore...")
    chunks = preprocess_pdf_documents()
    vector_store.add_documents(documents=chunks)
    print(f"✅ {len(chunks)} documents successfully added.")
else:
    print("✅ Vectorstore already initialized.")

retriever = vector_store.as_retriever(
    search_kwargs={"k": 5} # Optional: Retrieval amount of entries in DB
)