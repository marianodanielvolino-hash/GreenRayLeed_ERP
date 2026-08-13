# OCI ARM64 pilot

Run Terraform only in the tenancy home region. Copy `terraform.tfvars.example`, set OCI access values and restrict `ssh_allowed_cidr` to your public IP `/32`.

Before apply: `terraform fmt -check`, `terraform validate`, `terraform plan`.

The VM does not receive OCI API keys. Off-site backups use Instance Principal IAM. Application passwords belong only in the VM `.env`, never in Git or cloud-init.

After the VM exists, create `.env` with the sslip.io hostname from `terraform output sslip_io_domain`, strong random DB/Admin passwords and ACME email, then run `bash scripts/deploy-oci.sh` from `/opt/greenray/GreenRayLeed_ERP`.
