# Build and Deployment

## Overview

The repository uses two manually triggered GitHub Actions workflows:

1. **Infrastructure CI/CD** provisions AWS infrastructure through Terraform.
2. **Application CI/CD** validates the containerized application, publishes images to Amazon ECR, and deploys Kubernetes resources to Amazon EKS.

Both workflows authenticate to AWS with GitHub OpenID Connect (OIDC). They do not require long-lived AWS access keys in GitHub.

## Infrastructure CI/CD

Workflow file: `.github/workflows/infra-cd.yml`

```text
workflow_dispatch
  → GitHub OIDC authentication
  → terraform fmt -check
  → terraform init
  → terraform validate
  → terraform plan -out=tfplan
  → terraform apply tfplan
```

`terraform plan -out=tfplan` writes the exact reviewed plan to a file. The later `terraform apply tfplan` applies that saved plan instead of generating a different plan at apply time.

Terraform provisions:

- VPC, internet gateway, public and private subnets, routes, and security groups
- EKS cluster and managed node group
- ECR repositories for Frontend, Product, and Order
- RDS PostgreSQL and the DB subnet group
- IAM roles, policy attachments, and EKS access configuration

The Terraform backend uses an S3 bucket with `use_lockfile = true`.

## Application CI/CD

Workflow file: `.github/workflows/application-cd.yml`

```text
workflow_dispatch
  → Docker Compose build and smoke checks
  → GitHub OIDC authentication
  → ECR login
  → build Frontend, Product, and Order images
  → tag images with the short Git commit SHA
  → push images to ECR
  → connect kubectl to EKS
  → create or update Kubernetes Secret
  → apply manifests and HPA
  → set image versions
  → wait for deployment rollouts
```

### Local smoke checks in CI

The application workflow starts the Compose stack and checks:

```bash
curl -f http://localhost:5001/health
curl -f http://localhost:5003/health
curl -f http://localhost:5500/
```

The workflow stops the Compose environment with `docker compose down -v` in an `always()` step, so a failed check does not leave test containers running on the GitHub runner.

### Image publishing

Images use the short Git SHA as a tag:

```text
<ECR registry>/ecommerce-demo-frontend:<short SHA>
<ECR registry>/ecommerce-demo-product:<short SHA>
<ECR registry>/ecommerce-demo-order:<short SHA>
```

Each ECR repository enables `scan_on_push = true`.

### Kubernetes deployment

The workflow applies the namespace, ConfigMap, Deployments, Services, HPA, and Ingress. It creates or updates the `ecommerce-secrets` Secret from GitHub Actions Secrets, then uses `kubectl set image` to update the three Deployments and waits for rollout completion.

## Code quality scanning

SonarQube is used for code-quality and security-oriented scanning. Present it as a separate scan unless the workflow explicitly runs it and blocks deployment through a Quality Gate. Do not claim that SonarQube gates deployment unless that configuration exists.

## Recommended next CI improvement

The current application workflow performs Compose health smoke checks. Add the repository test suite before Compose in a future change:

```bash
python -m pytest -s tests
```

Then configure a SonarQube Quality Gate if the project requires quality findings to block deployment.


