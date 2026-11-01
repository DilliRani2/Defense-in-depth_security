#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
import argparse
import time

BASE = Path(__file__).resolve().parent
SECRET_FILE = BASE / "secret.txt"
ACCESS_LOG = BASE / "access.log"
EXPECTED_TOKEN = "lab-token-2026"

class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        return

    def record_rejection(self, reason):
        with ACCESS_LOG.open("a") as handle:
            handle.write(f"{int(time.time())} rejected {self.path} {reason}\n")

    def do_GET(self):
        if self.path != "/secret":
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"not found\n")
            return

        token = self.headers.get("X-Access-Token", "")
        if token != EXPECTED_TOKEN:
            self.record_rejection("missing_or_bad_token")
            self.send_response(403)
            self.end_headers()
            self.wfile.write(b"forbidden\n")
            return

        data = SECRET_FILE.read_bytes()
        self.send_response(200)
        self.end_headers()
        self.wfile.write(data)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8081)
    args = parser.parse_args()
    server = HTTPServer((args.host, args.port), Handler)
    print(f"serving on {args.host}:{args.port}", flush=True)
    server.serve_forever()

if __name__ == "__main__":
    main()