import os
import argparse
import yaml
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

from rag.embeddings import get_embeddings

def get_doc_type(filename: str) -> str:
    name = filename.lower()
    if any(k in name for k in ["precedent", "ruling", "statute", "case_law", "law"]):
        return "precedent"
    elif any(k in name for k in ["forensic", "photo", "evidence", "report", "lab"]):
        return "evidence"
    elif any(k in name for k in ["testimony", "statement", "deposition", "witness"]):
        return "testimony"
    elif any(k in name for k in ["motion", "rule", "procedure", "court"]):
        return "procedure"
    elif any(k in name for k in ["alibi", "character", "defense", "defendant"]):
        return "defense_doc"
    return "evidence"  # Default fallback

def ingest_documents(case_dir: str, config_path: str = "config/settings.yaml"):
    try:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        config = {}
        
    chunk_size = config.get("rag", {}).get("chunk_size", 512)
    chunk_overlap = config.get("rag", {}).get("chunk_overlap", 64)
    
    docs = []
    case_path = Path(case_dir)
    print(f"Scanning {case_dir} for documents...")
    
    if not case_path.exists():
        print(f"Directory {case_dir} does not exist.")
        return
        
    for file_path in case_path.rglob("*"):
        if file_path.is_file():
            loader = None
            if file_path.suffix == ".pdf":
                loader = PyPDFLoader(str(file_path))
            elif file_path.suffix == ".txt":
                loader = TextLoader(str(file_path))
            elif file_path.suffix == ".docx":
                try:
                    loader = Docx2txtLoader(str(file_path))
                except ImportError:
                    print("docx2txt not installed, skipping DOCX.")
                    continue
                
            if loader:
                try:
                    loaded_docs = loader.load()
                    doc_type = get_doc_type(file_path.name)
                    for d in loaded_docs:
                        d.metadata["doc_type"] = doc_type
                        d.metadata["source"] = file_path.name
                    docs.extend(loaded_docs)
                    print(f"Loaded {file_path.name} as {doc_type}")
                except Exception as e:
                    print(f"Error loading {file_path}: {e}")

    if not docs:
        print("No valid documents found.")
        return

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    splits = text_splitter.split_documents(docs)
    
    print(f"Split into {len(splits)} chunks. Storing in Chroma...")
    embeddings = get_embeddings()
    
    # Store locally
    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=embeddings,
        persist_directory="./data/vector_store/"
    )
    print("Ingestion complete!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest case documents into Vector DB")
    parser.add_argument("--case-dir", type=str, default="./data/case_files/", help="Path to case files directory")
    parser.add_argument("--config", type=str, default="config/settings.yaml", help="Path to settings.yaml")
    args = parser.parse_args()
    
    ingest_documents(args.case_dir, args.config)
