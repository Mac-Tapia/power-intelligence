"""Optional local bearer gateway: hash-only credentials and tenant-owned stores.

This profile does not expose a service on external interfaces or replace TLS/OIDC.
Tokens are provisioned outside Git and never passed in URLs or stored by the UI.
"""

from __future__ import annotations

import hmac
import json
import math
import re
import time
from contextlib import AsyncExitStack, asynccontextmanager
from hashlib import sha256
from pathlib import Path

from fastapi import FastAPI
from starlette.responses import JSONResponse


def load_grants(path: Path) -> list[dict]:
    if any(p.is_symlink() or p.is_junction() for p in [path, *path.parents]):
        raise ValueError("credential links are forbidden")
    if path.stat().st_size > 1_000_000:
        raise ValueError("credential configuration too large")
    data = json.loads(path.read_text(encoding="utf-8"))
    grants = data.get("grants")
    if data.get("schema") != "unitesis.credentials/1" or not isinstance(grants, list) or not grants:
        raise ValueError("invalid credential configuration")
    digests = set()
    for grant in grants:
        digest, tenant = grant.get("token_sha256", ""), grant.get("tenant_id", "")
        expiry = grant.get("expires_at")
        if (not isinstance(digest, str) or not re.fullmatch(r"[a-f0-9]{64}", digest)
                or digest in digests or not isinstance(tenant, str)
                or not re.fullmatch(r"[a-z][a-z0-9_-]{0,63}", tenant)
                or grant.get("role") not in {"reader", "engineer"}
                or not isinstance(grant.get("subject"), str) or not grant["subject"]
                or isinstance(expiry, bool) or not isinstance(expiry, (int, float))
                or not math.isfinite(expiry)):
            raise ValueError("invalid credential grant")
        digests.add(digest)
    return grants


class TenantAccess:
    def __init__(self, app, *, grants: list[dict], tenants: dict[str, FastAPI]):
        self.app, self.grants, self.tenants = app, grants, tenants

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http" or not scope["path"].startswith("/api/"):
            await self.app(scope, receive, send)
            return
        if scope["path"] == "/api/v1/health" and scope["method"] == "GET":
            await JSONResponse({"status": "ok", "version": "0.2.0", "auth": "bearer",
                                "tenant_isolation": True})(
                scope, receive, send)
            return
        headers = dict(scope.get("headers", []))
        value = headers.get(b"authorization", b"").decode("latin-1")
        token = value[7:] if value.startswith("Bearer ") else ""
        digest = sha256(token.encode()).hexdigest()
        principal = next((g for g in self.grants if hmac.compare_digest(g["token_sha256"], digest)
                          and g["expires_at"] > time.time()), None) if len(token) >= 32 else None
        if principal is None:
            await JSONResponse({"detail": "authentication required"}, status_code=401,
                               headers={"WWW-Authenticate": "Bearer"})(scope, receive, send)
            return
        if scope["method"] not in {"GET", "HEAD"} and principal["role"] != "engineer":
            await JSONResponse({"detail": "insufficient role"}, status_code=403)(
                scope, receive, send)
            return
        scope.setdefault("state", {})["principal"] = {
            k: principal[k] for k in ("tenant_id", "subject", "role")}
        await self.tenants[principal["tenant_id"]](scope, receive, send)


def create_secure_app(database: str | Path, credentials: Path, factory, ui_dir: Path) -> FastAPI:
    grants = load_grants(credentials.absolute())
    if str(database) == ":memory:":
        raise ValueError("authenticated tenant stores require a database file")
    base = Path(database).absolute()
    if any(p.is_symlink() or p.is_junction() for p in [base, *base.parents]):
        raise ValueError("linked database paths are forbidden")
    folder = base.parent / (base.stem + ".tenants")
    if folder.is_symlink() or folder.is_junction():
        raise ValueError("linked tenant directory is forbidden")
    tenants = {}
    try:
        for tenant in sorted({g["tenant_id"] for g in grants}):
            path = folder / (tenant + ".sqlite")
            if path.is_symlink() or path.is_junction():
                raise ValueError("linked tenant database is forbidden")
            tenants[tenant] = factory(path)
    except Exception:
        for app in tenants.values():
            app.state.repository.close()
            app.state.jobs.close()
        raise

    @asynccontextmanager
    async def lifespan(app):
        async with AsyncExitStack() as stack:
            for child in tenants.values():
                await stack.enter_async_context(child.router.lifespan_context(child))
            yield

    app = FastAPI(title="UNITESIS authenticated local gateway", lifespan=lifespan)
    app.add_middleware(TenantAccess, grants=grants, tenants=tenants)
    from .telemetry import AuditMiddleware, RequestMetrics

    app.add_middleware(AuditMiddleware, metrics=RequestMetrics(), stage="gateway")
    app.state.tenants = tenants
    if ui_dir.is_dir():
        from fastapi.staticfiles import StaticFiles

        app.mount("/", StaticFiles(directory=ui_dir, html=True), name="workstation")
    return app
