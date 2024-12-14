import os
import traceback
print(r'''                                                                              
                                 ,----,                                       
           .---.   ,---,       .'   .`|  ,---,       ,-.----.       ,---,     
          /. ./|,`--.' |    .'   .'   ; '  .' \      \    /  \    .'  .' `\   
      .--'.  ' ;|   :  :  ,---, '    .'/  ;    '.    ;   :    \ ,---.'     \  
     /__./ \ : |:   |  '  |   :     ./:  :       \   |   | .\ : |   |  .`\  | 
 .--'.  '   \' .|   :  |  ;   | .'  / :  |   /\   \  .   : |: | :   : |  '  | 
/___/ \ |    ' ''   '  ;  `---' /  ;  |  :  ' ;.   : |   |  \ : |   ' '  ;  : 
;   \  \;      :|   |  |    /  ;  /   |  |  ;/  \   \|   : .  / '   | ;  .  | 
 \   ;  `      |'   :  ;   ;  /  /--, '  :  | \  \ ,';   | |  \ |   | :  |  ' 
  .   \    .\  ;|   |  '  /  /  / .`| |  |  '  '--'  |   | ;\  \'   : | /  ;  
   \   \   ' \ |'   :  |./__;       : |  :  :        :   ' | \.'|   | '` ,/   
    :   '  |--" ;   |.' |   :     .'  |  | ,'        :   : :-'  ;   :  .'     
     \   \ ;    '---'   ;   |  .'     `--''          |   |.'    |   ,.'       
      '---"             `---'                        `---'      '---'         
                                                                              ''')

def list_usb_drives():
    """Lists all removable devices (e.g., USB drives) on Linux."""
    removable_drives = []
    sys_block_path = "/sys/block"

    for device in os.listdir(sys_block_path):
        removable_path = os.path.join(sys_block_path, device, "removable")
        device_path = f"/dev/{device}"

        try:
            with open(removable_path, "r") as f:
                if f.read().strip() == "1": 
                    removable_drives.append(device_path)
        except FileNotFoundError:
            continue

    return removable_drives

def overwrite_device(device_path):
    """Securely overwrites the selected USB device."""
    overwrite_patterns = [
        b'\x00',  
        b'\xFF', 
        os.urandom(512) 
    ]

    try:
        with open(device_path, 'r+b') as device:
            device.seek(0, os.SEEK_END)
            total_size = device.tell()  # Get the total size of the device
            print(f"Detected size: {total_size} bytes")

            # Perform multiple overwrite passes
            for pass_num in range(3):
                print(f"Starting Pass {pass_num + 1}")
                for pattern in overwrite_patterns:
                    device.seek(0)  # Reset to the beginning of the device
                    while device.tell() < total_size:
                        device.write(pattern * 1024) 
                    device.flush()
                    os.fsync(device.fileno())
                print(f"Pass {pass_num + 1} completed for device: {device_path}")

        print("Overwrite process completed successfully.")

    except PermissionError:
        print(f"Permission denied. Please run the script as an administrator.")
    except Exception as e:
        print(f"Error overwriting device {device_path}: {e}")
        traceback.print_exc()

def confirm_action(prompt):
    """Prompts the user for a yes/no confirmation."""
    while True:
        response = input(f"{prompt} (yes/no): ").strip().lower()
        if response in ['yes', 'no']:
            return response == 'yes'
        print("Invalid input. Please enter 'yes' or 'no'.")

def main():
    """Main function to list, select, and overwrite USB drives."""
    usb_drives = list_usb_drives()
    
    if not usb_drives:
        print("No removable USB drives detected.")
        return
    
    print("Removable USB Drives detected:")
    for idx, drive in enumerate(usb_drives, 1):
        print(f"{idx}. {drive}")
    
    try:
        choice = int(input("Enter the number of the USB drive to overwrite: "))
        if choice < 1 or choice > len(usb_drives):
            print("Invalid choice. Exiting...")
            return
        selected_drive = usb_drives[choice - 1]
        print(f"You selected: {selected_drive}")
        
        if confirm_action("Are you sure you want to overwrite this drive? This will permanently delete all data."):
            overwrite_device(selected_drive)
        else:
            print("Operation cancelled.")

    except ValueError:
        print("Invalid input. Please enter a valid number.")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
