import socket
import time
import csv

HOST = '127.0.0.1'
PORT = 9999
NUM_REQUESTS = 50

print(f"[*] Measuring baseline latency ({NUM_REQUESTS} requests)...\n")

latencies = []

for i in range(NUM_REQUESTS):
    try:
        start = time.time()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((HOST, PORT))
        s.recv(1024)
        end = time.time()
        s.close()

        latency = (end - start) * 1000  # convert to milliseconds
        latencies.append(('baseline', i+1, latency))
        print(f"  Request #{i+1:02d} | Latency: {latency:.2f} ms")
        time.sleep(0.1)  # small gap between requests

    except Exception as e:
        print(f"  Request #{i+1:02d} | FAILED: {e}")
        latencies.append(('baseline', i+1, -1))

# Save to CSV
with open('latency_results.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['phase', 'request_num', 'latency_ms'])
    writer.writerows(latencies)

avg = sum(l for _, _, l in latencies if l > 0) / len([l for _, _, l in latencies if l > 0])
print(f"\n[*] Baseline complete.")
print(f"[*] Average latency: {avg:.2f} ms")
print(f"[*] Results saved to latency_results.csv")