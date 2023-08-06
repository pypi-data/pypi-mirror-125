resource "aws_vpc" "kubernetes_cluster" {
  cidr_block           = var.vpc_cidr_block
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = var.cluster_name
  }
}

resource "aws_subnet" "cluster_subnets" {
  vpc_id                  = aws_vpc.kubernetes_cluster.id
  count                   = length(var.cluster_cidr_blocks)
  cidr_block              = element(var.cluster_cidr_blocks, count.index)
  map_public_ip_on_launch = true
  availability_zone       = element(var.availability_zones, count.index)

  tags = {
    Name = "${var.cluster_name}_cluster${count.index}"
  }
}

resource "aws_internet_gateway" "internet_gateway" {
  vpc_id = aws_vpc.kubernetes_cluster.id

  tags = {
    Name = "${var.cluster_name}_ig"
  }
}

resource "aws_eip" "nat_gateway_ips" {
  count      = length(var.cluster_cidr_blocks)
  vpc        = true
  depends_on = [aws_internet_gateway.internet_gateway]
}

resource "aws_nat_gateway" "nat_gateways" {
  count         = length(var.cluster_cidr_blocks)
  allocation_id = element(aws_eip.nat_gateway_ips.*.id, count.index)
  subnet_id     = element(aws_subnet.cluster_subnets.*.id, count.index)
  depends_on    = [aws_internet_gateway.internet_gateway]

  tags = {
    Name = "${var.cluster_name}_nat"
  }
}

resource "aws_route_table" "cluster_tables" {
  count  = length(var.cluster_cidr_blocks)
  vpc_id = aws_vpc.kubernetes_cluster.id

  tags = {
    Name = "${var.cluster_name}_cluster_route_table${count.index}"
  }
}

resource "aws_route" "cluster_routes" {
  count                  = length(var.cluster_cidr_blocks)
  route_table_id         = element(aws_route_table.cluster_tables.*.id, count.index)
  gateway_id             = aws_internet_gateway.internet_gateway.id
  destination_cidr_block = "0.0.0.0/0"
}

resource "aws_route_table_association" "cluster_associations" {
  count          = length(var.cluster_cidr_blocks)
  subnet_id      = element(aws_subnet.cluster_subnets.*.id, count.index)
  route_table_id = element(aws_route_table.cluster_tables.*.id, count.index)
}
