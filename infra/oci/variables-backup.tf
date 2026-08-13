variable "backup_bucket_name" {
  type    = string
  default = "greenray-erp-backups"
}

variable "backup_retention_days" {
  type    = number
  default = 7
}
