from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document

def format_context_with_sources(documents: list[Document]) -> str:
    formatted_chunks = []
    for doc in documents:
        text = doc.page_content.strip()
        source = doc.metadata.get("source_pdf", "unknown")
        page = doc.metadata.get("page_display", "unknown")
        formatted_chunks.append(f"{text}\n[{source}, page {page}])\n")
    return "\n---\n".join(formatted_chunks)

template = """
You are a RISC-V architecture expert assistant. You are answering questions strictly based on official documentation excerpts.

You are given relevant chunks of the RISC-V specification with citation information embedded directly after each paragraph.

Your task:
- Only use information from the provided context.
- Do NOT answer based on prior knowledge.
- If the answer is not found in the context, say:
  "The information is not available in the provided context."

Answer the question with:
- Clear, technical paragraphs.
- After each paragraph, include a citation like: [source_pdf, page page_display]
- Use only the provided citations, no made-up references.

Use simple Markdown formatting (e.g., **bold**, lists, etc.) for readability.

Context:
{context}

Question:
{question}

Answer:
"""

prompt = ChatPromptTemplate.from_template(template)