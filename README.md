# GitHub Actions + GenAI CI/CD -> AWS ECR

Hackathon-ready reference implementation covering Docker CI/CD, tests, Trivy scanning, GitHub OIDC -> AWS IAM, ECR publishing, AI-generated reports, and AI-assisted failure analysis.

## Repository

- `app/` sample Python HTTP service and tests
- `scripts/` OpenAI report and failure-analysis clients
- `terraform/` ECR + GitHub OIDC provider + IAM role
- `.github/workflows/cicd.yml` main CI/CD pipeline
- `.github/workflows/ai-failure-analysis.yml` manual AI troubleshooting workflow
- `docs/` architecture and demo script

## Setup

### 1. AWS/Terraform

Copy `terraform/terraform.tfvars.example` to `terraform/terraform.tfvars` and set your GitHub org/repository and exact OIDC subject. Run:

```bash
cd terraform
terraform init
terraform plan
terraform apply
```

GitHub's OIDC subject format changed for repositories created after July 15, 2026: new repositories use immutable owner/repository IDs in `sub`. Existing repositories may retain the previous format unless immutable subjects are enabled. Make `oidc_subject` match the actual subject used by your repository.

### 2. GitHub Actions variables/secrets

Repository Settings -> Secrets and variables -> Actions:

Variables:
- `AWS_REGION` = `ap-south-1`
- `ECR_REPOSITORY` = `genai-cicd-demo`
- `AWS_ROLE_TO_ASSUME` = Terraform output `github_actions_role_arn`
- `OPENAI_MODEL` = a model available to your OpenAI API project

Secret:
- `OPENAI_API_KEY`

No AWS access-key/secret-key pair is required for the workflow.

### 3. Local test

```bash
python -m venv .venv
# activate it
pip install -r requirements-dev.txt
pytest -q
```

### 4. Docker

```bash
docker build -t genai-cicd-demo:local .
docker run --rm -p 8080:8080 genai-cicd-demo:local
```

Open `http://localhost:8080/health`.

## Pipeline behavior

PR: tests -> Docker build -> Trivy scan.

Push to main: tests -> build/scan -> OIDC -> ECR push -> AI report -> GitHub Job Summary.

The image uses the full commit SHA as its immutable primary tag and also publishes a short SHA and `latest` on main.

## AI design

The AI receives structured pipeline metadata rather than credentials. It generates:
- build summary
- change summary
- validation summary
- deployment summary
- risks/follow-up
- release notes

The failure-analysis workflow accepts a sanitized log excerpt and returns a classification, evidence, probable cause, diagnostic checks, remediation suggestions, and limitations. Treat the output as advisory and review before production action.

## Demo

See `docs/DEMO.md`.
