import argparse
import subprocess
import signal
import sys
from concurrent.futures import ThreadPoolExecutor


def def_handler(sig, frame):
    print("\n[!] Exit the program")
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

def get_arguments():
    parser = argparse.ArgumentParser(description="Tool for find device ON in the network(ICMP)")
    parser.add_argument("-t","--target",required=True,dest="target",help="Host or Network range to scan")

    args = parser.parse_args()
    return args.target

def parse_target(target_str):
    #192.168.1.1-100
    target_str_splitted = target_str.split('.') # [192, 168, 1, "1-100"]
    first_three_octets = '.'.join(target_str_splitted[:3])# 192.168.1

    if len(target_str_splitted) == 4:
        if "-" in target_str_splitted[3]:
            start, end = target_str_splitted[3].split("-")
            return [f"{first_three_octets}.{i}" for i in range(int(start), int(end)+1) ]
        else:
            return [target_str]
    else:
        print("\n[!] Wrong Data")


def host_discovery(target):
    try:
        ping = subprocess.run(["ping","-c","1",target], timeout=1,stdout= subprocess.DEVNULL)
        if ping.returncode == 0:
            print(f"\n[+] {target} Is ON")
    except subprocess.TimeoutExpired:
        pass



def main():

    target_str = get_arguments()
    targets = parse_target(target_str)
    print(f"Host ON in the Network: \n")
    maxThreads =100
    with ThreadPoolExecutor(max_workers=maxThreads) as executor:

        executor.map(host_discovery, targets)

if __name__ == "__main__":
    main()