resource "helm_release" "prometheus_stack" {
  name             = "prometheus-stack"
  repository       = "https://prometheus-community.github.io/helm-charts"
  chart            = "kube-prometheus-stack"
  namespace        = "monitoring"
  create_namespace = true
  timeout          = 600 # بنزود الوقت عشان الـ Charts دي تقيلة

  # الإعدادات الافتراضية لـ Grafana
  set {
    name  = "grafana.adminPassword"
    value = "admin" # يفضل تغيرها أو تستخدم Secret
  }

  set {
    name  = "grafana.service.type"
    value = "LoadBalancer" # عشان يجيلك لينك تفتح منه الـ Dashboard
  }

  # التأكد إن النودز قايمة الأول عشان الـ Pods تلاقي مكان تسكن فيه
  depends_on = [aws_eks_node_group.managed]
}
