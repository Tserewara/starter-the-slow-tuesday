import os
import statistics
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor

BASE = os.environ.get("SERVICE_URL", "http://localhost:8081")


def one(_):
    started = time.perf_counter()
    with urllib.request.urlopen(f"{BASE}/reports?type=reconciliation", timeout=10) as response:
        response.read()
        status = response.status
    return status, (time.perf_counter() - started) * 1000


# One untimed request first: the container's first DNS lookup and connection
# are not part of Tuesday's traffic.
one(None)
with ThreadPoolExecutor(max_workers=8) as pool:
    results = list(pool.map(one, range(40)))
latencies = sorted(value for status, value in results if status == 200)
p99 = latencies[max(0, int(len(latencies) * 0.99) - 1)]
print(f"requests={len(results)} successful={sum(status == 200 for status, _ in results)} p50_ms={statistics.median(latencies):.1f} p99_ms={p99:.1f} max_ms={max(latencies):.1f}")
