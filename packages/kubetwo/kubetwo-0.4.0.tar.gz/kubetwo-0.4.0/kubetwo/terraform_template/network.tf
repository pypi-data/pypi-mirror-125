data "aws_availability_zones" "available" {
  state = "available"
}

module "vpc" {
  source              = "./vpc"
  cluster_name        = var.cluster_name
  availability_zones  = slice(data.aws_availability_zones.available.names, 0, length(var.cluster_cidr_blocks))
  vpc_cidr_block      = var.vpc_cidr_block
  cluster_cidr_blocks = var.cluster_cidr_blocks
}

module "control_plane_load_balancer" {
  source              = "./load_balancer"
  name                = "${var.cluster_name}-control-plane"
  subnet_ids          = module.vpc.cluster_subnet_ids
  security_group_ids  = [module.global_kubeapi_sg.security_group_id]
  instance_ids        = aws_instance.control_planes.*.id
  port                = 6443
  health_check_target = "HTTPS:6443/readyz"
}
