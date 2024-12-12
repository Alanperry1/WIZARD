# WIZARD (Write, Inspect, Zero, Analyze, Rewrite, Delete)

This reflects the key aspects of the script's functionality: overwriting, inspecting drives, zeroing data, analyzing device capacity, rewriting patterns, and deleting existing content. Let me know if you'd like to refine this further!

A Python script to securely overwrite removable USB drives, ensuring complete data erasure. This script is designed for Linux systems and requires administrative privileges to run.

## Features

- Lists all removable USB drives connected to the system.
- Allows the user to select a drive to overwrite.
- Securely overwrites the selected drive using multiple passes of different patterns:


## Requirements

- Linux operating system
- Python 3.x
- Administrative privileges to access and overwrite raw device files

## Usage

1. Clone the repository and navigate to the project directory:
   ```bash
   git clone https://github.com/Alanperry1/WIZARD.git
   cd WIZARD
   ```

2. Run the script with administrative privileges:
   ```bash
   sudo python3 WIZARD.py
   ```

3. Follow the on-screen prompts:
   - The script will display a list of detected removable USB drives.
   - Select the drive you wish to overwrite by entering its corresponding number.
   - Confirm your choice before the overwrite process begins.

## Code Walkthrough

### List USB Drives

The `list_usb_drives` function scans `/sys/block` for removable devices and returns their paths (e.g., `/dev/sdb`).

### Overwrite Device

The `overwrite_device` function performs multiple passes to securely overwrite the selected device:
- Null bytes (`\x00`)
- All 1s (`\xFF`)
- Random data generated using `os.urandom()`

### User Confirmation

The `confirm_action` function ensures the user is prompted before proceeding with any destructive action.

### Main Function

The `main` function handles:
- Detecting USB drives
- Allowing the user to select a drive
- Initiating the overwrite process

