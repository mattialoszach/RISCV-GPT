from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document

# Format Context for System Prompt
def format_context_with_sources(documents):
    formatted_chunks = []
    metadata_source = set()
    for doc in documents:
        text = doc.page_content.strip()
        source = doc.metadata.get("source_pdf", "unknown")
        page = doc.metadata.get("page_display", "unknown")

        metadata_source.add(f"[{source}, {page}]")
        formatted_chunks.append(f"> {text}\n> [{source}, page {page}]")
    return metadata_source, "\n\n---\n\n".join(formatted_chunks)

template = """
You are a RISC-V specification expert. Provide a thorough, precise, plain-text explanation that directly answers the QUESTION. Plain text only (no Markdown, no bullets, no code, no headings).

Core rules:
- Answer the QUESTION using only the provided context as evidence. No meta-sentences (e.g., “can be found in section …”).
- If the answer is not in the context, reply exactly:
  "The information is not available in the provided context."
- Paraphrase; do not include long verbatim quotes.
- Give long, thoroughly responses.

Depth and completeness (must):
- Provide the most comprehensive answer possible based on the context. Do not shorten or omit relevant details that are present in the context.
- Include all pertinent information found in the context such as definitions, semantics, operand types, encoding/fields, constraints, privilege requirements, alignment rules, exceptions/faults, corner cases, and differences to related instructions—only if supported by the context.
- Use as many paragraphs as necessary. If distinct subtopics are involved, separate them into separate paragraphs. Avoid redundancy.

Context:
{context}

Question:
{question}

Answer:
"""

prompt = ChatPromptTemplate.from_template(template)