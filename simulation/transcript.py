import json
import argparse
from pathlib import Path
import yaml
from simulation.state import SimulationState

def export_transcript(state: SimulationState, format_type: str = "markdown", out_path: str = None):
    # Ensure dir exists
    out_file = Path(out_path) if out_path else Path(f"output/transcript_{state.case_id}.{format_type[:2]}")
    out_file.parent.mkdir(parents=True, exist_ok=True)
    
    turns = [
        {
            "round": t.round,
            "speaker": t.speaker,
            "phase": t.phase,
            "content": t.content,
            "citations": t.citations,
            "objections_raised": t.objections_raised,
            "timestamp": t.timestamp
        }
        for t in state.transcript
    ]

    if format_type.lower() == "json":
        with open(out_file, "w") as f:
            json.dump(turns, f, indent=2)
    else:
        # Default markdown
        lines = [f"# Pre-trial Transcript: {state.case_id}", ""]
        for turn in turns:
            lines.append(f"## Round {turn['round']} - {turn['speaker']} ({turn['phase']})")
            lines.append(f"*{turn['timestamp']}*")
            lines.append(f"\n{turn['content']}\n")
            if turn["citations"]:
                lines.append("**Citations**:")
                for c in turn["citations"]:
                    lines.append(f"- {c}")
            if turn["objections_raised"]:
                lines.append("\n**Objections Raised**:")
                for o in turn["objections_raised"]:
                    lines.append(f"- {o}")
            lines.append("\n---\n")
            
        # Ensure correct extension for markdown fallback
        if format_type.lower() == "pdf":
            print("PDF generation requires external libraries (e.g. reportlab), falling back to Markdown.")
        
        real_out = out_file if str(out_file).endswith(".md") else out_file.with_suffix(".md")
        with open(real_out, "w") as f:
            f.write("\n".join(lines))
        print(f"Exported transcript to {real_out}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export simulation transcript")
    parser.add_argument("--format", type=str, default="markdown", choices=["json", "markdown", "pdf"])
    parser.add_argument("--out", type=str, default="./output/transcript.md")
    args = parser.parse_args()
    
    print(f"Standalone transcript formatter ready. Use save_transcript(state) from simulation.")
