output "instance_id" {
  value = oci_core_instance.erp.id
}

output "public_ip" {
  value = oci_core_instance.erp.public_ip
}

output "public_hostname" {
  value = "erp-${replace(oci_core_instance.erp.public_ip, ".", "-")}.sslip.io"
}

output "https_url" {
  value = "https://erp-${replace(oci_core_instance.erp.public_ip, ".", "-")}.sslip.io"
}

output "ssh_command" {
  value = "ssh ubuntu@${oci_core_instance.erp.public_ip}"
}

output "backup_bucket" {
  value = oci_objectstorage_bucket.backups.name
}

output "object_storage_namespace" {
  value = data.oci_objectstorage_namespace.ns.namespace
}
