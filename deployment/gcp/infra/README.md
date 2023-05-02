## Pre-requisites to run:

A GCP Project with a service account that has the following roles:
- Artifact Registry Administrator
- Cloud Run Admin
- Editor
- Project IAM Admin
- Service Usage Admin
## How to run?
- Download the Service Account Key in the .json-format, and place it in this directory.
- Configure your infrastructure in variables.tf
- Run `cp .env.template .env` and set `GOOGLE_APPLICATION_CREDENTIALS` to the path to your service account file.
- Run `terraform init`
- Run `terraform validate`
- Run `source .env && terraform apply`
- This will set up the required infrastructure and then return an Error, since the Docker image to be deployed through Cloud Run does not exist yet.
- Push your Docker image with the name `docker_image` to the repository `repository`, in line with your configuration in `variables.tf`
- Run `source .env && terraform apply` again.