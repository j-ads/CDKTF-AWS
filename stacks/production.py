#!/usr/bin/env python
from constructs import Construct
from cdktf import TerraformStack, TerraformOutput, TerraformVariable, Token, Fn
from cdktf_cdktf_provider_aws.provider import AwsProvider
from imports.vpc import Vpc
import cdktf_cdktf_provider_aws.eks_cluster as EksCluster_
import cdktf_cdktf_provider_aws.eks_node_group as EksNodes_
import cdktf_cdktf_provider_aws.iam_role as IamRole_
import cdktf_cdktf_provider_aws.iam_role_policy as IamPolicy_
import cdktf_cdktf_provider_aws.iam_role_policy_attachment as RoleAttachment_
import cdktf_cdktf_provider_aws.security_group as SecurityGroup_
from cdktf_cdktf_provider_aws.instance import Instance
import cdktf_cdktf_provider_aws.db_subnet_group as DbSubnetGroup_
import cdktf_cdktf_provider_aws.db_instance as DbInstance_
import cdktf_cdktf_provider_aws.key_pair as KeyPair_
import json
import os

d = os.path.dirname(os.getcwd())
path_to_key = f"{d}/path/to/key"
#CLASS FOR VPC

class Production(TerraformStack):
    def __init__(self, scope: Construct, id: str, region: str, azs:list, bastion_ami: str, bastion_tier: str, nodes_tier: str):
        super().__init__(scope, id)

#PROVIDER and REGION
        AwsProvider(self, "AWS", region=region)



#Declare Instance Variables
        image_id = TerraformVariable(self, "image_id",
                                     type="string",
                                     default=bastion_ami,
                                     description="AMI for instances"
                                     )
        
        instance_type = TerraformVariable(self, "instance_type",
                                          type="string",
                                          default=bastion_tier,
                                          description="Instance type for instances"
                                          )
        
        instance_type_nodes = TerraformVariable(self, "instance_type_nodes",
                                          type="string",
                                          default=nodes_tier,
                                          description="Instance type for instances"
                                          )        

#VPC DECLARATION
        private_subnets_c = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
        public_subnets_c = ["10.0.101.0/24","10.0.102.0/24", "10.0.103.0/24"]     

        dev_vpc = Vpc(self, "devops",
                      cidr="10.0.0.0/16",
                      azs=azs,
                      public_subnets=public_subnets_c,
                      private_subnets=private_subnets_c,
                      enable_dns_support=True,
                      enable_dns_hostnames=True,
                      instance_tenancy="default",
                      enable_nat_gateway=True
                      )
        
  
        public_key_file = path_to_key
        key_file = os.open(public_key_file, os.O_RDONLY)
        n = 4096
        # using os.read() method
        key = os.read(key_file, n)
        decode_key = key.decode('utf-8').strip()
        connect_key = str(decode_key)
        os.close(key_file)

        connection_key = KeyPair_.KeyPair(self, "key-ssh",
                         key_name= f"connection-key-{region}",
                         public_key = connect_key
                         )
        
#alb security group        
        alb_security_group = SecurityGroup_.SecurityGroup(self, "alb_security_group",
                                                          name="alb_sg",
                                                          description="Security group for alb with HTTP ports open from anywhere",
                                                          vpc_id=Token().as_string(dev_vpc.vpc_id_output),
                                                          ingress=[SecurityGroup_.SecurityGroupIngress(
                                                              from_port=80, to_port=80, protocol="tcp", cidr_blocks=["0.0.0.0/0"])],
                                                          egress=[SecurityGroup_.SecurityGroupEgress(
                                                              from_port=0, to_port=0, protocol="-1", cidr_blocks=["0.0.0.0/0"])]
                                                          )                                 
#Bastion

        bastion_security_group = SecurityGroup_.SecurityGroup(self, "bastion_security_group",
                                                                 name= f"bastion_sg-{region}",
                                                                 description="Security group for SSH ports open from bastion",
                                                                 vpc_id=Token().as_string(dev_vpc.vpc_id_output),
                                                                 ingress=[SecurityGroup_.SecurityGroupIngress(
                                                                     from_port=22, to_port=22, protocol="tcp", cidr_blocks=["0.0.0.0/0"])],
                                                                 egress=[SecurityGroup_.SecurityGroupEgress(
                                                                     from_port=0, to_port=0, protocol="-1", cidr_blocks=["0.0.0.0/0"])]
                                                                 )        

