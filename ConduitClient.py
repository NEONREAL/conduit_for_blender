import socket
import threading
import time
import json

class ConduitClient:
    HOST = "127.0.0.1"
    PORT = 8000
    TIMEOUT = 2

    def __init__(self, interval: float = 1.0):
        self.interval = interval  # seconds between heartbeats
        self._last_check = 0.0
        self._alive = False
        self._lock = threading.Lock()
        self._stop = False

        # Start background heartbeat thread
        self._thread = threading.Thread(target=self._heartbeat_loop, daemon=True)
        self._thread.start()

    # --------------------------
    # Internal heartbeat loop
    # --------------------------
    def _heartbeat_loop(self):
        while not self._stop:
            now = time.time()
            if now - self._last_check >= self.interval:
                self._ping()
            time.sleep(0.05)  # small sleep to avoid busy waiting

    def _ping(self):
        """Send ping command and update _alive status."""
        response = self.send("ping")
        if not response:
            return False
        with self._lock:
            alive = response["status"] == "ok"
            if alive:
                self._alive = True
            self._last_check = time.time()

    # --------------------------
    # Command sending
    # --------------------------
    def send(self, command: str, **kwargs) -> dict | None:
        payload = {"cmd": command, **kwargs}
        data = json.dumps(payload).encode("utf-8")
        try:
            with socket.create_connection((self.HOST, self.PORT), timeout=self.TIMEOUT) as s:
                s.sendall(data)
                try:
                    resp = s.recv(1024)
                    return json.loads(resp.decode("utf-8"))
                except socket.timeout:
                    return None
        except Exception as e:
            print("ConduitClient send error:", e)
            return None


    # --------------------------
    # Public API
    # --------------------------
    def check(self) -> bool:
        """Returns last known alive status (non-blocking)."""
        with self._lock:
            return self._alive




    def stop(self):
        """Stops background heartbeat thread."""
        self._stop = True
        self._thread.join()


# --------------------------
# Singleton for Blender usage
# --------------------------
_instance: ConduitClient | None = None

def get_client() -> ConduitClient:
    global _instance
    if _instance is None:
        _instance = ConduitClient()
    return _instance

def get_heartbeat() -> bool:
    """Shortcut to check if the server is alive."""
    return get_client().check()

def log(message: str, level: str = "info"):        
    """Send a log command to the server."""
    client = get_client()
    client.send("log", message=message,level=level)