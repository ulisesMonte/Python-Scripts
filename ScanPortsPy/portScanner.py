import socket
import argparse
from concurrent.futures import ThreadPoolExecutor
import signal
import sys

open_sockets = []


def handler(sig, frame): # id signal and frame is the status of script excecution
    print(f"\n[+] Exit the program")
    
    for socket in open_sockets:
        socket.close()
    
    sys.exit(1)

signal.signal(signal.SIGINT,handler)

def getArguments():
    parser = argparse.ArgumentParser(description="Fast TCP Port Scanner")
    parser.add_argument("-t","--target", dest="target",required=True, help="Victim target to scan (EX: -t 127.0.0.1 )") #When write the -t parameter, what you write will be saved in the target variable
    parser.add_argument("-p","--port",dest="port",required=True, help="The port range you want to scan (EX: -p 1-100) ")
    options = parser.parse_args()
    return options.target, options.port


def create_socket():
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.settimeout(1) # wait 1 second, if in 1 second cant do an answer, return close
    open_sockets.append(s)
    return s

def port_scanner(port, host):
    s= create_socket()

    try:
        s.connect((host,port))
        s.sendall(b"HEAD / HTTP/ 1.0\r\n\r\n")
        response = s.recv(1024)
        response = response.decode(errors="ignore").split("\n")
        if response:
            print(f"\n[+] The port is open -{response}")
            for line in response:
                print(f"{line}")
        else:
            print(f"The port {port} is open")
    except (socket.timeout, ConnectionRefusedError):
        pass
    finally:
        s.close()

def scan_ports(ports,target):

    with ThreadPoolExecutor(max_workers=50) as executor: # limit the proccess
        executor.map(lambda port: port_scanner(port,target),ports)

def parse_ports(ports_str):
    if "-" in ports_str:
        start,end = map(int,ports_str.split("-"))
        return range(start,end+1)
    elif "," in ports_str:
        return map(int(ports_str.split(",")))
    else:
        return (int(ports_str),)
    


def main():
    target, ports_str = getArguments()
    ports = parse_ports(ports_str)
    scan_ports(ports,target)

if __name__ == "__main__":
    main()