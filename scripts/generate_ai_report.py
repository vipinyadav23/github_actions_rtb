import json
import os
import sys

from google import genai


SYSTEM_PROMPT = """
You are an AI assistant integrated into a CI/CD pipeline.

Generate a concise but useful Markdown deployment report.

Use exactly these sections:

## Build Summary
## Changes
## Validation
## Deployment
## Risks / Follow-up
## Release Notes

Rules:
- Use only the information supplied in the pipeline JSON.
- Do not invent test results.
- Do not invent deployment results.
- Do not expose secrets, API keys, credentials, or tokens.
- If information is missing, explicitly say it is unavailable.
- Keep the report suitable for a software release/change record.
"""


def main():
    if len(sys.argv) != 2:
        raise SystemExit(
            "Usage: python scripts/generate_ai_report.py pipeline.json"
        )

    input_file = sys.argv[1]

    with open(input_file, "r", encoding="utf-8") as f:
        payload = json.load(f)

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise SystemExit("GEMINI_API_KEY is not configured")

    model = os.environ.get(
        "GEMINI_MODEL",
        "gemini-2.5-flash-lite",
    )

    client = genai.Client(api_key=api_key)

    prompt = f"""
{SYSTEM_PROMPT}

Pipeline data:

{json.dumps(payload, indent=2)}
"""

    response = client.models.generate_content(
        model=model,
        contents=prompt,
    )

    if not response.text:
        raise SystemExit("Gemini returned an empty response")

    print(response.text)


if __name__ == "__main__":
    main()
