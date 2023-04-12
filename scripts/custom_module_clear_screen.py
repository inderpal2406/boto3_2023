"""Custom module built to clear screen on WIndows & Linux hosts."""

# Import modules.

import platform
import os

# Define functions.

def clear_screen():
    """Function to detect OS & clear screen"""
    if platform.system() == "Windows":
        os.system("cls")
    elif platform.system() == "Linux":
        os.system("clear")
    else:
        print("This script clears screen for Windows & Linux OS only.")

def main():
    """First function to be called."""
    clear_screen()

# Call main() if this script is executed explicitly.

if __name__ == "__main__":
    main()
