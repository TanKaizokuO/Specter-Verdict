import argparse
import yaml
from simulation.orchestrator import Simulator

def main():
    parser = argparse.ArgumentParser(description="AI Courtroom Pre-Trial Simulation")
    parser.add_argument("--config", type=str, default="config/settings.yaml", help="Path to config file")
    args = parser.parse_args()
    
    try:
        with open(args.config, "r") as f:
            config = yaml.safe_load(f)
            case_id = config.get("case", {}).get("case_id", "CASE-2026-DEFAULT")
    except Exception as e:
        print(f"Warning: Could not read config {args.config}. Using defaults. Error: {e}")
        case_id = "CASE-2026-DEFAULT"

    print(f"Starting simulation orchestrator for case {case_id}...")
    sim = Simulator(case_id=case_id)
    sim.run()

if __name__ == "__main__":
    main()
