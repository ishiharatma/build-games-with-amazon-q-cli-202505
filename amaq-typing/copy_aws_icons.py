import os
import shutil
from PIL import Image

# AWS Services list (same as in main.py)
aws_services = [
    "S3", "EC2", "Lambda", "DynamoDB", "CloudFront", 
    "RDS", "SQS", "SNS", "CloudWatch", "IAM",
    "Route53", "ECS", "EKS", "Fargate", "API Gateway",
    "Cognito", "Amplify", "AppSync", "Athena", "Aurora",
    "Batch", "Bedrock", "CloudFormation", "CodeBuild", "CodePipeline",
    "Comprehend", "Connect", "DocumentDB", "Elastic Beanstalk", "ElastiCache",
    "EventBridge", "Glue", "Kinesis", "Lex", "Lightsail",
    "Macie", "MemoryDB", "Neptune", "Polly", "Rekognition",
    "SageMaker", "SecretsManager", "Step Functions", "Textract", "VPC"
]

# Mapping of service names to their icon paths in the AWS Architecture Icons package
service_to_icon_path = {
    "S3": "aws-icons/Architecture-Service-Icons_02072025/Arch_Storage/64/Arch_Amazon-Simple-Storage-Service_64.png",
    "EC2": "aws-icons/Architecture-Service-Icons_02072025/Arch_Compute/64/Arch_Amazon-EC2_64.png",
    "Lambda": "aws-icons/Architecture-Service-Icons_02072025/Arch_Compute/64/Arch_AWS-Lambda_64.png",
    "DynamoDB": "aws-icons/Architecture-Service-Icons_02072025/Arch_Database/64/Arch_Amazon-DynamoDB_64.png",
    "CloudFront": "aws-icons/Architecture-Service-Icons_02072025/Arch_Networking-Content-Delivery/64/Arch_Amazon-CloudFront_64.png",
    "RDS": "aws-icons/Architecture-Service-Icons_02072025/Arch_Database/64/Arch_Amazon-RDS_64.png",
    "SQS": "aws-icons/Architecture-Service-Icons_02072025/Arch_App-Integration/64/Arch_Amazon-Simple-Queue-Service_64.png",
    "SNS": "aws-icons/Architecture-Service-Icons_02072025/Arch_App-Integration/64/Arch_Amazon-Simple-Notification-Service_64.png",
    "CloudWatch": "aws-icons/Architecture-Service-Icons_02072025/Arch_Management-Governance/64/Arch_Amazon-CloudWatch_64.png",
    "IAM": "aws-icons/Architecture-Service-Icons_02072025/Arch_Security-Identity-Compliance/64/Arch_AWS-Identity-and-Access-Management_64.png",
    "Route53": "aws-icons/Architecture-Service-Icons_02072025/Arch_Networking-Content-Delivery/64/Arch_Amazon-Route-53_64.png",
    "ECS": "aws-icons/Architecture-Service-Icons_02072025/Arch_Containers/64/Arch_Amazon-Elastic-Container-Service_64.png",
    "EKS": "aws-icons/Architecture-Service-Icons_02072025/Arch_Containers/64/Arch_Amazon-Elastic-Kubernetes-Service_64.png",
    "Fargate": "aws-icons/Architecture-Service-Icons_02072025/Arch_Containers/64/Arch_AWS-Fargate_64.png",
    "API Gateway": "aws-icons/Architecture-Service-Icons_02072025/Arch_Networking-Content-Delivery/64/Arch_Amazon-API-Gateway_64.png",
    "Cognito": "aws-icons/Architecture-Service-Icons_02072025/Arch_Security-Identity-Compliance/64/Arch_Amazon-Cognito_64.png",
    "Amplify": "aws-icons/Architecture-Service-Icons_02072025/Arch_Front-End-Web-Mobile/64/Arch_AWS-Amplify_64.png",
    "AppSync": "aws-icons/Architecture-Service-Icons_02072025/Arch_App-Integration/64/Arch_AWS-AppSync_64.png",
    "Athena": "aws-icons/Architecture-Service-Icons_02072025/Arch_Analytics/64/Arch_Amazon-Athena_64.png",
    "Aurora": "aws-icons/Architecture-Service-Icons_02072025/Arch_Database/64/Arch_Amazon-Aurora_64.png",
    "Batch": "aws-icons/Architecture-Service-Icons_02072025/Arch_Compute/64/Arch_AWS-Batch_64.png",
    "Bedrock": "aws-icons/Architecture-Service-Icons_02072025/Arch_Artificial-Intelligence/64/Arch_Amazon-Bedrock_64.png",
    "CloudFormation": "aws-icons/Architecture-Service-Icons_02072025/Arch_Management-Governance/64/Arch_AWS-CloudFormation_64.png",
    "CodeBuild": "aws-icons/Architecture-Service-Icons_02072025/Arch_Developer-Tools/64/Arch_AWS-CodeBuild_64.png",
    "CodePipeline": "aws-icons/Architecture-Service-Icons_02072025/Arch_Developer-Tools/64/Arch_AWS-CodePipeline_64.png",
    "Comprehend": "aws-icons/Architecture-Service-Icons_02072025/Arch_Artificial-Intelligence/64/Arch_Amazon-Comprehend_64.png",
    "Connect": "aws-icons/Architecture-Service-Icons_02072025/Arch_Business-Applications/64/Arch_Amazon-Connect_64.png",
    "DocumentDB": "aws-icons/Architecture-Service-Icons_02072025/Arch_Database/64/Arch_Amazon-DocumentDB_64.png",
    "Elastic Beanstalk": "aws-icons/Architecture-Service-Icons_02072025/Arch_Compute/64/Arch_AWS-Elastic-Beanstalk_64.png",
    "ElastiCache": "aws-icons/Architecture-Service-Icons_02072025/Arch_Database/64/Arch_Amazon-ElastiCache_64.png",
    "EventBridge": "aws-icons/Architecture-Service-Icons_02072025/Arch_App-Integration/64/Arch_Amazon-EventBridge_64.png",
    "Glue": "aws-icons/Architecture-Service-Icons_02072025/Arch_Analytics/64/Arch_AWS-Glue_64.png",
    "Kinesis": "aws-icons/Architecture-Service-Icons_02072025/Arch_Analytics/64/Arch_Amazon-Kinesis_64.png",
    "Lex": "aws-icons/Architecture-Service-Icons_02072025/Arch_Artificial-Intelligence/64/Arch_Amazon-Lex_64.png",
    "Lightsail": "aws-icons/Architecture-Service-Icons_02072025/Arch_Compute/64/Arch_Amazon-Lightsail_64.png",
    "Macie": "aws-icons/Architecture-Service-Icons_02072025/Arch_Security-Identity-Compliance/64/Arch_Amazon-Macie_64.png",
    "MemoryDB": "aws-icons/Architecture-Service-Icons_02072025/Arch_Database/64/Arch_Amazon-MemoryDB_64.png",
    "Neptune": "aws-icons/Architecture-Service-Icons_02072025/Arch_Database/64/Arch_Amazon-Neptune_64.png",
    "Polly": "aws-icons/Architecture-Service-Icons_02072025/Arch_Artificial-Intelligence/64/Arch_Amazon-Polly_64.png",
    "Rekognition": "aws-icons/Architecture-Service-Icons_02072025/Arch_Artificial-Intelligence/64/Arch_Amazon-Rekognition_64.png",
    "SageMaker": "aws-icons/Architecture-Service-Icons_02072025/Arch_Analytics/64/Arch_Amazon-SageMaker_64.png",
    "SecretsManager": "aws-icons/Architecture-Service-Icons_02072025/Arch_Security-Identity-Compliance/64/Arch_AWS-Secrets-Manager_64.png",
    "Step Functions": "aws-icons/Architecture-Service-Icons_02072025/Arch_App-Integration/64/Arch_AWS-Step-Functions_64.png",
    "Textract": "aws-icons/Architecture-Service-Icons_02072025/Arch_Artificial-Intelligence/64/Arch_Amazon-Textract_64.png",
    "VPC": "aws-icons/Architecture-Service-Icons_02072025/Arch_Networking-Content-Delivery/64/Arch_Amazon-Virtual-Private-Cloud_64.png"
}

def copy_and_resize_icons():
    # Create images directory if it doesn't exist
    os.makedirs("images", exist_ok=True)
    
    # Copy and resize each icon
    for service in aws_services:
        if service in service_to_icon_path:
            source_path = service_to_icon_path[service]
            target_path = os.path.join("images", f"{service.lower().replace(' ', '_')}.png")
            
            if os.path.exists(source_path):
                # Copy and resize to 200x200
                img = Image.open(source_path)
                img = img.resize((200, 200), Image.LANCZOS)
                img.save(target_path)
                print(f"Copied and resized icon for {service} to {target_path}")
            else:
                print(f"Source icon not found for {service}: {source_path}")
        else:
            print(f"No icon mapping defined for {service}")

if __name__ == "__main__":
    copy_and_resize_icons()
