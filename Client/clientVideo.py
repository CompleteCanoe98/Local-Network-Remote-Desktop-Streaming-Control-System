import socket
import cv2
import numpy as np
import tkinter as tk
import select

# --- CONFIG ---
DISCOVERY_PORT = 4999
VIDEO_PORT = None  # Auto-discovered
SERVER_IP = None   # Auto-discovered

# ------------------------------
# 1. DISCOVERY (Standard)
# ------------------------------
def discover_server():
    global SERVER_IP, VIDEO_PORT
    print("[INFO] Looking for streaming server...")
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.settimeout(5)
    
    try:
        sock.sendto(b"DISCOVER_STREAMING_SERVER", ("255.255.255.255", DISCOVERY_PORT))
        data, addr = sock.recvfrom(1024)
        reply = data.decode().split(":")
        SERVER_IP = reply[0]
        VIDEO_PORT = int(reply[1])
        print(f"[FOUND] Server at {SERVER_IP}:{VIDEO_PORT}")
        return True
    except socket.timeout:
        print("[ERROR] No server found.")
        return False
    finally:
        sock.close()

# ------------------------------
# 2. MAIN FAST LOOP
# ------------------------------
if __name__ == "__main__":
    # Get screen size
    root = tk.Tk()
    root.withdraw()
    SCREEN_W = root.winfo_screenwidth()
    SCREEN_H = root.winfo_screenheight()

    if not discover_server():
        exit()

    # Setup UDP Socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 8 * 1024 * 1024) # 8MB buffer
    sock.bind(("0.0.0.0", VIDEO_PORT))
    sock.setblocking(False) # <--- KEY: Non-blocking mode

    # Setup Window
    cv2.namedWindow("Stream", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Stream", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    print("[INFO] Streaming active. Latency optimized.")

    packet_buffer = [] # List is faster than byte string concatenation

    while True:
        # 1. DRAIN THE SOCKET
        # Read ALL packets currently waiting in the network card buffer
        # This ensures we never fall behind.
        packets = []
        while True:
            try:
                data, _ = sock.recvfrom(65536)
                packets.append(data)
            except BlockingIOError:
                # No more data available right now
                break
            except OSError:
                break

        # 2. PROCESS PACKETS
        # If we received data, reconstruct the frames
        if packets:
            for data in packets:
                if data == b"END":
                    # We found a complete frame!
                    if packet_buffer:
                        # Join the chunks to form the JPEG
                        full_frame_data = b"".join(packet_buffer)
                        
                        # --- DECODE AND DISPLAY IMMEDIATELY ---
                        # (This replaces the old frame, so we only see the newest)
                        np_arr = np.frombuffer(full_frame_data, np.uint8)
                        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

                        if frame is not None:
                            frame = cv2.resize(frame, (SCREEN_W, SCREEN_H))
                            cv2.imshow("Stream", frame)
                        
                        # Clear buffer for the next frame
                        packet_buffer = []
                else:
                    # Just a chunk, add it to the list
                    packet_buffer.append(data)

        # 3. HANDLE GUI EVENTS
        if cv2.waitKey(1) == 27: # ESC
            break

    cv2.destroyAllWindows()