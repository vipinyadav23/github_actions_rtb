# Architecture

GitHub push -> GitHub Actions -> tests -> Docker build -> Trivy -> GitHub OIDC -> AWS IAM role -> Amazon ECR.

Pipeline metadata -> OpenAI API -> AI build/release/deployment report -> GitHub Job Summary.

A separate manual workflow sends sanitized failure evidence to the AI for classification and troubleshooting suggestions. The AI is advisory; it does not autonomously mutate production infrastructure.
