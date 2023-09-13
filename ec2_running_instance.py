import boto3
def check_for_avalability():

    try:
        # Create a session using the "default" profile
        aws_region = "eu-north-1"

        mng_console = boto3.session.Session(profile_name="default",region_name=aws_region)
        # Create an EC2 client
        ec2_console = mng_console.client(service_name="ec2")

        # Describe EC2 instances
        response = ec2_console.describe_instances()

        # Print instance information
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                print("Instance ID:", instance['InstanceId'])
                print("Instance State:", instance['State']['Name'])
                print("Instance Type:", instance['InstanceType'])
                print("=" * 40)  # Separator between instances

    except Exception as e:
        print("An error occurred:", e)

