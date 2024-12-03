import socket
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host=input("Enter the IP address of the target host: ")
port=int(input("Enter the Port you want to scan: "))
def PortScanner(port):
    if s.connect((host,port)):
        print("The port is closed")
    else:
        print("The port is open")

PortScanner(port)
