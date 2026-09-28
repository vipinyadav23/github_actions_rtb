variable "aws_region" { type = string, default = "ap-south-1" }
variable "ecr_repository_name" { type = string, default = "genai-cicd-demo" }
variable "github_org" { type = string }
variable "github_repo" { type = string }
variable "oidc_subject" { type = string }
