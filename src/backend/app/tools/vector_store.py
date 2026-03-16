from __future__ import annotations

from typing import List

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from app.config import settings
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


def build_vector_store(texts: List[str], metadatas: List[dict] | None = None) -> FAISS:
    """Build an in-memory FAISS vector store from a list of text strings."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs: List[Document] = []

    for i, text in enumerate(texts):
        chunks = splitter.create_documents([text], metadatas=[metadatas[i] if metadatas else {}])
        docs.extend(chunks)

    logger.info(f"Building vector store with {len(docs)} chunks from {len(texts)} documents")

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    store = FAISS.from_documents(docs, embeddings)
    return store


def similarity_search(store: FAISS, query: str, k: int = 4) -> List[str]:
    """Search the vector store and return top-k relevant text chunks."""
    results = store.similarity_search(query, k=k)
    return [doc.page_content for doc in results]
