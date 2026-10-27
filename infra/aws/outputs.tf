output "api_url" {
  description = "URL publique de l'API (via l'ALB)."
  value       = "http://${aws_lb.api.dns_name}"
}

output "ecr_repository_url" {
  description = "URI du dépôt ECR pour pousser l'image de l'API."
  value       = aws_ecr_repository.api.repository_url
}

output "db_endpoint" {
  description = "Point de terminaison RDS PostgreSQL."
  value       = aws_db_instance.postgres.address
}
