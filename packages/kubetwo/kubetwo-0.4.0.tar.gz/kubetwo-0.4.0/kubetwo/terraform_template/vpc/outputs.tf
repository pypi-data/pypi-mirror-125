output "vpc_id" {
  value = aws_vpc.kubernetes_cluster.id
}

output "vpc_cidr_block" {
  value = aws_vpc.kubernetes_cluster.cidr_block
}

output "cluster_subnet_ids" {
  value = aws_subnet.cluster_subnets.*.id
}
