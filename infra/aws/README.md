# Déploiement AWS — ECS Fargate + RDS (bonus)

Infrastructure as code pour servir l'API ShopPulse sur AWS. **Non appliquée ici**
(aucun credential dans le dépôt) : c'est une cible **reproductible et chiffrée**.

Voir l'architecture et l'estimation de coût dans
[`docs/deploiement_cloud.md`](../../docs/deploiement_cloud.md).

## Composants (`main.tf`)

| Ressource | Rôle |
|-----------|------|
| ECR | Registre de l'image Docker de l'API |
| ECS Fargate (cluster + service + task) | Exécution serverless de l'API derrière un ALB |
| ALB | Point d'entrée HTTP public, health-check `/health` |
| RDS PostgreSQL | Base consolidée managée |
| CloudWatch Logs | Centralisation des logs applicatifs |
| Security groups | ALB → API (8000), API → DB (5432) |

## Déploiement

```bash
# 1. Construire et pousser l'image vers ECR
aws ecr get-login-password --region eu-west-3 \
  | docker login --username AWS --password-stdin <ACCOUNT_ID>.dkr.ecr.eu-west-3.amazonaws.com
docker build -t shoppulse-api -f infra/Dockerfile .
docker tag shoppulse-api:latest <ACCOUNT_ID>.dkr.ecr.eu-west-3.amazonaws.com/shoppulse-api:latest
docker push <ACCOUNT_ID>.dkr.ecr.eu-west-3.amazonaws.com/shoppulse-api:latest

# 2. Provisionner l'infrastructure
cd infra/aws
terraform init
terraform apply \
  -var="api_image=<ACCOUNT_ID>.dkr.ecr.eu-west-3.amazonaws.com/shoppulse-api:latest" \
  -var="db_password=$DB_PASSWORD"

# 3. Récupérer l'URL publique
terraform output api_url
```

## Sécurité

- Le mot de passe RDS est passé par variable sensible (`TF_VAR_db_password`), jamais versionné.
- En production, le stocker dans **AWS Secrets Manager** (voir `secrets` dans
  `ecs-task-definition.json`) et retirer l'accès public de l'ALB au profit d'HTTPS (ACM).
- `terraform.tfstate` contient des valeurs sensibles : utiliser un **backend S3 chiffré**
  plutôt qu'un état local.
