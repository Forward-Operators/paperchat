# Ingester VM
GCP provides Deep Learning VM so you can use GPU for your ingester.

As mentioned in main README, Kaggle is providing arXiv dataset via GCS bucket.

Deep Learning VMs have built-in support for `gcsfuse` so we can easily mount them.

You can use terraform scripts in this directory to automatically set up everything, but you need to make sure you have [GPU limit](https://console.cloud.google.com/iam-admin/quotas?metric=compute.googleapis.com/gpus_all_regions) increased (it's 0 by default and takes around 2 business days to get approved).

And because access to gcs is allowed only for authenticated users, you need to use Terraform Cloud to pass service account credentials so the bucket can be auto-mounted. [Here's](https://support.hashicorp.com/hc/en-us/articles/4406586874387-How-to-set-up-Google-Cloud-GCP-credentials-in-Terraform-Cloud) how to do this
