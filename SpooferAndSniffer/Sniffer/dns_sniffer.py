import scapy.all as scapy

def process_dns_packet(packet):
    if packet.haslayer(scapy.DNSQR):
        domain= packet[scapy.DNSQR].qname.decode()

        print(f"[+] Dominio {domain}")


def main():
    interface = ""#enter your inteface wifi
    print("\n[+] Interceptando paquetes de la maquina victima")
    scapy.sniff(iface=interface,filter="udp and port 53",prn=process_dns_packet,store=0) #le decimos al sniffer que filtre por el puerto udp y el puerto 43

if __name__ == "__main__":
    main()
