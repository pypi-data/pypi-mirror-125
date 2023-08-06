output "control_plane_private_ips" {
  value = tolist(aws_instance.control_planes.*.private_ip)
}

output "worker_node_private_ips" {
  value = tolist(aws_instance.worker_nodes.*.private_ip)
}

output "control_plane_public_ips" {
  value = tolist(aws_instance.control_planes.*.public_ip)
}

output "worker_node_public_ips" {
  value = tolist(aws_instance.worker_nodes.*.public_ip)
}

output "control_plane_lb_dns" {
  value = module.control_plane_load_balancer.dns_name
}

output "ami" {
  value = aws_instance.control_planes.0.ami
}

output "ami_name" {
  value = data.aws_ami.specified_ami.name
}

output "ami_description" {
  value = data.aws_ami.specified_ami.description
}

output "ami_location" {
  value = data.aws_ami.specified_ami.image_location
}

output "instance_type" {
  value = aws_instance.control_planes.0.instance_type
}

output "ports" {
  value = tolist(var.ports)
}
