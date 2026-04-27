import pytest
from rag.retriever import retrieve
from unittest.mock import patch, MagicMock

@patch("rag.retriever.get_vectorstore")
def test_retrieve_filters(mock_get_vs):
    mock_vs = MagicMock()
    mock_get_vs.return_value = mock_vs
    
    retrieve("test query", "judge", top_k=2)
    mock_vs.similarity_search.assert_called_with(
        "test query", 
        k=2, 
        filter={"doc_type": {"$in": ["precedent", "procedure"]}}
    )
    
@patch("rag.retriever.get_vectorstore")
def test_prosecutor_retrieval(mock_get_vs):
    mock_vs = MagicMock()
    mock_get_vs.return_value = mock_vs
    
    retrieve("test", "prosecutor", top_k=5)
    mock_vs.similarity_search.assert_called_with(
        "test", 
        k=5, 
        filter={"doc_type": {"$in": ["evidence", "testimony", "precedent"]}}
    )
