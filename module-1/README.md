## Module 1:

- Docker and Postgres
- GCP amd Terraform

### Running terraform and GCP services

```console
Refresh service-account's auth-token for this session
gcloud auth application-default login

# Initialize state file (.tfstate)
terraform init

# Check changes to new infra plan
terraform plan -var="XXX"

# Create new infra
terraform apply -var="project=XXX"

# Delete infra after your work, to avoid costs on any running services
terraform destroy
```

### Utilities

```console
# copy to clipboard terminal content
terraform apply -var="project=afro-de-376122" | pbcopy

# add a file to the last commit in Git?
git add the_left_out_file
git commit --amend --no-edit
```
