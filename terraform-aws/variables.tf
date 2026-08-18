variable "aws_region" {
  type        = string
  description = "AWS Region (e.g. us-east-1, sa-east-1)"
  default     = "us-east-1"
}

variable "aws_access_key" {
  type        = string
  description = "AWS Access Key ID"
  sensitive   = true
}

variable "aws_secret_key" {
  type        = string
  description = "AWS Secret Access Key"
  sensitive   = true
}

variable "instance_type" {
  type        = string
  description = "AWS EC2 Graviton ARM64 Instance Type (t4g.small or t4g.medium)"
  default     = "t4g.medium"
}

variable "root_volume_size_gb" {
  type        = number
  description = "Size of the root EBS volume in GB"
  default     = 50
}

variable "ssh_public_key" {
  type        = string
  description = "Public SSH key for accessing the EC2 instance"
}

variable "ssh_allowed_cidr" {
  type        = string
  description = "CIDR block allowed for SSH access"
}

variable "admin_email" {
  type        = string
  description = "Admin email for ACME / Let's Encrypt certificates"
  default     = "ops@greenrayleed.com"
}
