import json
import os
import sys
from pathlib import Path
from openai import OpenAI

SYSTEM_PROMPT = """You are an AI assistant embedded in a DevOps CI/CD pipeline.
Convert structured pipeline metadata into a concise engineering report.
Do not invent test results, security findings, deployments, or code changes.
Clearly distinguish observed facts from recommendations. Never expose secrets.
Keep the report suitable for a GitHub Actions Job Summary. Return Markdown.
Use headings: Build Summary, Changes, Validation, Deployment, Risks / Follow-up, Release Notes."""

def main():
    if len(sys.argv) != 2:
        print("Usage: python scripts/generate_ai_report.py pipeline.json", file=sys.stderr); return 2
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        print("OPENAI_API_KEY is not configured", file=sys.stderr); return 2
    payload = json.loads(Path(sys.argv[1]).read_text())
    client = OpenAI(api_key=key)
    response = client.responses.create(
        model=os.environ.get("OPENAI_MODEL", "gpt-6-luna"),
        instructions=SYSTEM_PROMPT,
        input=json.dumps(payload, indent=2),
    )
    report = response.output_text.strip()
    if not report:
        print("OpenAI returned an empty report", file=sys.stderr); return 1
    print(report); return 0

if __name__ == "__main__":
    raise SystemExit(main())
