import re
from langchain_core.documents import Document




def create_document_chunks(documents):
    chunks = []

    full_text = "\n".join(
        doc.page_content for doc in documents
    )

    general_match = re.search(
        r"(DOCUMENT OFFICIEL.*?)(?=Sommaire)",
        full_text,
        re.DOTALL
    )

    if general_match:
        general_contents = general_match.group(1).strip()

        chunks.append(
            Document(
                page_content=general_contents,
                metadata={
                    "type": "general"
                }
            )
        )

    
    articles = list(
        re.finditer(
            r"Article\s+\d+\s*[—-]",
            full_text
        )
    )

    for i, match in enumerate(articles):
        start = match.start()

        if i + i < len(articles):
            end = articles[i + 1].start()
        else:
            end = len(full_text)

        content = full_text[start:end].strip()

        article_match = re.search(
            r"Article\s+(\d+)",
            content
        )

        article_number = (
            int(article_match.group(1))
            if article_match
            else None
        )

        chunks.append(
            Document(
                page_content =content,
                metadata={
                    "type": "article",
                    "article": article_number
                }
            )
        )

    contact_match = re.search(
        r"(CHAPITRE 4.*?)(?=Engagement de l'apprenant)",
        full_text,
        re.DOTALL
    )

    if contact_match:
        contact_content = contact_match.group(1).strip()

        chunks.append(
            Document(
                page_content=contact_content,
                metadata ={
                    "type": "contact"
                }
            )
        )
    
    return chunks