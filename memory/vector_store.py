import hashlib
import os
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SearchField,
    SearchFieldDataType,
    SimpleField,
    SearchableField,
    VectorSearch,
    HnswAlgorithmConfiguration,
    VectorSearchProfile,
)
from azure.search.documents.models import VectorizedQuery

load_dotenv()


class AzureAISearchVectorStore:
    """Vector store implementation using Azure AI Search."""

    def __init__(
        self,
        endpoint: Optional[str] = None,
        api_key: Optional[str] = None,
        index_name: Optional[str] = None,
        embedding_dimension: int = 1536,
    ):
        self.endpoint = endpoint or os.getenv("AZURE_SEARCH_ENDPOINT")
        self.api_key = api_key or os.getenv("AZURE_SEARCH_API_KEY")
        self.index_name = index_name or os.getenv(
            "AZURE_SEARCH_INDEX_NAME", "research-papers"
        )
        self.embedding_dimension = embedding_dimension

        if not self.endpoint or not self.api_key:
            raise ValueError("Azure Search endpoint and API key are required")

        self.credential = AzureKeyCredential(self.api_key)
        self.index_client = SearchIndexClient(
            endpoint=self.endpoint, credential=self.credential
        )
        self.search_client = SearchClient(
            endpoint=self.endpoint,
            index_name=self.index_name,
            credential=self.credential,
        )
        self._ensure_index()

    def create_index(self) -> None:
        """Create the search index if it doesn't exist."""
        fields = [
            SimpleField(
                name="id", type=SearchFieldDataType.String, key=True, filterable=True
            ),
            SearchableField(
                name="content", type=SearchFieldDataType.String, searchable=True
            ),
            SearchableField(
                name="title", type=SearchFieldDataType.String, searchable=True
            ),
            SimpleField(
                name="source",
                type=SearchFieldDataType.String,
                filterable=True,
                facetable=True,
            ),
            SimpleField(name="metadata", type=SearchFieldDataType.String),
            SearchField(
                name="embedding",
                type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
                searchable=True,
                vector_search_dimensions=self.embedding_dimension,
                vector_search_profile_name="vector-profile",
            ),
        ]

        vector_search = VectorSearch(
            algorithms=[
                HnswAlgorithmConfiguration(
                    name="hnsw-algorithm",
                ),
            ],
            profiles=[
                VectorSearchProfile(
                    name="vector-profile",
                    algorithm_configuration_name="hnsw-algorithm",
                ),
            ],
        )

        index = SearchIndex(
            name=self.index_name, fields=fields, vector_search=vector_search
        )
        try:
            self.index_client.get_index(self.index_name)
            print("Index already exists")
        except:
            self.index_client.create_index(index)

    def _ensure_index(self):
        try:
            self.index_client.get_index(self.index_name)
        except Exception:
            self.create_index()


    def _document_exists(self, doc_id: str) -> bool:
        """Check if a document already exists in the index."""
        try:
            self.search_client.get_document(key=doc_id)
            return True
        except Exception:
            return False

    def add_documents(
        self, documents: List[Dict[str, Any]], embeddings: List[List[float]]
    ) -> None:
        """
        Add documents with their embeddings to the index
        """
        docs_to_upload = []
        for doc, embedding in zip(documents, embeddings):
            upload_doc = {
                "id": doc.get("id"),
                "content": doc.get("content", ""),
                "title": doc.get("title", ""),
                "source": doc.get("source", ""),
                "metadata": str(doc.get("metadata", {})),
                "embedding": embedding,
            }
            docs_to_upload.append(upload_doc)

        result = self.search_client.merge_or_upload_documents(documents=docs_to_upload)
        print(
            f"Uploaded {len(docs_to_upload)} documents. Succeeded: {len([r for r in result if r.succeeded])}"
        )

    def search(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        filters: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Perform a vector similarity search.
        """
        vector_query = VectorizedQuery(
            vector=query_embedding, k_nearest_neighbors=top_k, fields="embedding"
        )

        results = self.search_client.search(
            search_text=None, vector_queries=[vector_query], filter=filters, top=top_k
        )

        search_results = []
        for result in results:
            search_results.append(
                {
                    "id": result.get("id"),
                    "content": result.get("content"),
                    "title": result.get("title"),
                    "source": result.get("source"),
                    "metadata": result.get("metadata"),
                    "score": result.get("@search.score"),
                }
            )

        return search_results

    def hybrid_search(
        self,
        query_text: str,
        query_embedding: List[float],
        top_k: int = 5,
        filters: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Perform a hybrid search combining text and vector search.
        """
        vector_query = VectorizedQuery(
            vector=query_embedding, k_nearest_neighbors=top_k, fields="embedding"
        )

        results = self.search_client.search(
            search_text=query_text,
            vector_queries=[vector_query],
            filter=filters,
            top=top_k,
        )

        search_results = []
        for result in results:
            search_results.append(
                {
                    "id": result.get("id"),
                    "content": result.get("content"),
                    "title": result.get("title"),
                    "source": result.get("source"),
                    "metadata": result.get("metadata"),
                    "score": result.get("@search.score"),
                }
            )

        return search_results

    def delete_documents(self, document_ids: List[str]) -> None:
        """
        Delete documents by their IDs.
        """
        documents_to_delete = [{"id": doc_id} for doc_id in document_ids]
        self.search_client.delete_documents(documents=documents_to_delete)
        print(f"Deleted {len(document_ids)} documents.")

    def delete_index(self) -> None:
        """Delete the entire search index."""
        self.index_client.delete_index(self.index_name)
        print(f"Index '{self.index_name}' deleted.")

    def reset(self) -> None:
        try:
            self.index_client.delete_index(self.index_name)
            print(f"Index '{self.index_name}' deleted.")
        except Exception:
            print("Index did not exist.")

        self.create_index()
        print(f"Index '{self.index_name}' recreated.")


VectorStore = AzureAISearchVectorStore
