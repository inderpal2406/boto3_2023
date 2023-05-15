"""Module to start database EC2 instances only"""

# Import modules.

import boto3
import custom_module_clear_screen

# Define functions.

def main():
    """First function to be called"""
    custom_module_clear_screen.clear_screen()
    print("This script starts all EC2 instances which host databases.")
    input("Press ENTER to proceed...")
    aws_region = "ap-south-1"
    aws_session = boto3.session.Session(profile_name="aws-admin")
    ec2_client = aws_session.client(service_name="ec2",region_name=aws_region)
    response_dict = ec2_client.describe_instances(
        Filters=[
            {
                "Name": "tag:App",
                "Values": [
                    "DB Server",
                ]
            },
        ]
    )
    instances_list = response_dict.get("Reservations")
    db_instance_list = []
    for instance in instances_list:
        instance_info_list = instance.get("Instances")
        # Above list will always have one item in it.
        instance_info_dict = instance_info_list[0]
        instance_id = instance_info_dict.get("InstanceId")
        db_instance_list.append(instance_id)
    #ec2_client.start_instances(InstanceIds=db_instance_list)
    ec2_client.stop_instances(InstanceIds=db_instance_list)
    print("DB Instances stopped.")

if __name__ == "__main__":
    main()
