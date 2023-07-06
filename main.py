#!/usr/bin/env python
from constructs import Construct
from cdktf import App, TerraformStack
from stacks.production import Production
from stacks.development import Development

#("Enter the desired AMI for the bastion instance. (Format Example: ami-064087b8d355e9051):  ")
ami_bastion = "ami-07151644aeb34558a"
#("Enter the tier for the bastion instance.(Format example: t3.micro)")
tier_bastion = "t2.micro"
#("Enter the tier for the nodes instance. 
tier_nodes = "t2.medium"


app = App()
Development(app, "dev-us-east1", region="us-east-1", azs=["us-east-1a", "us-east-1b", "us-east-1c"], 
            bastion_ami = ami_bastion, bastion_tier = tier_bastion, nodes_tier = tier_nodes)
Development(app, "dev-us-east2", region="us-east-2", azs=["us-east-2a", "us-east-2b", "us-east-2c"], 
            bastion_ami = ami_bastion, bastion_tier = tier_bastion, nodes_tier = tier_nodes)
Development(app, "dev-us-west1", region="us-west-1", azs=["us-west-1a", "us-west-1b", "us-west-1c"], 
            bastion_ami = ami_bastion, bastion_tier = tier_bastion, nodes_tier = tier_nodes)
Development(app, "dev-us-west2", region="us-west-2", azs=["us-west-2a", "us-west-2b", "us-west-2c"], 
            bastion_ami = ami_bastion, bastion_tier = tier_bastion, nodes_tier = tier_nodes)
Development(app, "dev-ap-east1", region="ap-east-1", azs=["ap-east-1a", "ap-east-1b", "ap-east-1c"], 
            bastion_ami = ami_bastion, bastion_tier = tier_bastion, nodes_tier = tier_nodes)
Development(app, "dev-ap-south1", region="ap-south-1", azs=["ap-south-1a", "ap-south-1b","ap-south-1c"], 
            bastion_ami = ami_bastion, bastion_tier = tier_bastion, nodes_tier = tier_nodes)
Development(app, "dev-ap-northeast1", region="ap-northeast-1", azs=["ap-northeast-1a", "ap-northeast-1b", "ap-northeast-1c"], 
            bastion_ami = ami_bastion, bastion_tier = tier_bastion, nodes_tier = tier_nodes)
Development(app, "dev-ap-northeast2", region="ap-northeast-2", azs=["ap-northeast-2a", "ap-northeast-2b", "ap-northeast-2c"], 
            bastion_ami = ami_bastion, bastion_tier = tier_bastion, nodes_tier = tier_nodes)
Development(app, "dev-ap-northeast3", region="ap-northeast-3", azs=["ap-northeast-3a", "ap-northeast-3b", "ap-northeast-3c"], 
            bastion_ami = ami_bastion, bastion_tier = tier_bastion, nodes_tier = tier_nodes)
Development(app, "dev-ap-southeast1", region="ap-southeast-1", azs=["ap-southeast-1a", "ap-southeast-1b", "ap-southeast-1c"], 
            bastion_ami = ami_bastion, bastion_tier = tier_bastion, nodes_tier = tier_nodes)
Development(app, "dev-ap-southeast2", region="ap-southeast-2", azs=["ap-southeast-2a", "ap-southeast-2b", "ap-southeast-2c"],
            bastion_ami = ami_bastion, bastion_tier = tier_bastion, nodes_tier = tier_nodes)
Development(app, "dev-ca-central1", region="ca-central-1", azs=["ca-central-1a", "ca-central-1b", "ca-central-1c"], 
            bastion_ami = ami_bastion, bastion_tier = tier_bastion, nodes_tier = tier_nodes)
Development(app, "dev-eu-central1", region="eu-central-1", azs=["eu-central-1a", "eu-central-1b", "eu-central-1c"],
            bastion_ami = ami_bastion, bastion_tier = tier_bastion, nodes_tier = tier_nodes)
Development(app, "dev-eu-west1", region="eu-west-1", azs=["eu-west-1a", "eu-west-1b", "eu-west-1c"],
            bastion_ami = ami_bastion, bastion_tier = tier_bastion, nodes_tier = tier_nodes)
Development(app, "dev-eu-west2", region="eu-west-2", azs=["eu-west-2a", "eu-west-2b", "eu-west-2c"],
            bastion_ami = ami_bastion, bastion_tier = tier_bastion, nodes_tier = tier_nodes)
Development(app, "dev-eu-west3", region="eu-west-3", azs=["eu-west-3a", "eu-west-3b", "eu-west-3c"],
            bastion_ami = ami_bastion, bastion_tier = tier_bastion, nodes_tier = tier_nodes)
Development(app, "dev-eu-south1", region="eu-south-1", azs=["eu-south-1a", "eu-south-1b", "eu-south-1c"],
            bastion_ami = ami_bastion, bastion_tier = tier_bastion, nodes_tier = tier_nodes)
Development(app, "dev-eu-north1", region="eu-north-1", azs=["eu-north-1a", "eu-north-1b", "eu-north-1c"],
            bastion_ami = ami_bastion, bastion_tier = tier_bastion, nodes_tier = tier_nodes)
Development(app, "dev-me-south1", region="me-south-1", azs=["me-south-1a", "me-south-1b", "me-south-1c"],
            bastion_ami = ami_bastion, bastion_tier = tier_bastion, nodes_tier = tier_nodes)
