"""Spec 004: structured request traces without bodies, queries or credentials."""

import json
import logging
import threading
import time
import uuid
from collections import Counter

RESOURCES = {"health", "snapshots", "studies", "jobs", "results", "examples", "catalogs",
             "economic-basis", "metrics"}
LOGGER = logging.getLogger("unitesis.audit")


class RequestMetrics:
    def __init__(self):
        self.counts = Counter()
        self.lock = threading.Lock()

    def record(self, status):
        with self.lock:
            self.counts[str(status)] += 1

    def snapshot(self):
        with self.lock:
            return {"requests": sum(self.counts.values()), "status_counts": dict(self.counts)}


class AuditMiddleware:
    def __init__(self, app, *, metrics: RequestMetrics, stage: str = "application"):
        self.app, self.metrics, self.stage = app, metrics, stage

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        state = scope.setdefault("state", {})
        trace = state.setdefault("request_id", uuid.uuid4().hex)
        started, status = time.monotonic(), 500

        async def traced_send(message):
            nonlocal status
            if message["type"] == "http.response.start":
                status = message["status"]
                headers = [(k, v) for k, v in message.get("headers", []) if k != b"x-request-id"]
                message = message | {"headers": headers + [(b"x-request-id", trace.encode())]}
            await send(message)

        try:
            await self.app(scope, receive, traced_send)
        finally:
            self.metrics.record(status)
            parts = scope["path"].split("/")
            resource = parts[3] if len(parts) > 3 and parts[3] in RESOURCES else "other"
            LOGGER.info(json.dumps({"event": "http_request", "stage": self.stage,
                "request_id": trace, "method": scope["method"], "resource": resource,
                "status": status, "duration_ms": round((time.monotonic() - started) * 1000, 3)}))
