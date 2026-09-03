import json
import os
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

import psycopg

DATABASE_URL = os.environ["DATABASE_URL"]
VERSION = "2026.09.02-report-headers"


def connection():
    for _ in range(30):
        try:
            return psycopg.connect(DATABASE_URL)
        except psycopg.OperationalError:
            time.sleep(1)
    raise RuntimeError("database did not become ready")


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        return

    def send_json(self, status, payload):
        encoded = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/health":
            with connection() as conn:
                conn.execute("SELECT 1")
            self.send_json(200, {"status": "ok"})
            return
        if parsed.path == "/version":
            self.send_json(200, {"version": VERSION})
            return
        if parsed.path != "/reports":
            self.send_json(404, {"error": "not_found"})
            return
        report_type = parse_qs(parsed.query).get("type", ["reconciliation"])[0]
        started = time.perf_counter()
        with connection() as conn:
            rows = conn.execute(
                "SELECT id, report_type, created_at, total_cents "
                "FROM reports WHERE report_type = %s "
                "AND created_at >= now() - interval '7 days'",
                (report_type,),
            ).fetchall()
        elapsed_ms = (time.perf_counter() - started) * 1000
        self.send_response(200)
        self.send_header("X-Report-Format", "summary")
        self.send_header("Content-Type", "application/json")
        encoded = json.dumps({"count": len(rows), "report_type": report_type, "latency_ms": round(elapsed_ms, 3)}).encode()
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)


if __name__ == "__main__":
    ThreadingHTTPServer(("0.0.0.0", 8080), Handler).serve_forever()
