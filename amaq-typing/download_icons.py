import os
import requests
import time
from PIL import Image
from io import BytesIO

# Create images directory if it doesn't exist
os.makedirs("images", exist_ok=True)

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

# Base URL for AWS Architecture Icons
BASE_URL = "https://d1.awsstatic.com/icons/q1-2023/"

# Service name to filename mapping (adjust as needed)
service_to_filename = {
    "S3": "Storage/Amazon-Simple-Storage-Service_S3_light-bg.png",
    "EC2": "Compute/Amazon-EC2_light-bg.png",
    "Lambda": "Compute/AWS-Lambda_light-bg.png",
    "DynamoDB": "Database/Amazon-DynamoDB_light-bg.png",
    "CloudFront": "Networking-Content-Delivery/Amazon-CloudFront_light-bg.png",
    "RDS": "Database/Amazon-RDS_light-bg.png",
    "SQS": "Application-Integration/Amazon-SQS_light-bg.png",
    "SNS": "Application-Integration/Amazon-SNS_light-bg.png",
    "CloudWatch": "Management-Governance/Amazon-CloudWatch_light-bg.png",
    "IAM": "Security-Identity-Compliance/AWS-Identity-and-Access-Management_IAM_light-bg.png",
    "Route53": "Networking-Content-Delivery/Amazon-Route-53_light-bg.png",
    "ECS": "Compute/Amazon-Elastic-Container-Service_light-bg.png",
    "EKS": "Compute/Amazon-Elastic-Kubernetes-Service_light-bg.png",
    "Fargate": "Compute/AWS-Fargate_light-bg.png",
    "API Gateway": "Application-Integration/Amazon-API-Gateway_light-bg.png",
    "Cognito": "Security-Identity-Compliance/Amazon-Cognito_light-bg.png",
    "Amplify": "Front-End-Web-Mobile/AWS-Amplify_light-bg.png",
    "AppSync": "Application-Integration/AWS-AppSync_light-bg.png",
    "Athena": "Analytics/Amazon-Athena_light-bg.png",
    "Aurora": "Database/Amazon-Aurora_light-bg.png",
    "Batch": "Compute/AWS-Batch_light-bg.png",
    "Bedrock": "Machine-Learning/Amazon-Bedrock_light-bg.png",
    "CloudFormation": "Management-Governance/AWS-CloudFormation_light-bg.png",
    "CodeBuild": "Developer-Tools/AWS-CodeBuild_light-bg.png",
    "CodePipeline": "Developer-Tools/AWS-CodePipeline_light-bg.png",
    "Comprehend": "Machine-Learning/Amazon-Comprehend_light-bg.png",
    "Connect": "Business-Applications/Amazon-Connect_light-bg.png",
    "DocumentDB": "Database/Amazon-DocumentDB_light-bg.png",
    "Elastic Beanstalk": "Compute/AWS-Elastic-Beanstalk_light-bg.png",
    "ElastiCache": "Database/Amazon-ElastiCache_light-bg.png",
    "EventBridge": "Application-Integration/Amazon-EventBridge_light-bg.png",
    "Glue": "Analytics/AWS-Glue_light-bg.png",
    "Kinesis": "Analytics/Amazon-Kinesis_light-bg.png",
    "Lex": "Machine-Learning/Amazon-Lex_light-bg.png",
    "Lightsail": "Compute/Amazon-Lightsail_light-bg.png",
    "Macie": "Security-Identity-Compliance/Amazon-Macie_light-bg.png",
    "MemoryDB": "Database/Amazon-MemoryDB_light-bg.png",
    "Neptune": "Database/Amazon-Neptune_light-bg.png",
    "Polly": "Machine-Learning/Amazon-Polly_light-bg.png",
    "Rekognition": "Machine-Learning/Amazon-Rekognition_light-bg.png",
    "SageMaker": "Machine-Learning/Amazon-SageMaker_light-bg.png",
    "SecretsManager": "Security-Identity-Compliance/AWS-Secrets-Manager_light-bg.png",
    "Step Functions": "Application-Integration/AWS-Step-Functions_light-bg.png",
    "Textract": "Machine-Learning/Amazon-Textract_light-bg.png",
    "VPC": "Networking-Content-Delivery/Amazon-Virtual-Private-Cloud_VPC_light-bg.png"
}

def download_icon(service_name):
    if service_name not in service_to_filename:
        print(f"No icon mapping found for {service_name}")
        return False
    
    filename = service_to_filename[service_name]
    url = BASE_URL + filename
    output_path = os.path.join("images", f"{service_name.lower().replace(' ', '_')}.png")
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Process and save the image
            img = Image.open(BytesIO(response.content))
            img = img.resize((200, 200), Image.LANCZOS)
            img.save(output_path)
            print(f"Downloaded {service_name} icon to {output_path}")
            return True
        else:
            print(f"Failed to download {service_name} icon: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"Error downloading {service_name} icon: {e}")
        return False

def main():
    success_count = 0
    
    for service in aws_services:
        if download_icon(service):
            success_count += 1
        # Add a small delay to avoid rate limiting
        time.sleep(0.5)
    
    print(f"Downloaded {success_count} out of {len(aws_services)} icons")

if __name__ == "__main__":
    main()
