data "oci_identity_availability_domains" "ads" {
  compartment_id = var.tenancy_ocid
}

data "oci_core_images" "ubuntu_arm64" {
  compartment_id           = var.compartment_ocid
  operating_system         = "Canonical Ubuntu"
  operating_system_version = "24.04"
  shape                    = "VM.Standard.A1.Flex"
  sort_by                  = "TIMECREATED"
  sort_order               = "DESC"

  filter {
    name   = "display_name"
    values = ["^Canonical-Ubuntu-24.04-aarch64-.*"]
    regex  = true
  }
}

data "oci_objectstorage_namespace" "ns" {
  compartment_id = var.tenancy_ocid
}

locals {
  availability_domain = var.availability_domain != "" ? var.availability_domain : data.oci_identity_availability_domains.ads.availability_domains[0].name
}

resource "oci_core_vcn" "greenray" {
  compartment_id = var.compartment_ocid
  display_name   = "greenray-erp-vcn"
  dns_label      = "greenrayerp"
  cidr_blocks    = [var.vcn_cidr]
}

resource "oci_core_internet_gateway" "greenray" {
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.greenray.id
  display_name   = "greenray-erp-igw"
  enabled        = true
}

resource "oci_core_route_table" "public" {
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.greenray.id
  display_name   = "greenray-erp-public-routes"

  route_rules {
    network_entity_id = oci_core_internet_gateway.greenray.id
    destination       = "0.0.0.0/0"
    destination_type  = "CIDR_BLOCK"
  }
}

resource "oci_core_security_list" "public" {
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.greenray.id
  display_name   = "greenray-erp-public-security"

  egress_security_rules {
    protocol    = "all"
    destination = "0.0.0.0/0"
  }

  ingress_security_rules {
    protocol = "6"
    source   = var.ssh_allowed_cidr
    tcp_options {
      min = 22
      max = 22
    }
  }

  ingress_security_rules {
    protocol = "6"
    source   = "0.0.0.0/0"
    tcp_options {
      min = 80
      max = 80
    }
  }

  ingress_security_rules {
    protocol = "6"
    source   = "0.0.0.0/0"
    tcp_options {
      min = 443
      max = 443
    }
  }
}

resource "oci_core_subnet" "public" {
  compartment_id             = var.compartment_ocid
  vcn_id                     = oci_core_vcn.greenray.id
  cidr_block                 = var.subnet_cidr
  display_name               = "greenray-erp-public-subnet"
  dns_label                  = "erp"
  route_table_id             = oci_core_route_table.public.id
  security_list_ids          = [oci_core_security_list.public.id]
  prohibit_public_ip_on_vnic = false
}

resource "oci_objectstorage_bucket" "backups" {
  compartment_id = var.compartment_ocid
  namespace      = data.oci_objectstorage_namespace.ns.namespace
  name           = var.backup_bucket_name
  access_type    = "NoPublicAccess"
  storage_tier   = "Standard"
  versioning     = "Disabled"
}

resource "oci_objectstorage_object_lifecycle_policy" "backup_retention" {
  bucket    = oci_objectstorage_bucket.backups.name
  namespace = data.oci_objectstorage_namespace.ns.namespace

  rules {
    action      = "DELETE"
    is_enabled  = true
    name        = "expire-greenray-backups"
    time_amount = var.backup_retention_days
    time_unit   = "DAYS"
    target      = "objects"

    object_name_filter {
      inclusion_prefixes = ["backups/"]
    }
  }
}

resource "oci_core_instance" "erp" {
  availability_domain = local.availability_domain
  compartment_id      = var.compartment_ocid
  display_name        = var.instance_name
  shape               = "VM.Standard.A1.Flex"

  shape_config {
    ocpus         = var.ocpus
    memory_in_gbs = var.memory_gb
  }

  create_vnic_details {
    subnet_id        = oci_core_subnet.public.id
    assign_public_ip = true
    hostname_label   = "greenray-erp"
  }

  source_details {
    source_type             = "image"
    source_id               = data.oci_core_images.ubuntu_arm64.images[0].id
    boot_volume_size_in_gbs = var.boot_volume_gb
  }

  metadata = {
    ssh_authorized_keys = var.ssh_authorized_key
    user_data = base64encode(templatefile("${path.module}/cloud-init.yaml.tftpl", {
      git_repo_url = var.git_repo_url
      git_ref      = var.git_ref
      bucket_name  = oci_objectstorage_bucket.backups.name
      namespace    = data.oci_objectstorage_namespace.ns.namespace
    }))
  }

  instance_options {
    are_legacy_imds_endpoints_disabled = true
  }

  freeform_tags = {
    Application = "GreenRayERP"
    Tier        = "AlwaysFreePilot"
  }
}

resource "oci_identity_dynamic_group" "erp_backup" {
  compartment_id = var.tenancy_ocid
  name           = "greenray-erp-backup-vm"
  description    = "GreenRay ERP VM using Instance Principal for private Object Storage backups"
  matching_rule  = "ALL {instance.id = '${oci_core_instance.erp.id}'}"
}

resource "oci_identity_policy" "erp_backup" {
  compartment_id = var.tenancy_ocid
  name           = "greenray-erp-backup-policy"
  description    = "Least-privilege Object Storage access for the GreenRay ERP backup VM"
  statements = [
    "Allow dynamic-group ${oci_identity_dynamic_group.erp_backup.name} to read buckets in compartment id ${var.compartment_ocid} where target.bucket.name='${oci_objectstorage_bucket.backups.name}'",
    "Allow dynamic-group ${oci_identity_dynamic_group.erp_backup.name} to manage objects in compartment id ${var.compartment_ocid} where target.bucket.name='${oci_objectstorage_bucket.backups.name}'"
  ]
}
