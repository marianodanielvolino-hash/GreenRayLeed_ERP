resource "oci_objectstorage_bucket" "backup_bucket" {
  compartment_id = var.compartment_ocid
  name           = "greenray-erp-backups"
  namespace      = data.oci_objectstorage_namespace.ns.namespace
  access_type    = "NoPublicAccess"
  storage_tier   = "Standard"

  auto_tiering = "Disabled"
}

data "oci_objectstorage_namespace" "ns" {
  compartment_id = var.compartment_ocid
}
