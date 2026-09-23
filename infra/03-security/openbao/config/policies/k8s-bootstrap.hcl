# Short-lived hy-home.k8s bootstrap token: reads the Argo CD platform entry
# before External Secrets is running. Issued through the k8s-bootstrap token
# role on every cluster rebuild.
path "secret/data/platform/argocd" {
  capabilities = ["read"]
}
