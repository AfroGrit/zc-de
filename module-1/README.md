pbcopy

# Refresh service-account's auth-token for this session

gcloud auth application-default login

# Initialize state file (.tfstate)

terraform init

# Check changes to new infra plan

terraform plan -var="project=afro-de-376122"

# Create new infra

terraform apply -var="project=afro-de-376122"

# Delete infra after your work, to avoid costs on any running services

terraform destroy
