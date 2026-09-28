import json
import os
import sys
from pathlib import Path
from openai import OpenAI

SYSTEM_PROMPT = """You are an AI SRE assistant analyzing a failed CI/CD pipeline.
Use only the supplied evidence.
Return Markdown with headings: Failure Classification, Evidence, Probable Root Cause,
Recommended Checks, Suggested Remediation, Confidence / Limitations.
Never claim certainty when evidence is insufficient. Do not invent logs or infrastructure state.
Do not execute commands. Never request or expose credentials. Recommendations require human review."""

def main():
    if len(sys.argv) != 2:
        print("Usage: python scripts/analyze_failure.py failure.json", file=sys.stderr); return 2
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        print("OPENAI_API_KEY is not configured", file=sys.stderr); return 2
    payload = json.loads(Path(sys.argv[1]).read_text())
    response = OpenAI(api_key=key).responses.create(
        model=os.environ.get("OPENAI_MODEL", "gpt-5-mini"),
        instructions=SYSTEM_PROMPT,
        input=json.dumps(payload, indent=2),
    )
    print(response.output_text.strip()); return 0

if __name__ == "__main__":
    raise SystemExit(main())
