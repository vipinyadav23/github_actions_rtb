output "ecr_repository_url" { value = aws_ecr_repository.app.repository_url }
output "github_actions_role_arn" { value = aws_iam_role.github_actions.arn }
output "oidc_provider_arn" { value = aws_iam_openid_connect_provider.github.arn }
