import os
import psutil
import shutil
import random
import traceback

def list_usb_drives():
    """
    Lists all USB drives (removable drives) attached to the system.
    """
    usb_drives = []
    for part in psutil.disk_partitions():
        if 'removable' in part.opts:  # Identify removable drives (USB)
            usb_drives.append(part.device)
    return usb_drives

def overwrite_device(device_path):
    """
    Overwrites the entire device (USB drive) with multiple passes of random patterns
    based on the Gutmann algorithm.
    """
    # Define patterns for overwriting the entire device
    overwrite_patterns = [
        b'\x00',       # Zeroes
        b'\xFF',       # Ones
        os.urandom(512), # Random byte pattern
        b'\x55',       # Alternating bits
        b'\xAA',       # Alternating bits
        b'\x5A'        # Reverse alternating bits
    ]
    
    try:
        # Get the total size of the device (use 'device_path' as a raw device)
        total_size = shutil.disk_usage(device_path).total
        
        # Open the device in binary write mode (admin privileges needed)
        with open(device_path, 'r+b') as device:
            # Perform multiple overwrite passes
            for pass_num in range(3):  # Limiting to 3 passes for flash storage
                print(f"Starting Pass {pass_num + 1}")
                # Loop through each overwrite pattern
                for pattern in overwrite_patterns:
                    # Write the pattern to the entire device
                    device.seek(0)  # Reset to the beginning of the device
                    while device.tell() < total_size:
                        device.write(pattern)
                    device.flush()
                    os.fsync(device.fileno())  # Ensure data is written to the device
                print(f"Pass {pass_num + 1} completed for device: {device_path}")

        print("Overwrite process completed.")

    except Exception as e:
        print(f"Error overwriting device {device_path}: {e}")
        traceback.print_exc()

def main():
    # List all available USB drives
    usb_drives = list_usb_drives()
    
    if not usb_drives:
        print("No USB drives detected.")
        return
    
    # Display available drives for selection
    print("USB Drives detected:")
    for idx, drive in enumerate(usb_drives, 1):
        print(f"{idx}. {drive}")
    
    # Ask the user to select a drive
    try:
        choice = int(input("Enter the number of the USB drive to overwrite: "))
        if choice < 1 or choice > len(usb_drives):
            print("Invalid choice. Exiting...")
            return
        selected_drive = usb_drives[choice - 1]
        print(f"You selected: {selected_drive}")
        
        # Proceed to overwrite the selected USB drive
        overwrite_device(selected_drive)

    except ValueError:
        print("Invalid input. Please enter a valid number.")
        return

# Run the script
if __name__ == "__main__":
    main()
