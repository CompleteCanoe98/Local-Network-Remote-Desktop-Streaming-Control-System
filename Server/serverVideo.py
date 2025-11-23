# -----------------------------
# SERVER (Screen Streamer)
# -----------------------------

import socket
import cv2
import numpy as np
import mss
import threading
import time


DISCOVERY_PORT = 4999
VIDEO_PORT = 5000
TARGET_IP = None

MAX_UDP = 60000  # safe chunk size (<65507) # for windows
MAX_UDP = 8000  # safe chunk size for mac

# ------------------------------
# 1. DISCOVERY LISTENER
# ------------------------------
def discovery_listener():
    global TARGET_IP

    print("[DISCOVERY] Waiting for client...")

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("0.0.0.0", DISCOVERY_PORT))

    while True:
        msg, addr = sock.recvfrom(1024)
        if msg == b"DISCOVER_STREAMING_SERVER":
            client_ip = addr[0]
            print(f"[DISCOVERY] Client discovered: {client_ip}")

            # send back "serverip:videoport"
            server_ip = socket.gethostbyname(socket.gethostname())
            reply = f"{server_ip}:{VIDEO_PORT}".encode()
            sock.sendto(reply, addr)

            TARGET_IP = client_ip



# ------------------------------
# 2. VIDEO STREAMER
# ------------------------------
def video_streamer():
    global TARGET_IP

    print("[VIDEO] Waiting for discovery...")
    while TARGET_IP is None:
        time.sleep(0.1)

    print(f"[VIDEO] Streaming to {TARGET_IP}:{VIDEO_PORT}")

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sct = mss.mss()
    monitor = sct.monitors[1]

    try:
        while True:
            # Capture monitor
            frame = np.array(sct.grab(monitor))

            # Downscale → saves bandwidth
            frame = cv2.resize(frame, (854, 480)) # for mac

            # Encode JPEG
            ok, buffer = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 25]) # for mac
            data = buffer.tobytes()

            # ---- CHUNK THE FRAME ----
            for i in range(0, len(data), MAX_UDP):
                sock.sendto(data[i:i+MAX_UDP], (TARGET_IP, VIDEO_PORT))

            # END marker
            sock.sendto(b"END", (TARGET_IP, VIDEO_PORT))

            time.sleep(0.03)  # ~30 FPS
    finally:
        sock.close()
        print("[VIDEO] Streaming stopped.")


# ------------------------------
# 3. START
# ------------------------------
if __name__ == "__main__":
    t = threading.Thread(target=discovery_listener, daemon=True)
    t.start()

    video_streamer()
