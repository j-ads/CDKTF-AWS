
# Cloud Development Kit for Terraform in Python

CDKTF allows you to use familiar programming languages to define and provision infrastructure. This project deploys infrastructure as a code in AWS for a Kubernetes environment.

![alt text](https://github.com/j-ads/CDKTF-AWS/blob/main/aws_infra.JPG?raw=true)

## Set Up

1.	Install Terraform. Guide: https://developer.hashicorp.com/terraform/downloads
2.	Install CDKTF. Guide: https://developer.hashicorp.com/terraform/tutorials/cdktf/cdktf-install
3.	Optional. In this specific case, we use flag ‘–local’ to create a local database. Login to the Terraform Cloud to store the terraform state remotely.  Guide: https://developer.hashicorp.com/terraform/tutorials/cloud-get-started/cloud-login
4.	Use a valid AWS account and install AWS CLI. Guide: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html
5.	Configure AWS CLI with your valid credentials. Guide: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html
6.	Install Kubernetes CLI. Guide: https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/
7.	Install aws-iam-authenticator. Guide: https://docs.aws.amazon.com/eks/latest/userguide/install-aws-iam-authenticator.html
8.	Make a new directory for the application and create a CDK template with the desired language. For example, following these commands:

```linux
mkdir test
cd test
cdktf init --template="python" --providers="aws@~>4.0" --local
```




## Usage/Examples

To plan and deploy the infrastructure is very similar to Terraform. But first the user has to change a few things:

- The desired AMI for the bastion instance in the main.py file. (For Example: ami-064087b8d355e9051)
- The tier for the bastion instance in the main.py file.(For example: t3.micro)
- The tier for the nodes instances in Kubernetes. (For example: t2.medium)
-Finally, the ssh key path in the development.py or production.py file. (For example: 
```python3
d = os.path.dirname(os.getcwd())
path_to_key = f"{d}/path/to/key")
```
### Planning and Deployment
After the user changes are made. Choose a stack from the main.py file. For example to deploy a development environment in eu-central-1 region in 3 availability zones.

```linux
cdktf plan dev-eu-central1
cdktf deploy dev-eu-central1
```

