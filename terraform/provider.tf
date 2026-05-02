# provider.tf

terraform {
  required_version = ">= 1.5.0" # إصدار تيرفورم مستقر

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0" # استخدام الإصدار 5 المستقر بدلاً من 6
    }
    helm = {
      source  = "hashicorp/helm"
      version = "~> 2.12.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.24.0"
    }
    tls = {
      source  = "hashicorp/tls"
      version = "~> 4.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# جلب بيانات الـ Cluster بعد إنشائه للتعامل مع الـ Auth
data "aws_eks_cluster" "cluster" {
  name = aws_eks_cluster.main.name
}

data "aws_eks_cluster_auth" "cluster" {
  name = aws_eks_cluster.main.name
}

# إعداد الـ Helm ليتمكن من تنصيب ArgoCD و Prometheus
provider "helm" {
  kubernetes {
    host                   = data.aws_eks_cluster.cluster.endpoint
    cluster_ca_certificate = base64decode(data.aws_eks_cluster.cluster.certificate_authority[0].data)
    token                  = data.aws_eks_cluster_auth.cluster.token
  }
}

# إعداد الـ Kubernetes للتعامل مع الـ Resources مباشرة
provider "kubernetes" {
  host                   = data.aws_eks_cluster.cluster.endpoint
  cluster_ca_certificate = base64decode(data.aws_eks_cluster.cluster.certificate_authority[0].data)
  token                  = data.aws_eks_cluster_auth.cluster.token
}