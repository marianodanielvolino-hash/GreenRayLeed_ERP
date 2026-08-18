output "greenray_public_ip" {
  value       = aws_eip.greenray_eip.public_ip
  description = "Public IP address of GreenRay ERP EC2 Instance"
}

output "greenray_site_name" {
  value       = "erp-${replace(aws_eip.greenray_eip.public_ip, ".", "-")}.sslip.io"
  description = "Suggested sslip.io SITE_NAME for SSL/HTTPS certificate"
}

output "ssh_command" {
  value       = "ssh -i C:/Users/Mariano Volino/.ssh/greenray_oci_id_ed25519 ubuntu@${aws_eip.greenray_eip.public_ip}"
  description = "SSH connection string"
}
