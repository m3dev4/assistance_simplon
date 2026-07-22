from langchain_community.document_loaders import PyPDFLoader
from chunks import create_document_chunks
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_classic.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_openai import ChatOpenAI
from vector_store import create_vector_store
import os 
import dotenv

dotenv.load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API")


llm = ChatOpenAI(
    model="poolside/laguna-m.1:free",
    temperature=0.1,
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

loader = PyPDFLoader("data/re-simplon.pdf")

documents = loader.load()


#  ---------------------------------- Nettoyage du texte -----------------------------

text = documents[1].page_content

documents_utiles = []

for doc in documents:
    if doc.metadata["page"] >= 2:
        documents_utiles.append(doc)

# ---------------------------- Chunk ----------------------------------------
documents_chunks = create_document_chunks(documents_utiles)

embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

vectorStore = create_vector_store(documents_chunks, embeddings=embeddings)

retriever = vectorStore.as_retriever(
    search_kwargs={
        "k": 2
    }
)


for chunk in documents_chunks:
    print('=' * 100)
    print("TYPE :", chunk.metadata["type"])
    print(chunk.page_content[:300])

prompt = ChatPromptTemplate.from_template(
"""
Tu es l'assistant officiel du règlement intérieur de Simplon Sénégal.

Ton rôle est d'aider les apprenants à comprendre les règles de la formation.

Consignes :

- Réponds de manière claire, naturelle et pédagogique.
- Utilise uniquement les informations présentes dans le contexte.
- Ne dis jamais que tu vois "un contexte" ou "des documents fournis".
- Ne mentionne pas les limites de ta recherche sauf si l'information est réellement absente.
- Si l'information n'existe pas, répond simplement :
  "Je ne trouve pas cette information dans le règlement intérieur."

Quand c'est pertinent :
- cite le numéro de l'article concerné ;
- résume les règles sous forme de liste ;
- ajoute les horaires ou détails importants.

Contexte :
{context}

Question :
{input}

Réponse :
"""
)

document_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, document_chain)

def ask_question(question):
    response = rag_chain.invoke(
        {
            "input": question
        }
    )
    return response