#Bastion Instance        
        bastion = Instance(self, "bastion",
                              ami=image_id.default,
                              instance_type=instance_type.default,
                              vpc_security_group_ids=[
                                  bastion_security_group.id],
                              subnet_id=Fn.element(Token().as_list(
                                  dev_vpc.public_subnets_output), 0),
                              key_name = connection_key.key_name                                 
                              ) 


#EKS CLUSTER AND NODES DECLARATION

        eks_nodes_sg = SecurityGroup_.SecurityGroup(self, "eks_nodes_sg",
            name = f"eks_nodes_security_group_{region}",
            description = "Security Group for EKS Nodes",
            vpc_id = Token().as_string(dev_vpc.vpc_id_output),
            ingress=[SecurityGroup_.SecurityGroupIngress(
                from_port=0, to_port=0, protocol="tcp", cidr_blocks=["0.0.0.0/0"])],    
            egress=[SecurityGroup_.SecurityGroupEgress(
                from_port=0, to_port=0, protocol="-1", cidr_blocks=["0.0.0.0/0"])]
                )



##IAM ROLES FOR CLUSTER
        cluster_role = {    "Version": "2012-10-17",
            "Statement": [
             {
                "Effect": "Allow",
                "Principal": {
                    "Service": "eks.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
                }
            ]
        }

#Create Iam Role
        aws_eks_role = IamRole_.IamRole(self, "eks_role",
                                name = f"eks_role-{region}",
                                assume_role_policy = json.dumps(cluster_role)
        )

#Attach Policies to Role
        eks_cluster_policy = RoleAttachment_.IamRolePolicyAttachment(self, "eks_cluster_policy",
            policy_arn="arn:aws:iam::aws:policy/AmazonEKSClusterPolicy",
            role=aws_eks_role.name
            )
        
        eks_service_policy = RoleAttachment_.IamRolePolicyAttachment(self, "eks_service_policy",
            policy_arn="arn:aws:iam::aws:policy/AmazonEKSServicePolicy",
            role=aws_eks_role.name
            )

        eks_vpc_policy = RoleAttachment_.IamRolePolicyAttachment(self, "eks_vpc_resource",
            policy_arn="arn:aws:iam::aws:policy/AmazonEKSVPCResourceController",
            role=aws_eks_role.name
            )
        
#Node Group Policies

        node_role = {    "Version": "2012-10-17",
            "Statement": [
                {
                "Effect": "Allow",
                "Principal": {
                    "Service": "ec2.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
                }
            ]
        }

#Create Iam Role
        aws_node_role = IamRole_.IamRole(self, "node_role",
                                name = f"node_role_{region}",
                                assume_role_policy = json.dumps(node_role)
        )

#Attach Policies to Role
        worker_node_policy = RoleAttachment_.IamRolePolicyAttachment(self, "worker_node_policy",
            policy_arn="arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy",
            role=aws_node_role.name
            )

        cni_node_policy = RoleAttachment_.IamRolePolicyAttachment(self, "CNI_node_policy",
            policy_arn="arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy",
            role=aws_node_role.name
            )

        ec2_node_policy = RoleAttachment_.IamRolePolicyAttachment(self, "node_ec2_policy",
            policy_arn="arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly",
            role=aws_node_role.name
            )


#EKS CLUSTER

        eks_cluster = EksCluster_.EksCluster(self, "eks_cluster",
                                             name = f"EKSCluster-{region}",
                                             role_arn = aws_eks_role.arn,
                                             version = "1.27",
                                             vpc_config = EksCluster_.EksClusterVpcConfig(
                                                security_group_ids=[eks_nodes_sg.id],
                                                endpoint_private_access=True,
                                                endpoint_public_access=True,
                                                public_access_cidrs= ["0.0.0.0/0"],
                                                subnet_ids=[Fn.element(Token().as_list(dev_vpc.public_subnets_output), 0), 
                                                            Fn.element(Token().as_list(dev_vpc.public_subnets_output), 1),
                                                            Fn.element(Token().as_list(dev_vpc.public_subnets_output), 2)
                                                        ]
                                                ),
                                             depends_on = [eks_cluster_policy, eks_service_policy, eks_vpc_policy],
                                             enabled_cluster_log_types = ["api", "audit", "authenticator", "controllerManager", "scheduler"]
                                             )
        
#NODE GROUP

        eks_node_group_public = EksNodes_.EksNodeGroup(self, "eks_node_group",
                                                    cluster_name = eks_cluster.name,
                                                    node_group_name = f"public_group_{region}",
                                                    node_role_arn = aws_node_role.arn,
                                                    subnet_ids = [Fn.element(Token().as_list(dev_vpc.public_subnets_output), 0), 
                                                            Fn.element(Token().as_list(dev_vpc.public_subnets_output), 1),
                                                            Fn.element(Token().as_list(dev_vpc.public_subnets_output), 2)],
                                                    instance_types = [instance_type_nodes.default],
                                                    scaling_config = EksNodes_.EksNodeGroupScalingConfig(
                                                        desired_size = 2,
                                                        max_size = 4,
                                                        min_size = 1
                                                        ),
                                                    remote_access = EksNodes_.EksNodeGroupRemoteAccess(
                                                        source_security_group_ids = [eks_nodes_sg.id, bastion_security_group.id, alb_security_group.id],
                                                        ec2_ssh_key = connection_key.key_name
                                                    ),
                                                    depends_on = [worker_node_policy, cni_node_policy, ec2_node_policy]
                                                    )
        
#DATABASE

        db_security_group = SecurityGroup_.SecurityGroup(self, "db_security_group",
                                                                 name= f"db_server_sg_{region}",
                                                                 description="Security group for DB",
                                                                 vpc_id=Token().as_string(dev_vpc.vpc_id_output),
                                                                 ingress=[SecurityGroup_.SecurityGroupIngress(
                                                                     from_port=5432, to_port=5432, protocol="tcp", cidr_blocks=["0.0.0.0/0"])],    
                                                                 egress=[SecurityGroup_.SecurityGroupEgress(
                                                                     from_port=0, to_port=0, protocol="-1", cidr_blocks=["0.0.0.0/0"])]
                                                                 )
        
#Database config
        db_subnet_group = DbSubnetGroup_.DbSubnetGroup(self, 'db-subnet-group',
                                        name=f"db-subnet-group-{region}",
                                        subnet_ids=[Fn.element(Token().as_list(dev_vpc.private_subnets_output), 0),
                                                    Fn.element(Token().as_list(dev_vpc.private_subnets_output), 1), 
                                                    Fn.element(Token().as_list(dev_vpc.private_subnets_output), 2)]
                                        )    

        db_instance = DbInstance_.DbInstance(self, 'rds-instance',
                                    #storage
                                    allocated_storage = 10,
                                    max_allocated_storage = 20,
                                    storage_type = "gp2",
                                    #engine
                                    engine='postgres',
                                    engine_version='15.2',
                                    instance_class='db.t3.micro',
                                    #configs
                                    db_name=f'db',
                                    username='adminpostgres',
                                    password='notasafepw',
                                    multi_az = True,
                                    vpc_security_group_ids = [db_security_group.id],
                                    #others    
                                    skip_final_snapshot = True,
                                    publicly_accessible = False,    
                                    db_subnet_group_name=db_subnet_group.name,
                                    storage_encrypted = True,
                                    backup_retention_period = 14,
                                    backup_window = "03:00-04:00",
                                    delete_automated_backups = True,
                                    auto_minor_version_upgrade = True,
                                    maintenance_window = "Sat:00:00-Sat:02:00"

                                    )

        db_replicas = DbInstance_.DbInstance(self, "rds-instance-replicas",
                                             count = 2,
                                             engine='postgres',
                                             engine_version='15.2',
                                             name = "production-db",
                                             replicate_source_db="db",
                                             skip_final_snapshot=True,
                                             instance_class="db.t3.micro",
                                             storage_type="gp2",
                                             allocated_storage = 10,
                                             max_allocated_storage = 20,
                                             publicly_accessible=False,
                                             vpc_security_group_ids=[db_security_group.id],
                                             storage_encrypted=True,
                                             iam_database_authentication_enabled=False
                                        )