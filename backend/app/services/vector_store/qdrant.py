from typing import List, Any
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_community.vectorstores import Qdrant

from .base import BaseVectorStore

class QdrantStore(BaseVectorStore):
    """Qdrant vector store implementation"""
    
    def __init__(self, collection_name: str, embedding_function: Embeddings, **kwargs):
        """Initialize Qdrant vector store"""
        url = kwargs.get('url', 'http://localhost:6333')
        prefer_grpc = kwargs.get('prefer_grpc', True)
        
        self._store = Qdrant(
            collection_name=collection_name,
            embeddings=embedding_function,
            url=url,
            prefer_grpc=prefer_grpc
        )
    
    def add_documents(self, documents: List[Document]) -> None:
        """Add documents to Qdrant"""
        self._store.add_documents(documents)
    
    def delete(self, ids: List[str]) -> None:
        """Delete documents from Qdrant"""
        self._store.delete(ids)
    
    def as_retriever(self, **kwargs: Any):
        """Return a retriever interface"""
        return self._store.as_retriever(**kwargs)
    
    def similarity_search(self, query: str, k: int = 4, **kwargs: Any) -> List[Document]:
        """Search for similar documents in Qdrant"""
        return self._store.similarity_search(query, k=k, **kwargs)
    
    def similarity_search_with_score(self, query: str, k: int = 4, **kwargs: Any) -> List[Document]:
        """Search for similar documents in Qdrant with score"""
        return self._store.similarity_search_with_score(query, k=k, **kwargs)

    def delete_collection(self) -> None:
        """Delete the entire collection"""
        self._store._client.delete_collection(self._store._collection_name) 