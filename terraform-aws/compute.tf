data "aws_ami" "ubuntu_arm64" {
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd-gp3/ubuntu-noble-24.04-arm64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

resource "aws_key_pair" "greenray_key" {
  key_name   = "greenray-ec2-key"
  public_key = var.ssh_public_key
}

resource "aws_instance" "greenray_ec2" {
  ami                  = data.aws_ami.ubuntu_arm64.id
  instance_type        = var.instance_type
  subnet_id            = aws_subnet.greenray_subnet.id
  key_name             = aws_key_pair.greenray_key.key_name
  vpc_security_group_ids = [aws_security_group.greenray_sg.id]

  root_block_device {
    volume_size           = var.root_volume_size_gb
    volume_type           = "gp3"
    delete_on_termination = true
  }

  user_data = replace(
    file("${path.module}/cloud-init-aws.yaml"),
    "__SSH_ALLOWED_CIDR__",
    var.ssh_allowed_cidr
  )

  tags = {
    Name = "greenray-erp-ec2"
  }
}

resource "aws_eip" "greenray_eip" {
  instance = aws_instance.greenray_ec2.id
  domain   = "vpc"

  tags = {
    Name = "greenray-eip"
  }
}
