data "aws_ami" "specified_ami" {
  most_recent = true
  owners = [
    "amazon",
    "aws-marketplace",
    "099720109477", # Ubuntu
    "309956199498", # RHEL
    "136693071363", # Debian
  ]

  filter {
    name   = "image-id"
    values = [var.ami]
  }

  filter {
    name   = "architecture"
    values = ["x86_64"]
  }

  filter {
    name   = "state"
    values = ["available"]
  }
}

resource "aws_instance" "control_planes" {
  count         = var.control_plane_count
  ami           = data.aws_ami.specified_ami.image_id
  instance_type = var.instance_type
  key_name      = aws_key_pair.kubernetes_cluster.id
  vpc_security_group_ids = [
    module.internal_all_sg.security_group_id,
    module.global_ssh_sg.security_group_id
  ]
  subnet_id = element(module.vpc.cluster_subnet_ids, count.index % length(module.vpc.cluster_subnet_ids))

  tags = {
    Name = "${var.cluster_name}-control-plane${count.index}"
  }
}

resource "aws_instance" "worker_nodes" {
  count                  = var.worker_node_count
  ami                    = data.aws_ami.specified_ami.image_id
  instance_type          = var.instance_type
  key_name               = aws_key_pair.kubernetes_cluster.id
  vpc_security_group_ids = local.worker_node_security_group_ids
  subnet_id              = element(module.vpc.cluster_subnet_ids, count.index % length(module.vpc.cluster_subnet_ids))

  tags = {
    Name = "${var.cluster_name}-worker-node${count.index}"
  }
}

resource "aws_key_pair" "kubernetes_cluster" {
  key_name   = "${var.cluster_name}-${var.ssh_public_key_name}"
  public_key = file(pathexpand(var.ssh_public_key))
}
