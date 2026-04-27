import pytest
from agents.judge import JudgeAgent
from agents.defense import DefenseAgent
from agents.prosecutor import ProsecutorAgent
from unittest.mock import patch, MagicMock

@patch("agents.judge.get_llm")
@patch("agents.judge.retrieve")
def test_judge_agent_objection(mock_retrieve, mock_llm_factory):
    mock_llm = MagicMock()
    # Mock string response vs object content wrapper
    mock_llm.invoke.return_value.content = "SUSTAINED. The evidence is irrelevant."
    mock_llm_factory.return_value = mock_llm
    
    mock_retrieve.return_value = []
    
    agent = JudgeAgent()
    res = agent.generate_response("ruling", "Defense objects.")
    assert "SUSTAINED" in res["content"]
    assert res["speaker"] == "Judge"

@patch("agents.defense.get_llm")
@patch("agents.defense.retrieve")
def test_defense_agent_objection(mock_retrieve, mock_llm_factory):
    mock_llm = MagicMock()
    mock_llm.invoke.return_value.content = "I object! [OBJECTION: Hearsay]"
    mock_llm_factory.return_value = mock_llm
    
    mock_retrieve.return_value = []
    
    agent = DefenseAgent()
    res = agent.generate_response("rebuttal", "Respond")
    assert "[OBJECTION:" in res["content"]
    assert res["speaker"] == "Defense Attorney"
