import socket
import threading
import json
import pyautogui

# --- OPTIMIZATION SETTINGS ---
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0  # <--- CRITICAL: Removes the 0.1s delay after every move
# -----------------------------

BIND_IP = "0.0.0.0"
BIND_PORT = 5020
DISCOVERY_PORT = 4998

SCREEN_W, SCREEN_H = pyautogui.size()

def discovery_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", DISCOVERY_PORT))
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            if data == b"DISCOVER_INPUT_SERVER":
                server_ip = socket.gethostbyname(socket.gethostname())
                sock.sendto(f"{server_ip}:{BIND_PORT}".encode(), addr)
        except:
            pass

def start_udp_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((BIND_IP, BIND_PORT))
    # Increase buffer size to prevent packet drops on OS level
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65536)
    
    print(f"[SPEED-OPTIMIZED] Server listening on {BIND_IP}:{BIND_PORT}")

    while True:
        try:
            # Receive packet
            data, _ = sock.recvfrom(1024)
            
            # Decode and Parse
            # We skip 'errors=ignore' and logging for maximum speed
            event = json.loads(data)
            t = event["type"]

            if t == "mouse_move":
                # Direct math, no helper variables, straight to C-level Move
                pyautogui.moveTo(
                    event["x"] * SCREEN_W, 
                    event["y"] * SCREEN_H, 
                    _pause=False # Ensure internal pause is skipped
                )

            elif t == "mouse_click":
                btn = event["button"]
                if event["action"] == "down":
                    pyautogui.mouseDown(button=btn, _pause=False)
                else:
                    pyautogui.mouseUp(button=btn, _pause=False)

            elif t == "mouse_scroll":
                pyautogui.scroll(event["dy"], _pause=False)

            elif t == "key":
                k = event["key"]
                if event["action"] == "down":
                    pyautogui.keyDown(k, _pause=False)
                else:
                    pyautogui.keyUp(k, _pause=False)

        except Exception:
            # Silently ignore errors to keep stream moving
            pass

if __name__ == "__main__":
    threading.Thread(target=discovery_server, daemon=True).start()
    start_udp_server()