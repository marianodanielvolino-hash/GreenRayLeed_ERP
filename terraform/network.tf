resource "oci_core_vcn" "greenray_vcn" {
  cidr_block     = "10.0.0.0/16"
  compartment_id = var.compartment_ocid
  display_name   = "greenray-vcn"
  dns_label      = "greenrayvcn"
}

resource "oci_core_internet_gateway" "greenray_ig" {
  compartment_id = var.compartment_ocid
  display_name   = "greenray-internet-gateway"
  vcn_id         = oci_core_vcn.greenray_vcn.id
  enabled        = true
}

resource "oci_core_route_table" "greenray_rt" {
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.greenray_vcn.id
  display_name   = "greenray-route-table"

  route_rules {
    destination       = "0.0.0.0/0"
    destination_type  = "CIDR_BLOCK"
    network_entity_id = oci_core_internet_gateway.greenray_ig.id
  }
}

resource "oci_core_security_list" "greenray_sl" {
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.greenray_vcn.id
  display_name   = "greenray-security-list"

  # Egress: allow all outbound
  egress_security_rules {
    destination = "0.0.0.0/0"
    protocol    = "all"
  }

  # Ingress: SSH (22)
  ingress_security_rules {
    protocol = "6" # TCP
    source   = var.ssh_allowed_cidr
    tcp_options {
      min = 22
      max = 22
    }
  }

  # Ingress: HTTP (80)
  ingress_security_rules {
    protocol = "6" # TCP
    source   = "0.0.0.0/0"
    tcp_options {
      min = 80
      max = 80
    }
  }

  # Ingress: HTTPS (443)
  ingress_security_rules {
    protocol = "6" # TCP
    source   = "0.0.0.0/0"
    tcp_options {
      min = 443
      max = 443
    }
  }
}

resource "oci_core_subnet" "greenray_subnet" {
  cidr_block        = "10.0.1.0/24"
  compartment_id    = var.compartment_ocid
  vcn_id            = oci_core_vcn.greenray_vcn.id
  route_table_id    = oci_core_route_table.greenray_rt.id
  security_list_ids = [oci_core_security_list.greenray_sl.id]
  display_name      = "greenray-public-subnet"
  dns_label         = "greenraysubnet"
}
