### Running terraform and GCP services

```console
# Refresh service-account's auth-token for this session
gcloud auth application-default login

# Initialize state file (.tfstate)
terraform init

# Check changes to new infra plan
terraform plan -var="project=<your-gcp-project-id>"

# Create new infra
terraform apply -var="project=<your-gcp-project-id>"

# Referesh config files after making changes
terraform apply -refresh-only -auto-approve

# Delete infra after your work, to avoid costs on any running services
terraform destroy
```
