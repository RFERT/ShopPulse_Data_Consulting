variable "aws_region" {
  description = "Région AWS de déploiement."
  type        = string
  default     = "eu-west-3" # Paris
}

variable "project" {
  description = "Préfixe de nommage des ressources."
  type        = string
  default     = "shoppulse"
}

variable "api_image" {
  description = "Image conteneur de l'API (URI ECR, tag inclus)."
  type        = string
}

variable "api_cpu" {
  description = "vCPU de la tâche Fargate (256 = 0,25 vCPU)."
  type        = number
  default     = 256
}

variable "api_memory" {
  description = "Mémoire de la tâche Fargate (Mo)."
  type        = number
  default     = 512
}

variable "desired_count" {
  description = "Nombre de tâches API."
  type        = number
  default     = 1
}

variable "db_username" {
  description = "Utilisateur maître RDS."
  type        = string
  default     = "shoppulse"
}

variable "db_password" {
  description = "Mot de passe maître RDS (injecté via TF_VAR, jamais versionné)."
  type        = string
  sensitive   = true
}

variable "db_instance_class" {
  description = "Classe d'instance RDS."
  type        = string
  default     = "db.t4g.micro"
}
