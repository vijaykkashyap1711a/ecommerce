# Security and Observability

## Configuration and access controls

| Control | Current implementation |
| --- | --- |
| AWS authentication from GitHub | GitHub Actions uses OIDC to assume an AWS IAM role. Long-lived AWS access keys are not stored in GitHub. |
| Deployment secrets | `TF_VAR_db_password` and `API_TOKEN` are GitHub Actions Secrets. |
| Kubernetes runtime secrets | The deployment workflow creates or updates `ecommerce-secrets`. Product and Order load database URLs and API token values from this Secret. |
| Database isolation | RDS uses private DB subnets, encrypted storage, `publicly_accessible = false`, and a security group that permits PostgreSQL only from the VPC CIDR. |
| Network exposure | Kubernetes Services remain internal. The ALB Ingress is the intended public HTTP entry point. |
| Container privilege | The Dockerfile creates `appuser` with UID `10001` and runs the application as that non-root user. |
| Image scanning | Every ECR repository enables scan on push. |
| Cluster access | EKS access uses IAM access entries and cluster access policy association. |
| Code scanning | SonarQube is used for code-quality and security-oriented findings. |

## Important scope note

The API bearer token is a demonstration mechanism, not complete production authentication or authorization. A production service would use an identity provider, token rotation, authorization policy, and audit controls.

## CloudWatch observability

The `amazon-cloudwatch-observability` EKS add-on with EKS Pod Identity collects:

- Application container logs
- Cluster, node, Pod, and container metrics
- CPU and memory signals
- Pod status and restart information

Cloudwatch Agent : Monitoring
Fluent bit : Logging

Expected log groups include:

```text
/aws/containerinsights/ecommerce-demo/application
/aws/containerinsights/ecommerce-demo/dataplane
/aws/containerinsights/ecommerce-demo/host
/aws/containerinsights/ecommerce-demo/performance
```

Verify the CloudWatch components:

```bash
kubectl get pods -n amazon-cloudwatch

aws eks describe-addon \
  --cluster-name ecommerce-demo \
  --addon-name amazon-cloudwatch-observability \
  --region ap-south-1 \
  --query "addon.status" \
  --output text
```

```

 
