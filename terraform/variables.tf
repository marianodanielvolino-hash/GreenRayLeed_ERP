variable "tenancy_ocid" {
  type        = string
  description = "OCID of your OCI tenancy"
}

variable "user_ocid" {
  type        = string
  description = "OCID of the user running Terraform"
}

variable "compartment_ocid" {
  type        = string
  description = "OCID of the compartment where resources will be created"
}

variable "fingerprint" {
  type        = string
  description = "Fingerprint of the OCI API key"
}

variable "private_key_path" {
  type        = string
  description = "Path to the private key file used for OCI API authentication"
}

variable "region" {
  type        = string
  description = "OCI region (e.g. us-ashburn-1, sa-saopaulo-1)"
  default     = "us-ashburn-1"
}

variable "ssh_public_key" {
  type        = string
  description = "Public SSH key text for accessing the VM"
}

variable "instance_ocpus" {
  type        = number
  description = "Number of OCPUs for VM.Standard.A1.Flex (Always Free max 4)"
  default     = 2
}

variable "instance_memory_gb" {
  type        = number
  description = "Memory in GB for VM.Standard.A1.Flex (Always Free max 24)"
  default     = 12
}

variable "boot_volume_size_gb" {
  type        = number
  description = "Boot volume size in GB (Always Free max 200)"
  default     = 100
}

variable "admin_email" {
  type        = string
  description = "Email address for ACME / Let's Encrypt TLS certificates"
  default     = "admin@greenrayleed.com"
}
