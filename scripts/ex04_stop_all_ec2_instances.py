"""Module to stop any running instance & send email with details of those running instances"""

# Import modules.

import boto3
from botocore.exceptions import ClientError

# Define functions.

def main():
    """First function to be called"""
    # Collect info of all existing instances.
    # From this info, get instance ids of instances not in stopped state.
    aws_region = "ap-south-1"
    aws_session = boto3.session.Session(profile_name="aws-admin")
    ec2_client = aws_session.client(service_name="ec2",region_name=aws_region)
    response_dict = ec2_client.describe_instances()
    instances_list = response_dict.get("Reservations")
    not_stopped_instances_id_list = []
    not_stopped_instances_name_list = []
    for instance in instances_list:
        instance_info_list = instance.get("Instances")
        # Above list will always have one item in it.
        instance_info_dict = instance_info_list[0]
        instance_state = instance_info_dict.get("State").get("Name")
        if instance_state != "stopped":
            instance_id = instance_info_dict.get("InstanceId")
            not_stopped_instances_id_list.append(instance_id)
            instance_tags_list = instance_info_dict.get("Tags")
            for tag in instance_tags_list:
                if tag.get("Key") == "Name":
                    instance_name = tag.get("Value")
                    not_stopped_instances_name_list.append(instance_name)
    if len(not_stopped_instances_id_list) == 0:
        print("All instances are in stopped state.")
    else:
        # Try stopping the instances which are not in stopped state.
        try:
            ec2_client.stop_instances(InstanceIds=not_stopped_instances_id_list)
        except ClientError as e:
            print("Error while stopping instances.")
            print(e)
        else:
            # Send email with details of instances which were not stopped.
            # Send this email as no error received while stopping the instances.
            sender = "abc@test.com"
            recipient = "xyz@gmail.com"
            subject = "Non-stopped EC2 instances from last night."
            msg_start = "Hello,\n\n"
            # Convert instance name list to str to be concatenated in msg_body.
            # Objects of same data type can only be concatenated.
            # Concatenation of str & list data types don't work.
            # Str+str, list+list, etc concatenation works.
            instance_str = ", ".join(not_stopped_instances_name_list)
            msg_body = "Below instances were not in stopped state last night,\n\n"+instance_str+"\n\n"
            msg_end = "These instances were initiated to be stopped.\n\nThank You,\nAWS Lambda\n"
            message = msg_start+msg_body+msg_end
            charset = "utf-8"
            ses_client = aws_session.client(service_name="ses",region_name=aws_region)
            try:
                response = ses_client.send_email(
                    Source=sender,
                    Destination={
                        "ToAddresses": [recipient]
                    },
                    Message={
                        "Subject": {
                            "Data": subject,
                            "Charset": charset
                        },
                        "Body": {
                            "Text": {
                                "Data": message,
                                "Charset": charset
                            }
                        }
                    }
                )
            except ClientError as e:
                print("Error while sending email.")
                print(e)
            else:
                print("Email sent!")
                print(f"Message ID: {response.get('MessageId')}")

if __name__ == "__main__":
    main()
