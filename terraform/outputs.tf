output "instance_public_ip" {
  description = "Public IP address of the GreenRay ERP VM"
  value       = oci_core_instance.greenray_vm.public_ip
}

output "sslip_io_domain" {
  description = "Free sslip.io hostname resolving to the VM public IP"
  value       = "erp-${replace(oci_core_instance.greenray_vm.public_ip, ".", "-")}.sslip.io"
}

output "sslip_io_url" {
  description = "Public URL for accessing GreenRay ERP"
  value       = "http://erp-${replace(oci_core_instance.greenray_vm.public_ip, ".", "-")}.sslip.io:8080"
}

output "ssh_command" {
  description = "Command to SSH into the VM"
  value       = "ssh ubuntu@${oci_core_instance.greenray_vm.public_ip}"
}

output "backup_bucket_name" {
  description = "OCI Object Storage Bucket for off-site backups"
  value       = oci_objectstorage_bucket.backup_bucket.name
}
