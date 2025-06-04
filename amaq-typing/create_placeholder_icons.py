import os
from PIL import Image, ImageDraw, ImageFont

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

# Colors for different service categories
colors = {
    "Compute": (255, 153, 0),      # Orange
    "Storage": (146, 204, 60),     # Green
    "Database": (48, 151, 221),    # Blue
    "Networking": (223, 83, 83),   # Red
    "Analytics": (156, 106, 222),  # Purple
    "Security": (255, 212, 0),     # Yellow
    "Integration": (0, 195, 170),  # Teal
    "Machine Learning": (255, 153, 204),  # Pink
    "Default": (100, 100, 100)     # Gray
}

# Service to category mapping
service_categories = {
    "S3": "Storage",
    "EC2": "Compute",
    "Lambda": "Compute",
    "DynamoDB": "Database",
    "CloudFront": "Networking",
    "RDS": "Database",
    "SQS": "Integration",
    "SNS": "Integration",
    "CloudWatch": "Networking",
    "IAM": "Security",
    "Route53": "Networking",
    "ECS": "Compute",
    "EKS": "Compute",
    "Fargate": "Compute",
    "API Gateway": "Integration",
    "Cognito": "Security",
    "Amplify": "Integration",
    "AppSync": "Integration",
    "Athena": "Analytics",
    "Aurora": "Database",
    "Batch": "Compute",
    "Bedrock": "Machine Learning",
    "CloudFormation": "Integration",
    "CodeBuild": "Integration",
    "CodePipeline": "Integration",
    "Comprehend": "Machine Learning",
    "Connect": "Integration",
    "DocumentDB": "Database",
    "Elastic Beanstalk": "Compute",
    "ElastiCache": "Database",
    "EventBridge": "Integration",
    "Glue": "Analytics",
    "Kinesis": "Analytics",
    "Lex": "Machine Learning",
    "Lightsail": "Compute",
    "Macie": "Security",
    "MemoryDB": "Database",
    "Neptune": "Database",
    "Polly": "Machine Learning",
    "Rekognition": "Machine Learning",
    "SageMaker": "Machine Learning",
    "SecretsManager": "Security",
    "Step Functions": "Integration",
    "Textract": "Machine Learning",
    "VPC": "Networking"
}

def create_service_icon(service_name):
    # Determine the color based on service category
    category = service_categories.get(service_name, "Default")
    color = colors.get(category, colors["Default"])
    
    # Create a 200x200 image with the category color
    img = Image.new('RGB', (200, 200), color)
    draw = ImageDraw.Draw(img)
    
    try:
        # Try to use a TrueType font
        font = ImageFont.truetype("Arial", 24)
    except IOError:
        # Fallback to default font
        font = ImageFont.load_default()
    
    # Draw the service name
    text_width, text_height = draw.textsize(service_name, font=font) if hasattr(draw, 'textsize') else (100, 20)
    position = ((200 - text_width) // 2, (200 - text_height) // 2)
    draw.text(position, service_name, fill=(255, 255, 255), font=font)
    
    # Save the image
    output_path = os.path.join("images", f"{service_name.lower().replace(' ', '_')}.png")
    img.save(output_path)
    print(f"Created placeholder icon for {service_name} at {output_path}")

def main():
    for service in aws_services:
        create_service_icon(service)
    print(f"Created {len(aws_services)} placeholder icons")

if __name__ == "__main__":
    main()
