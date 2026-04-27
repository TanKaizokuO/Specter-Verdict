from typing import Dict, Any, Optional
from agents import get_llm
from rag.retriever import retrieve

PROSECUTOR_PROMPT = """You are a prosecutor in a pre-trial hearing. Your goal is to demonstrate
probable cause and argue for the charges to proceed to full trial.
Cite only retrieved evidence. Be persuasive but accurate.
Whenever citing, use inline evidence citations [Doc: {{source}}].

Retrieved context: 
{context}

Opposing argument (if any): 
{defense_last_argument}

Current phase/instructions: 
{query}
"""

class ProsecutorAgent:
    def __init__(self):
        self.llm = get_llm()

    def generate_response(self, phase: str, query: str, defense_last_argument: Optional[str] = None) -> Dict[str, Any]:
        """
        Retrieves context and queries the LLM for the Prosecutor's argument.
        """
        docs = retrieve(query, role="prosecutor")
        context = "\n".join([f"[Doc: {d.metadata.get('source', 'Unknown')}] {d.page_content}" for d in docs])
        
        prompt = PROSECUTOR_PROMPT.format(
            context=context,
            defense_last_argument=defense_last_argument or "None",
            query=query
        )
        
        response = self.llm.invoke(prompt)
        content = response.content if hasattr(response, "content") else str(response)
        citations = list(set([d.metadata.get("source", "Unknown") for d in docs]))
        
        return {
            "speaker": "Prosecutor",
            "content": content,
            "citations": citations
        }
