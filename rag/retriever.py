import yaml
from typing import List
from langchain_chroma import Chroma
from langchain_core.documents import Document
from rag.embeddings import get_embeddings

def get_vectorstore(persist_directory: str = "./data/vector_store/") -> Chroma:
    """Returns the Chroma vectorstore initialized with the embedding function."""
    embeddings = get_embeddings()
    return Chroma(persist_directory=persist_directory, embedding_function=embeddings)

def retrieve(query: str, role: str, top_k: int = None) -> List[Document]:
    """
    Retrieve documents relevant to the query, scoped by the specified role's permissions.
    """
    if top_k is None:
        try:
            with open("config/settings.yaml", "r") as f:
                config = yaml.safe_load(f)
                top_k = config.get("rag", {}).get("top_k", 5)
        except Exception:
            top_k = 5
            
    role_filters = {
        "judge":      ["precedent", "procedure"],
        "prosecutor": ["evidence", "testimony", "precedent"],
        "defense":    ["defense_doc", "testimony", "procedure"],
    }
    
    allowed_types = role_filters.get(role.lower(), ["evidence", "testimony", "precedent", "procedure", "defense_doc"])
    
    search_kwargs = {
        "k": top_k,
        "filter": {"doc_type": {"$in": allowed_types}}
    }
    
    vectorstore = get_vectorstore()
    docs = vectorstore.similarity_search(query, **search_kwargs)
    
    return docs
