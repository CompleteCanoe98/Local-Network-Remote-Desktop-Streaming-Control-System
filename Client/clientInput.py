import socket
import json
import threading
from pynput import mouse, keyboard
import time
import tkinter as tk

DISCOVERY_PORT = 4998
SERVER_IP = None
SERVER_PORT = 5020

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# -----------------------------
# 1. KEY MAPPING (The Fix)
# -----------------------------
# Map pynput keys to pyautogui keys
KEY_MAPPING = {
    "Key.space": "space",
    "Key.enter": "enter",
    "Key.backspace": "backspace",
    "Key.tab": "tab",
    "Key.esc": "esc",
    "Key.delete": "delete",
    "Key.up": "up",
    "Key.down": "down",
    "Key.left": "left",
    "Key.right": "right",
    "Key.shift": "shift",
    "Key.shift_r": "shiftright",
    "Key.ctrl_l": "ctrlleft",
    "Key.ctrl_r": "ctrlright",
    "Key.alt_l": "altleft",
    "Key.alt_r": "altright",
    "Key.caps_lock": "capslock",
    "Key.cmd": "win",
    "Key.cmd_r": "winright"
}

def get_pyautogui_key(key):
    """Converts pynput key object to pyautogui string"""
    # 1. Handle character keys (a, b, 1, 2, etc.)
    if hasattr(key, 'char') and key.char is not None:
        return key.char

    # 2. Handle special keys (Space, Enter, etc.)
    k_str = str(key)
    
    # Check explicit mapping first
    if k_str in KEY_MAPPING:
        return KEY_MAPPING[k_str]
    
    # Fallback: strip "Key." prefix (e.g. Key.f1 -> f1)
    return k_str.replace("Key.", "")

# -----------------------------
# 2. DISCOVERY & NETWORKING
# -----------------------------
def discover_server():
    global SERVER_IP, SERVER_PORT
    print("[DISCOVERY] Searching...")
    ds = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ds.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    ds.settimeout(2)
    try:
        ds.sendto(b"DISCOVER_INPUT_SERVER", ("255.255.255.255", DISCOVERY_PORT))
        data, _ = ds.recvfrom(1024)
        SERVER_IP, port_str = data.decode().split(":")
        SERVER_PORT = int(port_str)
        print(f"[CONNECTED] Server at {SERVER_IP}:{SERVER_PORT}")
        return True
    except:
        return False

def send_event(obj):
    if SERVER_IP:
        try:
            sock.sendto(json.dumps(obj).encode(), (SERVER_IP, SERVER_PORT))
        except:
            pass

# -----------------------------
# 3. INPUT LISTENERS
# -----------------------------
last_send = 0
RATE_LIMIT = 0.016  # 60 FPS for mouse

def on_move(x, y):
    global last_send
    now = time.time()
    if (now - last_send) > RATE_LIMIT:
        last_send = now
        send_event({"type": "mouse_move", "x": x / CLIENT_W, "y": y / CLIENT_H})

def on_click(x, y, button, pressed):
    btn = button.name if hasattr(button, "name") else str(button)
    msg = {"type": "mouse_click", "button": btn, "action": "down" if pressed else "up"}
    send_event(msg) 
    # Double-send removed here to prevent double-clicking

def on_scroll(x, y, dx, dy):
    send_event({"type": "mouse_scroll", "dx": dx, "dy": dy})

def on_key_action(key, action):
    key_name = get_pyautogui_key(key)
    msg = {"type": "key", "key": key_name, "action": action}
    send_event(msg)
    # Double-send removed here to prevent double-typing

def on_press(key): on_key_action(key, "down")
def on_release(key): on_key_action(key, "up")

# -----------------------------
# 4. MAIN
# -----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    CLIENT_W, CLIENT_H = root.winfo_screenwidth(), root.winfo_screenheight()

    if discover_server():
        # Start listeners
        with mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as ml, \
             keyboard.Listener(on_press=on_press, on_release=on_release) as kl:
            ml.join()
            kl.join()
    else:
        print("Server not found. Make sure serverInput.py is running.")