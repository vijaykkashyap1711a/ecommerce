# Limitations and Production Roadmap

## Known limitations

The exercise had a four-hour timebox. The current platform is a working end-to-end demo; the following are the main production improvements.

| Area | Current state | Production improvement |
| --- | --- | --- |
| Terraform backend | The S3 state bucket was created manually. | Create it through a small Terraform bootstrap module with versioning and locking. |
| Manual AWS configuration | The CloudWatch Observability add-on was enabled manually. | Manage the add-on and its configuration through Terraform. |
| IAM configuration | Some IAM user ARNs are hard-coded. | Use variables or Terraform data sources so the configuration is reusable. |
| Tests in CI | Unit and integration tests pass locally but are not yet a required CI step before image build and push. | Run `python -m pytest -s tests` in the pull-request and application pipelines. |
| Scan findings | SonarQube and ECR scans report findings that still need remediation. | Fix SonarQube issues and upgrade or replace vulnerable image dependencies. |
| Worker node capacity | HPA can scale Product and Order Pods, but worker nodes do not scale automatically. | Add Cluster Autoscaler or Karpenter. |
| Worker-node and secret security | Worker nodes are in public subnets and secrets are managed through Kubernetes and GitHub Actions. | Move nodes to private subnets and use AWS Secrets Manager with External Secrets. |
| RDS availability | RDS is single-AZ with demo-level backup and deletion settings. | Enable Multi-AZ, longer backups, deletion protection, and recovery testing. |

## Prioritized roadmap

### 1. Make infrastructure fully(100 per) repeatable

- Create a Terraform bootstrap module for the S3 state backend.
- Enable state versioning, locking, plan review, and drift detection.
- Move the CloudWatch add-on configuration into Terraform.
- Remove hard-coded IAM ARNs by using variables or data sources.

### 2. Strengthen CI and scanning

- Run unit and integration tests on pull requests and before building or pushing images.
- Fix SonarQube findings and configure a Quality Gate when ready to enforce it.
- Review ECR scan findings and update vulnerable base-image packages.

### 3. Improve security and availability

- Move EKS worker nodes to private subnets.
- Replace manually managed Kubernetes secrets with AWS Secrets Manager and External Secrets.
- Add node autoscaling with Cluster Autoscaler or Karpenter.
- Enable Multi-AZ RDS, backup retention, deletion protection, and recovery testing.

### 4. Improve monitoring and operations

- Add CloudWatch alarms and EKS control-plane logs.
- Add Prometheus, Grafana, and Alertmanager for deeper application metrics and alerts.
- Add Pod Disruption Budgets and topology-spread rules for better workload resilience.

### 5. Mature delivery and cost controls

- Use development, staging, and production environments with pull-request review and approval before production.
- Document rollback and upgrade procedures .
- Add AWS Budgets, billing alerts, ECR lifecycle policies, and regular rightsizing reviews.



> The project is a complete working demo. Due to the time constraint, I could not fully complete a few production enhancements, so I have listed them as prioritized roadmap items. The next focus would be to implement these improvements step by step.

