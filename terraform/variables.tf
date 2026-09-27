variable "aws_region" {
  type    = string
  default = "ap-south-1"
}

variable "project_name" {
  type    = string
  default = "ecommerce-demo"
}

variable "vpc_cidr" {
  type    = string
  default = "10.0.0.0/16"
}

variable "node_instance_type" {
  type    = string
  default = "t3.medium"
}

variable "db_username" {
  type    = string
  default = "app"
}

variable "db_password" {
  description = "Enter this only when Terraform asks."
  type        = string
  sensitive   = true
}