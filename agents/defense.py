from typing import Dict, Any, Optional
from agents import get_llm
from rag.retriever import retrieve

DEFENSE_PROMPT = """You are a defense attorney in a pre-trial hearing. Your goal is to protect
your client's rights and challenge the sufficiency of the prosecution's evidence.
Raise objections when warranted using objection flags [OBJECTION: {{type}}]. 
Cite retrieved documents to support your position using inline citations [Doc: {{source}}].

Retrieved context: 
{context}

Prosecution's last argument: 
{prosecutor_last_argument}

Current phase/instructions: 
{query}
"""

class DefenseAgent:
    def __init__(self):
        self.llm = get_llm()

    def generate_response(self, phase: str, query: str, prosecutor_last_argument: Optional[str] = None) -> Dict[str, Any]:
        """
        Retrieves context and queries the LLM for the Defense's argument/objections.
        """
        docs = retrieve(query, role="defense")
        context = "\n".join([f"[Doc: {d.metadata.get('source', 'Unknown')}] {d.page_content}" for d in docs])
        
        prompt = DEFENSE_PROMPT.format(
            context=context,
            prosecutor_last_argument=prosecutor_last_argument or "None",
            query=query
        )
        
        response = self.llm.invoke(prompt)
        content = response.content if hasattr(response, "content") else str(response)
        citations = list(set([d.metadata.get("source", "Unknown") for d in docs]))
        
        return {
            "speaker": "Defense Attorney",
            "content": content,
            "citations": citations
        }
