resource "aws_elb" "kubernetes_elb" {
  name            = var.name
  subnets         = var.subnet_ids
  security_groups = var.security_group_ids

  listener {
    instance_port     = var.port
    instance_protocol = "tcp"
    lb_port           = var.port
    lb_protocol       = "tcp"
  }

  health_check {
    healthy_threshold   = 2
    unhealthy_threshold = 2
    timeout             = 3
    target              = var.health_check_target
    interval            = 30
  }

  cross_zone_load_balancing   = true
  idle_timeout                = 400
  connection_draining         = true
  connection_draining_timeout = 400

  tags = {
    Name = var.name
  }
}

resource "aws_elb_attachment" "attach_control_plane" {
  count    = length(var.instance_ids)
  elb      = aws_elb.kubernetes_elb.id
  instance = element(var.instance_ids, count.index)
}
