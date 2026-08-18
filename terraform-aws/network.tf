resource "aws_vpc" "greenray_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "greenray-vpc"
  }
}

resource "aws_internet_gateway" "greenray_igw" {
  vpc_id = aws_vpc.greenray_vpc.id

  tags = {
    Name = "greenray-igw"
  }
}

resource "aws_subnet" "greenray_subnet" {
  vpc_id                  = aws_vpc.greenray_vpc.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true

  tags = {
    Name = "greenray-public-subnet"
  }
}

resource "aws_route_table" "greenray_rt" {
  vpc_id = aws_vpc.greenray_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.greenray_igw.id
  }

  tags = {
    Name = "greenray-route-table"
  }
}

resource "aws_route_table_association" "greenray_rta" {
  subnet_id      = aws_subnet.greenray_subnet.id
  route_table_id = aws_route_table.greenray_rt.id
}

resource "aws_security_group" "greenray_sg" {
  name        = "greenray-security-group"
  description = "Security group for GreenRay ERP on AWS"
  vpc_id      = aws_vpc.greenray_vpc.id

  # SSH (Port 22 restricted to ssh_allowed_cidr)
  ingress {
    description = "SSH from allowed CIDR"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.ssh_allowed_cidr]
  }

  # HTTP (Port 80)
  ingress {
    description = "HTTP traffic"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # HTTPS (Port 443)
  ingress {
    description = "HTTPS traffic"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Egress: allow all outbound
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "greenray-sg"
  }
}
