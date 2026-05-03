# جلب بيانات السيكرت بتاع جرافانا
data "aws_secretsmanager_secret" "grafana_password_meta" {
  name = "grafana/admin-password"
}

data "aws_secretsmanager_secret_version" "grafana_password_value" {
  secret_id = data.aws_secretsmanager_secret.grafana_password_meta.id
}

resource "helm_release" "prometheus_stack" {
  name             = "prometheus-stack"
  repository       = "https://prometheus-community.github.io/helm-charts"
  chart            = "kube-prometheus-stack"
  namespace        = "monitoring"
  create_namespace = true
  timeout          = 600 # بنزود الوقت عشان الـ Charts دي تقيلة

  set {
      name  = "adminPassword"
      value = jsondecode(data.aws_secretsmanager_secret_version.grafana_password_value.secret_string)["password"]
  }

  set {
    name  = "grafana.service.type"
    value = "LoadBalancer" # عشان يجيلك لينك تفتح منه الـ Dashboard
  }

  # التأكد إن النودز قايمة الأول عشان الـ Pods تلاقي مكان تسكن فيه
  depends_on = [aws_eks_node_group.managed]
}


