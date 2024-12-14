import os
import psutil
import shutil
import random
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
    usb_drives = []
    for part in psutil.disk_partitions():
        if 'removable' in part.opts:  
            usb_drives.append(part.device)
    return usb_drives

def overwrite_device(device_path):
    overwrite_patterns = [
        b'\x00',       
        b'\xFF',      
        os.urandom(512), 
        b'\x55',       
        b'\xAA',      
        b'\x5A'        
    ]
    
    try:
        total_size = shutil.disk_usage(device_path).total
        
        with open(device_path, 'r+b') as device:
            for pass_num in range(3):  
                print(f"Starting Pass {pass_num + 1}")
                for pattern in overwrite_patterns:
                    device.seek(0)  
                    while device.tell() < total_size:
                        device.write(pattern)
                    device.flush()
                    os.fsync(device.fileno())  
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
    
    print("USB Drives detected:")
    for idx, drive in enumerate(usb_drives, 1):
        print(f"{idx}. {drive}")
    
    try:
        choice = int(input("Enter the number of the USB drive to overwrite: "))
        if choice < 1 or choice > len(usb_drives):
            print("Invalid choice. Exiting...")
            return
        selected_drive = usb_drives[choice - 1]
        print(f"You selected: {selected_drive}")
        
        overwrite_device(selected_drive)

    except ValueError:
        print("Invalid input. Please enter a valid number.")
        return


if __name__ == "__main__":
    main()
