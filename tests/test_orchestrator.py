import pytest
from simulation.orchestrator import Simulator
from unittest.mock import patch, MagicMock

@patch("simulation.orchestrator.JudgeAgent")
@patch("simulation.orchestrator.ProsecutorAgent")
@patch("simulation.orchestrator.DefenseAgent")
@patch("simulation.orchestrator.export_transcript")
@patch("builtins.input", return_value="")
def test_simulator_termination(mock_input, mock_export, mock_def, mock_pros, mock_judge):
    # Mock judge returning CASE DISMISSED to end early
    mock_j_instance = MagicMock()
    mock_j_instance.generate_response.return_value = {"content": "CASE DISMISSED", "citations": []}
    mock_judge.return_value = mock_j_instance
    
    sim = Simulator("TEST-CASE")
    sim.run()
    
    # Should only run 1 round then exit because of dismissal
    assert sim.state.round == 1
    mock_export.assert_called()
