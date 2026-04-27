import os
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from typing import Generator

def get_client() -> ChatNVIDIA:
    return ChatNVIDIA(
        model="moonshotai/kimi-k2-instruct-0905",
        api_key=os.environ.get("NVIDIA_API_KEY") 
    )

# Alias to avoid breaking compatibility with existing agent scripts
get_llm = get_client
