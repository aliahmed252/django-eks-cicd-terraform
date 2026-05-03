# جلب بيانات السيكرت من AWS
data "aws_secretsmanager_secret" "argocd_password_meta" {
  name = "argocd/admin-password"
}

data "aws_secretsmanager_secret_version" "argocd_password_value" {
  secret_id = data.aws_secretsmanager_secret.argocd_password_meta.id
}
resource "helm_release" "argocd" {
  name             = "argocd"
  repository       = "https://argoproj.github.io/argo-helm"
  chart            = "argo-cd"
  namespace        = "argocd"
  create_namespace = true

  set {
    name  = "server.service.type"
    value = "LoadBalancer"
  }

  set {
    name  = "configs.secret.argocdServerAdminPassword"
    # بنستخدم jsondecode عشان نحول النص لـ Map ونختار منها الـ password
    value = jsondecode(data.aws_secretsmanager_secret_version.argocd_password_value.secret_string)["password"]
  }

  set {
    name  = "configs.secret.argocdServerAdminPasswordMtime"
    value = timestamp() # مهم عشان يطبق التغيير فوراً
  }

  depends_on = [aws_eks_node_group.managed]
}

