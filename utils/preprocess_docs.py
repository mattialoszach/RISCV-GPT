import os
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

# Loading and Parsing PDFs
def load_all_riscv_pdfs(data_dir: str) -> list[Document]:
    documents = []
    filenames = [
        ("riscv-privileged.pdf", 7),    # PDF, Page Offset
        ("riscv-unprivileged.pdf", 20)  # PDF, Page Offset
    ]

    for filename, skip_pages in filenames:
        path = os.path.join(data_dir, filename)
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")

        loader = PyMuPDFLoader(path)
        docs = loader.load()

        docs = docs[skip_pages:] # Skip pages until offset
        
        # Metadata
        for d in docs:
            d.metadata["source_pdf"] = filename                                         # Actual File name (necessary Metadata 1)
            d.metadata["page_display"] = d.metadata.get("page", 0) + 1 - skip_pages     # Actual page metadata (necessary Metadata 2)
        documents.extend(docs)

    return documents

# Chunking with semantic seperation
def chunk_documents(documents: list[Document], chunk_size: int = 1000, overlap: int = 150) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        separators=["\n\n", "\n", " ", ""]
    )
    return splitter.split_documents(documents)


def preprocess_pdf_documents(data_dir: str = "data") -> list[Document]:
    """
    Loads and preprocesses the official RISC-V PDF specification documents for use in a vector database.

    This function performs the full preprocessing pipeline:
    - Loads both privileged and unprivileged PDFs from the specified data directory
    - Skips frontmatter pages such as title and table of contents
    - Adds useful metadata like the visible page number and file name
    - Splits each document into semantically meaningful, overlapping text chunks

    Returns:
        list[Document]: A list of chunked and metadata-rich Document objects, ready for embedding and retrieval.
    """
    docs = load_all_riscv_pdfs(data_dir)
    chunks = chunk_documents(docs)
    return chunks