"""Application cases: everything local (country, utility, CRS, timezone, currency,
regulatory profiles, data sources) is declared per case; the core stays universal.

A case never supplies electrical defaults. It is validated against the regulatory
profiles and the dataset source registry so the three stay synchronized.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

CASE_SCHEMA = "unitesis.application-case/1"
ROLES = ("pilot_application_case", "application_case")
_CASE_ID = re.compile(r"^[a-z]{2}-[a-z0-9]+(-[a-z0-9]+)*$")


class CaseError(ValueError):
    """The application case is incomplete or inconsistent with registries."""


@dataclass(frozen=True, slots=True)
class ApplicationCase:
    case_id: str
    role: str
    country: str
    region: str
    utility: str
    frequency_hz: float
    crs: str
    crs_verified: bool
    timezone: str
    measurement_interval: str
    currency: str
    regulatory_profiles: tuple[str, ...]
    source_ids: tuple[str, ...]
    authorized: bool

    @property
    def zone(self) -> ZoneInfo:
        return ZoneInfo(self.timezone)


def _require(data: dict[str, Any], path: str) -> Any:
    node: Any = data
    for key in path.split("."):
        if not isinstance(node, dict) or key not in node:
            raise CaseError(f"missing field {path}; values are never defaulted")
        node = node[key]
    return node


def parse_case(data: dict[str, Any]) -> ApplicationCase:
    if data.get("schema") != CASE_SCHEMA:
        raise CaseError(f"unsupported case schema {data.get('schema')!r}")
    case_id = _require(data, "case_id")
    if not isinstance(case_id, str) or not _CASE_ID.match(case_id):
        raise CaseError("case_id must look like '<country>-<region>-<utility>' in lowercase")
    role = _require(data, "role")
    if role not in ROLES:
        raise CaseError(f"role must be one of {ROLES}")
    country = _require(data, "country")
    if not isinstance(country, str) or not re.fullmatch(r"[A-Z]{2}", country):
        raise CaseError("country must be an ISO-3166 alpha-2 code")
    if not case_id.startswith(country.lower() + "-"):
        raise CaseError("case_id must start with the country code")
    freq = _require(data, "electrical.frequency_hz")
    if isinstance(freq, bool) or freq not in (50, 60):
        raise CaseError("frequency_hz must be 50 or 60")
    crs = _require(data, "spatial.crs")
    if not isinstance(crs, str) or not re.fullmatch(r"EPSG:\d{4,6}", crs):
        raise CaseError("crs must be an EPSG code such as EPSG:32718")
    tz = _require(data, "time.timezone")
    try:
        ZoneInfo(tz)
    except (ZoneInfoNotFoundError, ValueError, TypeError) as exc:
        raise CaseError(f"unknown timezone {tz!r}") from exc
    currency = _require(data, "economics.currency")
    if not isinstance(currency, str) or not re.fullmatch(r"[A-Z]{3}", currency):
        raise CaseError("currency must be an ISO-4217 code")
    for name in ("region", "utility"):
        if not str(_require(data, name)).strip():
            raise CaseError(f"{name} is required")
    profiles = _require(data, "regulatory_profiles")
    sources = _require(data, "source_ids")
    if not isinstance(profiles, list) or not isinstance(sources, list):
        raise CaseError("regulatory_profiles and source_ids must be arrays")
    if len(set(sources)) != len(sources):
        raise CaseError("duplicate source_ids")
    return ApplicationCase(
        case_id=case_id, role=role, country=country, region=data["region"],
        utility=data["utility"], frequency_hz=float(freq), crs=crs,
        crs_verified=_require(data, "spatial.crs_status") == "verified",
        timezone=tz, measurement_interval=_require(data, "time.measurement_interval"),
        currency=currency, regulatory_profiles=tuple(profiles), source_ids=tuple(sources),
        authorized=_require(data, "authorization.status") == "confirmed")


def check_consistency(case: ApplicationCase, profiles_dir: Path,
                      sources_registry: dict[str, Any]) -> list[str]:
    """Return every inconsistency between the case, regulatory profiles and data sources."""
    issues: list[str] = []
    for pid in case.regulatory_profiles:
        path = profiles_dir / f"{pid}.json"
        if not path.is_file():
            issues.append(f"regulatory profile {pid} not found")
            continue
        jurisdiction = json.loads(path.read_text(encoding="utf-8")).get("jurisdiction")
        if jurisdiction != case.country:
            issues.append(f"profile {pid} jurisdiction {jurisdiction!r} != case country "
                          f"{case.country!r}")
    registered = {s["source_id"]: s for s in sources_registry.get("sources", [])}
    for sid in case.source_ids:
        src = registered.get(sid)
        if src is None:
            issues.append(f"source {sid} not in registry")
        elif src.get("case_id") != case.case_id:
            issues.append(f"source {sid} belongs to case {src.get('case_id')!r}")
    for sid, src in registered.items():
        if src.get("case_id") == case.case_id and sid not in case.source_ids:
            issues.append(f"source {sid} claims this case but is not listed in it")
    return issues


def load_case(path: str | Path) -> ApplicationCase:
    return parse_case(json.loads(Path(path).read_text(encoding="utf-8")))


def list_cases(cases_dir: str | Path) -> dict[str, Path]:
    """Case files by id; files starting with '_' are templates and are skipped."""
    folder = Path(cases_dir)
    return {p.stem: p for p in sorted(folder.glob("*.json")) if not p.name.startswith("_")}
