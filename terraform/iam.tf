resource "oci_identity_dynamic_group" "greenray_backup" {
  compartment_id = var.tenancy_ocid
  name           = "greenray-erp-backup-vm"
  description    = "GreenRay ERP VM backup identity"
  matching_rule  = "ALL {instance.id = '${oci_core_instance.greenray_vm.id}'}"
}

resource "oci_identity_policy" "greenray_backup" {
  compartment_id = var.tenancy_ocid
  name           = "greenray-erp-backup-policy"
  description    = "Bucket-scoped backup permissions for the ERP VM"
  statements = [
    "Allow dynamic-group ${oci_identity_dynamic_group.greenray_backup.name} to use object-family in compartment id ${var.compartment_ocid} where all {target.bucket.name='${oci_objectstorage_bucket.backup_bucket.name}'}",
    "Allow dynamic-group ${oci_identity_dynamic_group.greenray_backup.name} to manage objects in compartment id ${var.compartment_ocid} where all {target.bucket.name='${oci_objectstorage_bucket.backup_bucket.name}'}"
  ]
}
