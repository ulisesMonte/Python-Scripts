import argparse
import re
import subprocess
def get_arguments():
    parser = argparse.ArgumentParser(description="Tool for changes de MAC Address")
    parser.add_argument("-i", "--interface", required=True, dest="interface",help="Network Interface Name ")
    parser.add_argument("-m","--mac", required=True,dest="mac_address",help="New Mac Address")


    return parser.parse_args()







def is_valid_input(interface,mac_address):
    is_valid_interface = re.match(r'^[e][n|t][s|h]\d{1,2}$',interface) 
    is_valid_mac_address = re.match(r'^([A-Fa-f0-9]{2}[:]){5}[A-Fa-f0-9]{2}$',mac_address)
    return is_valid_interface and is_valid_mac_address
def change_mac_address(mac_address,interface):
    if is_valid_input(interface, mac_address):
        subprocess.run(["ifconfig", interface, "down"])
        subprocess.run(["ifconfig", interface, "hw", "ether", mac_address])
        subprocess.run(["ifconfig", interface, "up"])
        print("The MAC address change")
    else:
        print("Wrong Data")
def main():
    args = get_arguments()
    change_mac_address(args.mac_address,args.interface)

if __name__ == "__main__":
    main()
