"""Module to list all IAM users in AWS account"""

# Import modules.

import boto3
import custom_module_clear_screen

# Define functions.

def list_all_iam_users():
    """Function to list all IAM users in the AWS account."""
    aws_console = boto3.session.Session(profile_name="aws-admin")
    aws_service = aws_console.resource(service_name="iam")
    count = 0
    print("The IAM users are:\n")
    # aws_service.users.all() is a collection of objects and not dictionaries.
    # Each object has attributes of corresponding user.
    # name is one such attribute.
    for user in aws_service.users.all():
        print(user.name)  # user object has an attribute name, so, we print it this way.
        #print(user.get("name")) # This fails as it is not a dict.
        # It says AttributeError: 'iam.User' object has no attribute 'get'.
        count = count + 1
        # As it is not a dict, we use count in each iteration to find total no. of objects.
        # If it would have been a dict, then we would have used len() to find dict length.
    print(f"\nTotal number of users: {count}")

def main():
    """First function to be called"""
    custom_module_clear_screen.clear_screen()
    print("This script will print all IAM users from the AWS account.")
    input("Press ENTER to proceed...\n")
    list_all_iam_users()
    print()

# Call main() when the script is executed.

if __name__ == "__main__":
    main()
