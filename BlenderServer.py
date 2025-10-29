from __future__ import annotations

import socket
import threading
import traceback
from typing import Optional

import bpy  # type: ignore


class BlenderServer:
    """Standalone TCP server that receives Python and executes it in Blender.

    Public API:
    - start(host: str = "localhost", port: int = 9000) -> None
    - close(timeout: float = 2.0) -> None

    Implementation notes:
    - The server runs on a background thread. It uses a short accept timeout
      to poll for shutdown requests.
    - Received payloads are decoded as UTF-8 and executed with `exec` using
      a globals dict that exposes `bpy`.
    """

    def __init__(self) -> None:
        self._thread: Optional[threading.Thread] = None
        self._sock: Optional[socket.socket] = None
        self._running = False
        self._host = "127.0.0.1"
        self._port = 9000

    def start(self, host: str = "127.0.0.1", port: int = 9000) -> None:
        """Start the server in a daemon thread.

        If a server is already running this is a no-op.
        """
        if self._running:
            print(f"ConduitConnector already running on {self._host}:{self._port}")
            return

        self._host = host
        self._port = port
        self._running = True

        # create and bind socket here so errors surface synchronously
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # allow quick restart during development
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self._host, self._port))
        sock.listen(5)
        sock.settimeout(1.0)  # timeout used to check self._running periodically
        self._sock = sock

        self._thread = threading.Thread(target=self._serve_loop, daemon=True)
        self._thread.start()
        print(f"ConduitConnector listening on {self._host}:{self._port}")

    def is_running(self) -> bool:
        """Return whether the server is currently running."""
        return bool(self._running)

    def _serve_loop(self) -> None:
        assert self._sock is not None
        sock = self._sock
        while self._running:
            try:
                try:
                    conn, addr = sock.accept()
                except socket.timeout:
                    continue

                with conn:
                    try:
                        conn.settimeout(2.0)
                        data = b""
                        # single recv is fine for small payloads; adjust if needed
                        chunk = conn.recv(4096)
                        while chunk:
                            data += chunk
                            # try to read more if available
                            try:
                                chunk = conn.recv(4096)
                            except socket.timeout:
                                break

                        if not data:
                            continue

                        text = data.decode("utf-8")
                        print(f"ConduitConnector received from {addr}: {text!r}")

                        # Execute received Python with access to `bpy` only.
                        # WARNING: this will run arbitrary code. Only use on trusted
                        # networks and for local development.
                        globals_dict = {"bpy": bpy}
                        try:
                            exec(text, globals_dict)
                        except Exception:
                            print("Error executing received code:")
                            traceback.print_exc()
                    except Exception:
                        print("ConduitConnector connection handling error:")
                        traceback.print_exc()
            except OSError:
                # socket was closed or other fatal error
                break

        print("ConduitConnector server loop exiting")

    def close(self, timeout: float = 2.0) -> None:
        """Stop the server and close the socket.

        Blocks briefly waiting for the thread to exit (timeout seconds).
        """
        if not self._running:
            return

        self._running = False

        # close socket to unblock accept()
        try:
            if self._sock:
                self._sock.close()
        except Exception:
            pass

        # wait for thread to finish
        if self._thread is not None:
            self._thread.join(timeout)
            if self._thread.is_alive():
                print("ConduitConnector thread did not stop within timeout")

        self._thread = None
        self._sock = None
        print("ConduitConnector closed")


# global singleton helpers
_global_connector: Optional[BlenderServer] = None


def get_global_connector() -> Optional[BlenderServer]:
    """Return the global connector instance if any."""
    return _global_connector

def start_global_connector(host: str = "127.0.0.1", port: int = 9000) -> BlenderServer:
    """Create and start a global connector if not already present."""
    global _global_connector
    if _global_connector is None:
        _global_connector = BlenderServer()
        _global_connector.start(host=host, port=port)
    else:
        if not _global_connector.is_running():
            _global_connector.start(host=host, port=port)
    return _global_connector


def stop_global_connector(timeout: float = 2.0) -> None:
    """Stop and clear the global connector."""
    global _global_connector
    if _global_connector is None:
        return
    try:
        _global_connector.close(timeout=timeout)
    finally:
        _global_connector = None


if __name__ == "__main__":
    # simple local run for development / manual testing
    conn = BlenderServer()
    try:
        conn.start()
        print("Press Ctrl+C to stop")
        while True:
            try:
                # keep the main thread alive
                threading.Event().wait(1.0)
            except KeyboardInterrupt:
                break
    finally:
        conn.close()
