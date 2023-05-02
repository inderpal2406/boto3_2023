"""Module to print details of EC2 instances in ap-south-1 region"""

# Import modules.

import csv
import boto3
import custom_module_clear_screen

# Define functions.

def upload_to_s3():
    """Function to upload CSV file to S3 bucket"""
    file = ".\\ec2_instance.csv"
    bucket_name = "inderpalaws05-test-bucket"
    aws_session = boto3.session.Session(profile_name="aws-admin")
    s3_client = aws_session.client(service_name="s3",region_name="ap-south-1")
    s3_client.upload_file(file,bucket_name,"ec2_instance.csv")
    # It fails if the 3rd arg Key is not provided in above function call.
    # Key arg is the name of the key to upload to.

def ec2_details(aws_region):
    """Function to display details of EC2 instances in specific region"""
    # Initiate CSV file.
    file = ".\\ec2_instance.csv"
    fileobj = open(file,"w",newline="") 
    # In absence of newline arg above, csv_writer.writerow() adds blank line b/wn each row.
    headings = [
        "Sr. No.",
        "Instance Name",
        "Private IP Address",
        "Instance ID",
        "Instance Type",
        "Instance State",
        "Last Launch Time"
        ]
    csv_writer = csv.writer(fileobj)
    csv_writer.writerow(headings)
    # Collect EC2 instance details using Boto3.
    aws_session = boto3.session.Session(profile_name="aws-admin")
    ec2_client = aws_session.client(service_name="ec2",region_name=aws_region)
    response_dict = ec2_client.describe_instances()
    instances_list = response_dict.get("Reservations")
    serial_number = 0
    for instance in instances_list:
        instance_info_list = instance.get("Instances")
        # Above list will always have one item in it.
        instance_info_dict = instance_info_list[0]
        instance_id = instance_info_dict.get("InstanceId")
        instance_type = instance_info_dict.get("InstanceType")
        launch_time = instance_info_dict.get("LaunchTime")
        private_ip = instance_info_dict.get("PrivateIpAddress")
        instance_state_dict = instance_info_dict.get("State")
        instance_state = instance_state_dict.get("Name")
        instance_tags_list = instance_info_dict.get("Tags")
        for tag in instance_tags_list:
            if tag.get("Key") == "Name":
                instance_name = tag.get("Value")
        serial_number = serial_number + 1
        csv_writer.writerow([
            serial_number,
            instance_name,
            private_ip,
            instance_id,
            instance_type,
            instance_state,
            launch_time
            ])
    fileobj.close()

def main():
    """First function to be called"""
    custom_module_clear_screen.clear_screen()
    region = "ap-south-1"
    print(f"This script displays details of all EC2 instances in {region} region.\n")
    input("Press ENTER to proceed.\n")
    ec2_details(region)
    upload_to_s3()

# Call main() when the script is executed.

if __name__ == "__main__":
    main()
