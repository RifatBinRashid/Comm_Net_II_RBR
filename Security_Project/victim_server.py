import socket
import threading
import time

HOST = '127.0.0.1'
PORT = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(100)

print(f"[*] Victim Server listening on {HOST}:{PORT}")
print("[*] Waiting for connections...\n")

connection_count = 0

def handle_client(conn, addr, conn_id, arrival_time):
    response_time = time.time() - arrival_time
    print(f"[+] Connection #{conn_id} from {addr} | Response time: {response_time*1000:.2f} ms")
    try:
        conn.send(b"HTTP/1.1 200 OK\r\n\r\nHello!")
    except:
        pass
    conn.close()

while True:
    try:
        conn, addr = server.accept()
        arrival_time = time.time()
        connection_count += 1
        t = threading.Thread(target=handle_client, args=(conn, addr, connection_count, arrival_time))
        t.daemon = True
        t.start()
    except KeyboardInterrupt:
        print("\n[*] Server shutting down.")
        break

server.close()