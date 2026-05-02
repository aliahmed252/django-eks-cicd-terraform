# variables.tf

variable "aws_region" {
  description = "The AWS region to deploy resources in."
  type        = string
  default     = "us-east-1" # Default to a common region; change as needed.
}

variable "cluster_name" {
  description = "The name for the EKS cluster."
  type        = string
  default     = "malerator-eks-cluster"
}

variable "vpc_cidr" {
  description = "The CIDR block for the VPC."
  type        = string
  default     = "10.0.0.0/16"
}

variable "private_subnet_cidrs" {
  description = "List of CIDR blocks for private subnets."
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "public_subnet_cidrs" {
  description = "List of CIDR blocks for public subnets."
  type        = list(string)
  default     = ["10.0.101.0/24", "10.0.102.0/24"]
}

variable "availability_zones" {
  description = "List of availability zones to use for subnets. Ensure these exist in your chosen AWS region."
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b"] # Must match your chosen aws_region
}

variable "eks_node_group_instance_types" {
  description = "Instance types for the EKS managed node groups."
  type        = list(string)
  default     = ["m7i-flex.large"] # A reasonable default for production
}

variable "eks_node_group_desired_size" {
  description = "Desired number of nodes in the EKS managed node group."
  type        = number
  default     = 2
}

variable "eks_node_group_max_size" {
  description = "Maximum number of nodes in the EKS managed node group."
  type        = number
  default     = 3
}

variable "eks_node_group_min_size" {
  description = "Minimum number of nodes in the EKS managed node group."
  type        = number
  default     = 1
}

