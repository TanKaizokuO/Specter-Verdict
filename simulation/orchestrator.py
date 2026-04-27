import yaml
from simulation.state import SimulationState, Turn, Ruling
from agents.judge import JudgeAgent
from agents.prosecutor import ProsecutorAgent
from agents.defense import DefenseAgent
from simulation.transcript import export_transcript

class Simulator:
    def __init__(self, case_id: str):
        self.state = SimulationState(case_id=case_id)
        self.judge = JudgeAgent()
        self.prosecutor = ProsecutorAgent()
        self.defense = DefenseAgent()
        
        try:
            with open("config/settings.yaml", "r") as f:
                config = yaml.safe_load(f)
                self.max_rounds = config.get("simulation", {}).get("max_rounds", 5)
                self.allow_human = config.get("simulation", {}).get("allow_human_injection", True)
                self.export_format = config.get("simulation", {}).get("export_format", "markdown")
        except Exception:
            self.max_rounds = 5
            self.allow_human = True
            self.export_format = "markdown"

    def run(self):
        print(f"--- Starting Simulation for Case: {self.state.case_id} ---")
        
        # Turn-based loop
        while self.state.round <= self.max_rounds:
            print(f"\n[Round {self.state.round}/{self.max_rounds}]")
            
            if self.allow_human:
                human_input = input("Human intervention (enter to skip, 'exit' to terminate): ").strip()
                if human_input.lower() == "exit":
                    print("Simulation manually terminated.")
                    break
                elif human_input:
                    self.state.human_interventions.append(human_input)
                    print(f"Observer injected: {human_input}")

            # 1. Judge opens round
            judge_res = self.judge.generate_response(phase="opening", query=f"Open Round {self.state.round}. Pending human injections: {self.state.human_interventions}")
            self.log_turn("Judge", "opening", judge_res)
            
            if "CASE DISMISSED" in judge_res["content"] or "PROCEED TO TRIAL" in judge_res["content"]:
                print("Simulation terminated by Judge.")
                break
                
            # 2. Prosecutor presents argument
            pros_res = self.prosecutor.generate_response(phase="evidence", query=f"Present your argument for round {self.state.round}.")
            self.log_turn("Prosecutor", "evidence", pros_res)
            
            # 3. Defense rebuts
            def_res = self.defense.generate_response(phase="rebuttal", query=f"Prosecutor presented argument. Please respond and raise objections if needed.", prosecutor_last_argument=pros_res["content"])
            self.log_turn("Defense Attorney", "rebuttal", def_res)
            
            # 4. Judge Rules on objections
            if "[OBJECTION:" in def_res["content"]:
                ruling_res = self.judge.generate_response(phase="ruling", query=f"Defense raised an objection: {def_res['content']}.")
                self.log_turn("Judge", "ruling", ruling_res)
                
            self.state.round += 1

        # Closing phase
        print("\n[Closing Sequence]")
        pros_close = self.prosecutor.generate_response(phase="closing", query="Provide your closing statement.")
        self.log_turn("Prosecutor", "closing", pros_close)

        def_close = self.defense.generate_response(phase="closing", query="Provide your closing statement.", prosecutor_last_argument=pros_close["content"])
        self.log_turn("Defense Attorney", "closing", def_close)
        
        final_rule = self.judge.generate_response(phase="final_ruling", query="Closing arguments finished. Provide your FINAL RULING.")
        self.log_turn("Judge", "final_ruling", final_rule)

        # Export outcome
        export_transcript(self.state, format_type=self.export_format)
        print("Simulation complete.")

    def log_turn(self, speaker: str, phase: str, response: dict):
        content = response.get("content", "")
        objections = []
        if "[OBJECTION:" in content:
            objections.append("Objection flagged.")
            
        turn = Turn(
            round=self.state.round,
            speaker=speaker,
            phase=phase,
            content=content,
            citations=response.get("citations", []),
            objections_raised=objections
        )
        self.state.transcript.append(turn)
        print(f"\n>> {speaker} ({phase}):\n{content}")
