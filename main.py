'''file sharing program that uses an AWS EC2 instance and Apache2 to share files with ease. It works by first uploading the file to the EC2 instance. Once the file is uploaded,
the program generates a QR code that contains the file's URL. The QR code can then be shared with anyone who wants to download the file. When the QR code is scanned, the user 
will be taken to the file's URL, where they can download it directlyfrom the AWS server.'''

import os
import boto3
from boto3.resources import response
from botocore.exceptions import ClientError


def create_ec2_instance(imageId, instance_Type, key_Name, security_group, aws_region):
    try:
        # Create a session using the "default" profile and the specified region
        mng_console = boto3.session.Session(profile_name="default", region_name=aws_region)

        # Create an EC2 resource
        ec2_resource = mng_console.resource(service_name="ec2")

        # Specify instance details
        instance_details = {
            "ImageId": imageId,
            "InstanceType": instance_Type,
            "KeyName": key_Name,
            "MinCount": 1,
            "MaxCount": 1,
            "SecurityGroups": [security_group],  # Replace with your security group name
            # Add more parameters as needed
        }

        # Launch the instance
        instances = ec2_resource.create_instances(**instance_details)

        # Print instance IDs
        for instance in instances:
            print("Created instance:", instance.id)

    except Exception as e:
        print("An error occurred:", e)


def pass_command(imageId, user_command, aws_region):

    try:
        start_sessions = boto3.session.Session(profile_name="default", region_name=aws_region)
        consle = start_sessions.client(service_name="ssm")
        response = consle.send_command(
            InstanceIds=[imageId],  # Use InstanceIds keyword
            DocumentName="AWS-RunShellScript",
            Parameters={"commands": [user_command]},  # Use Parameters keyword
        )
        command_id = response["Command"]["CommandId"]  # Use "Command" instead of "command"
        print(f"Command sent!! Command ID: {command_id}")
    except Exception as e:
        print("An error occurred:", e)


user_use = input("Select your choice:- \npress 1 for creating instance \npress 2 for using existing instance ")

if user_use == "1":
    imageId = input("Enter Your AMI ID:- ")  # value for instance id
    instance_Type = input("Enter Your Instance Type:- ")  # value pf instance type eg:- t3.micro
    key_Name = input("Enter Your Key Name type:- ")  # your key name example <**anything**>.pem
    security_group = input("Enter Security Group Name:- ")  # your security group name example <launch-wizard-5>
    # Specify the AWS region
    aws_region = "eu-north-1"  # Replace with your desired region
    create_ec2_instance(imageId, instance_Type, key_Name, security_group, aws_region)

elif user_use == "2":
    imageId = input("Enter Your Instance ID:- ")  # value for instance id
    aws_region = "eu-north-1"  # Replace with your desuser_commandired region
    user_command = "echo hello world"
    pass_command(imageId, user_command, aws_region)
else:
    print("Enter a valid input")
