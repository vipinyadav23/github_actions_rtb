# Demo Walkthrough

1. Show repository structure and architecture.
2. Show Terraform-created ECR and IAM/OIDC role.
3. Make a harmless application change and push to main.
4. Show tests, Docker build, Trivy scan, OIDC authentication, and ECR push.
5. Open the GitHub Actions Summary and show the AI-generated report.
6. Open ECR and show immutable SHA tagging.
7. Run AI Failure Analysis with a sanitized failure excerpt.
8. Explain the security story: no static AWS credentials, least-privilege ECR policy, image scanning, immutable tags, and human-reviewed AI recommendations.
