import socket
import threading
import time
from time import sleep
import bpy  # type: ignore


class ConduitClient:
    HOST = "127.0.0.1"
    PORT = 8000
    TIMEOUT = 2

    def __init__(self, interval: float = 1.0):
        self.interval = interval  # seconds between heartbeats
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
            self._ping()
            sleep(1)

    def _ping(self):
        """Send ping command and update _alive status."""
        response = self.send("ping")
        if not response:
            return False
        with self._lock:
            alive = response["status"] == "ok"

            if not self._alive:
                log("Successfully connected to Conduit. Conduit <- Blender", "success")
                print(
                    "Successfully connected to Conduit. Conduit <- Blender", "success"
                )

            if alive:
                self._alive = True
            else:
                self._alive = False
            self._last_check = time.time()

    def register_blender_exec(self):
        path = bpy.app.binary_path
        self.send("blender_exec", path=path)

    # --------------------------
    # Command sending
    # --------------------------

    def send(self, command: str, **kwargs) -> dict | None:
        """Send a JSON command to the server and receive a JSON response using a delimiter."""
        import json

        payload = {"cmd": command, **kwargs}
        data = json.dumps(payload) + "\n"  # <-- add delimiter
        data_bytes = data.encode("utf-8")

        try:
            with socket.create_connection(
                (self.HOST, self.PORT), timeout=self.TIMEOUT
            ) as s:
                s.sendall(data_bytes)

                # Receive until delimiter
                buffer = ""
                while True:
                    chunk = s.recv(1024).decode("utf-8")
                    if not chunk:
                        break  # connection closed
                    buffer += chunk
                    if "\n" in buffer:
                        line, _ = buffer.split("\n", 1)
                        return json.loads(line)
                # if we exit loop without finding delimiter
                return json.loads(buffer) if buffer else None

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
    client.send("log", message=message, level=level)


def register():
    client = get_client()
    client.register_blender_exec()