Development(app, "dev-sa-east1", region="sa-east-1", azs=["sa-east-1a", "sa-east-1b", "sa-east-1c"],
            bastion_ami = ami_bastion, bastion_tier = tier_bastion, nodes_tier = tier_nodes)


Production(app, "prod-us-east1", region="us-east-1", azs=["us-east-1a", "us-east-1b", "us-east-1c"], 
            bastion_ami = ami_bastion, bastion_tier = tier_bastion, nodes_tier = tier_nodes)
Production(app, "prod-us-east2", region="us-east-2", azs=["us-east-2a", "us-east-2b", "us-east-2c"], 
            bastion_ami = ami_bastion, bastion_tier = tier_bastion, nodes_tier = tier_nodes)
Production(app, "prod-us-west1", region="us-west-1", azs=["us-west-1a", "us-west-1b", "us-west-1c"], 
            bastion_ami = ami_bastion, bastion_tier = tier_bastion, nodes_tier = tier_nodes)
Production(app, "prod-us-west2", region="us-west-2", azs=["us-west-2a", "us-west-2b", "us-west-2c"], 
            bastion_ami = ami_bastion, bastion_tier = tier_bastion, nodes_tier = tier_nodes)
Production(app, "prod-ap-east1", region="ap-east-1", azs=["ap-east-1a", "ap-east-1b", "ap-east-1c"], 
            bastion_ami = ami_bastion, bastion_tier = tier_bastion, nodes_tier = tier_nodes)
Production(app, "prod-ap-south1", region="ap-south-1", azs=["ap-south-1a", "ap-south-1b","ap-south-1c"], 
            bastion_ami = ami_bastion, bastion_tier = tier_bastion, nodes_tier = tier_nodes)
Production(app, "prod-ap-northeast1", region="ap-northeast-1", azs=["ap-northeast-1a", "ap-northeast-1b", "ap-northeast-1c"], 
            bastion_ami = ami_bastion, bastion_tier = tier_bastion, nodes_tier = tier_nodes)
Production(app, "prod-ap-northeast2", region="ap-northeast-2", azs=["ap-northeast-2a", "ap-northeast-2b", "ap-northeast-2c"], 
            bastion_ami = ami_bastion, bastion_tier = tier_bastion, nodes_tier = tier_nodes)
Production(app, "prod-ap-northeast3", region="ap-northeast-3", azs=["ap-northeast-3a", "ap-northeast-3b", "ap-northeast-3c"], 
            bastion_ami = ami_bastion, bastion_tier = tier_bastion, nodes_tier = tier_nodes)
Production(app, "prod-ap-southeast1", region="ap-southeast-1", azs=["ap-southeast-1a", "ap-southeast-1b", "ap-southeast-1c"], 
            bastion_ami = ami_bastion, bastion_tier = tier_bastion, nodes_tier = tier_nodes)
Production(app, "prod-ap-southeast2", region="ap-southeast-2", azs=["ap-southeast-2a", "ap-southeast-2b", "ap-southeast-2c"],
            bastion_ami = ami_bastion, bastion_tier = tier_bastion, nodes_tier = tier_nodes)
Production(app, "prod-ca-central1", region="ca-central-1", azs=["ca-central-1a", "ca-central-1b", "ca-central-1c"], 
            bastion_ami = ami_bastion, bastion_tier = tier_bastion, nodes_tier = tier_nodes)
Production(app, "prod-eu-central1", region="eu-central-1", azs=["eu-central-1a", "eu-central-1b", "eu-central-1c"],
            bastion_ami = ami_bastion, bastion_tier = tier_bastion, nodes_tier = tier_nodes)
Production(app, "prod-eu-west1", region="eu-west-1", azs=["eu-west-1a", "eu-west-1b", "eu-west-1c"],
            bastion_ami = ami_bastion, bastion_tier = tier_bastion, nodes_tier = tier_nodes)
Production(app, "prod-eu-west2", region="eu-west-2", azs=["eu-west-2a", "eu-west-2b", "eu-west-2c"],
            bastion_ami = ami_bastion, bastion_tier = tier_bastion, nodes_tier = tier_nodes)
Production(app, "prod-eu-west3", region="eu-west-3", azs=["eu-west-3a", "eu-west-3b", "eu-west-3c"],
            bastion_ami = ami_bastion, bastion_tier = tier_bastion, nodes_tier = tier_nodes)
Production(app, "prod-eu-south1", region="eu-south-1", azs=["eu-south-1a", "eu-south-1b", "eu-south-1c"],
            bastion_ami = ami_bastion, bastion_tier = tier_bastion, nodes_tier = tier_nodes)
Production(app, "prod-eu-north1", region="eu-north-1", azs=["eu-north-1a", "eu-north-1b", "eu-north-1c"],
            bastion_ami = ami_bastion, bastion_tier = tier_bastion, nodes_tier = tier_nodes)
Production(app, "prod-me-south1", region="me-south-1", azs=["me-south-1a", "me-south-1b", "me-south-1c"],
            bastion_ami = ami_bastion, bastion_tier = tier_bastion, nodes_tier = tier_nodes)
Production(app, "prod-sa-east1", region="sa-east-1", azs=["sa-east-1a", "sa-east-1b", "sa-east-1c"],
            bastion_ami = ami_bastion, bastion_tier = tier_bastion, nodes_tier = tier_nodes)


app.synth()
