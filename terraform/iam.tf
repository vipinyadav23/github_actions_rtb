resource "aws_iam_openid_connect_provider" "github" {
  url = "https://token.actions.githubusercontent.com"
  client_id_list = ["sts.amazonaws.com"]
  thumbprint_list = ["6938fd4d98bab03faadb97b34396831e3780aea1"]
}

data "aws_iam_policy_document" "github_assume_role" {
  statement {
    effect = "Allow"
    actions = ["sts:AssumeRoleWithWebIdentity"]
    principals { type = "Federated", identifiers = [aws_iam_openid_connect_provider.github.arn] }
    condition { test = "StringEquals", variable = "token.actions.githubusercontent.com:aud", values = ["sts.amazonaws.com"] }
    condition { test = "StringEquals", variable = "token.actions.githubusercontent.com:sub", values = [var.oidc_subject] }
  }
}
resource "aws_iam_role" "github_actions" {
  name = "github-actions-ecr-${var.github_repo}"
  assume_role_policy = data.aws_iam_policy_document.github_assume_role.json
  tags = { Project = "genai-cicd" }
}
data "aws_iam_policy_document" "ecr_push" {
  statement { sid = "EcrAuth", effect = "Allow", actions = ["ecr:GetAuthorizationToken"], resources = ["*"] }
  statement {
    sid = "EcrPushPull", effect = "Allow"
    actions = ["ecr:BatchCheckLayerAvailability", "ecr:BatchGetImage", "ecr:CompleteLayerUpload", "ecr:GetDownloadUrlForLayer", "ecr:InitiateLayerUpload", "ecr:PutImage", "ecr:UploadLayerPart"]
    resources = [aws_ecr_repository.app.arn]
  }
}
resource "aws_iam_role_policy" "ecr_push" {
  name = "ecr-push"
  role = aws_iam_role.github_actions.id
  policy = data.aws_iam_policy_document.ecr_push.json
}
