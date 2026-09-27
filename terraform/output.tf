output "cluster_name" {
  value = aws_eks_cluster.main.name
}

output "aws_region" {
  value = var.aws_region
}

output "rds_endpoint" {
  value = aws_db_instance.postgres.address
}

output "frontend_ecr_url" {
  value = aws_ecr_repository.frontend.repository_url
}

output "product_ecr_url" {
  value = aws_ecr_repository.product.repository_url
}

output "order_ecr_url" {
  value = aws_ecr_repository.order.repository_url
}