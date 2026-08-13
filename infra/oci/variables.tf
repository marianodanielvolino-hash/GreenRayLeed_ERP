variable "tenancy_ocid" { type = string }
variable "compartment_ocid" { type = string }
variable "region" { type = string }
variable "availability_domain" { type = string default = "" }
variable "instance_name" { type = string default = "greenray-erp" }
variable "acme_email" { type = string }
variable "ssh_allowed_cidr" { type = string }

variable "ocpus" {
  type = number
  default = 2
  validation {
    condition = var.ocpus > 0 && var.ocpus <= 2
    error_message = "ocpus must be > 0 and <= 2 for this Always Free profile."
  }
}

variable "memory_gb" {
  type = number
  default = 12
  validation {
    condition = var.memory_gb >= 1 && var.memory_gb <= 12
    error_message = "memory_gb must be between 1 and 12 for this Always Free profile."
  }
}

variable "boot_volume_gb" {
  type = number
  default = 100
  validation {
    condition = var.boot_volume_gb >= 47 && var.boot_volume_gb <= 200
    error_message = "boot_volume_gb must be between 47 and 200."
  }
}

variable "vcn_cidr" { type = string default = "10.20.0.0/16" }
variable "subnet_cidr" { type = string default = "10.20.1.0/24" }
variable "backup_bucket_name" { type = string default = "greenray-erp-backups" }
variable "backup_retention_days" { type = number default = 7 }
variable "git_repo_url" { type = string default = "https://github.com/marianodanielvolino-hash/GreenRayLeed_ERP.git" }
variable "git_ref" { type = string default = "main" }
