import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings

def get_embeddings():
    """
    Returns the configured embedding model based on environment variables.
    Defaults to OpenAI text-embedding-3-small if OPENAI_API_KEY is present,
    otherwise falls back to a local HuggingFace nomad-embed-text-v1 or similar model.
    """
    if os.getenv("OPENAI_API_KEY"):
        return OpenAIEmbeddings(model="text-embedding-3-small")
    
    # Fallback to local model via sentence-transformers
    # Note: nomic-embed-text-v1 requires trust_remote_code=True for HuggingFace
    return HuggingFaceEmbeddings(
        model_name="nomic-ai/nomic-embed-text-v1",
        model_kwargs={"trust_remote_code": True}
    )
