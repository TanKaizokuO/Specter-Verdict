from typing import Dict, Any
from agents import get_llm
from rag.retriever import retrieve

JUDGE_PROMPT = """You are a neutral federal judge presiding over a pre-trial hearing.
You have access to relevant case law and procedural rules via retrieval.
Speak formally. Issue rulings concisely. Always cite retrieved precedent.
Current phase: {phase}
Retrieved context: {context}

Input query / pending action:
{query}

If rendering a ruling on an objection or final decision, start your response with one of the following words in all caps:
SUSTAINED, OVERRULED, DEFERRED, FINAL RULING
"""

class JudgeAgent:
    def __init__(self):
        self.llm = get_llm()

    def generate_response(self, phase: str, query: str) -> Dict[str, Any]:
        """
        Retrieves context and queries the LLM for the Judge's perspective.
        """
        # Retrieve context for Judge
        docs = retrieve(query, role="judge")
        context = "\n".join([f"[Doc: {d.metadata.get('source', 'Unknown')}] {d.page_content}" for d in docs])
        
        prompt = JUDGE_PROMPT.format(phase=phase, context=context, query=query)
        response = self.llm.invoke(prompt)
        
        content = response.content if hasattr(response, "content") else str(response)
        citations = list(set([d.metadata.get("source", "Unknown") for d in docs]))
        
        return {
            "speaker": "Judge",
            "content": content,
            "citations": citations
        }
