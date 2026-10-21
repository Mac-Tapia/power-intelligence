"""Fail-closed authorization for *proposed* market settlement; no financial settlement."""

from collections.abc import Mapping


class MarketGateError(PermissionError):
    pass


def require_market_gates(proposal: Mapping) -> None:
    """Never treat payment or ledger acceptance as proof of electric feasibility."""
    if proposal.get("mode") != "authorized-pilot":
        raise MarketGateError("real trading disabled: simulation mode is the default")
    for field in (
        "legal_approval_id",
        "regulator_or_operator_approval_id",
        "metering_evidence_id",
        "power_flow_evidence_id",
        "network_snapshot_id",
        "human_approval_id",
    ):
        if not isinstance(proposal.get(field), str) or not proposal[field].strip():
            raise MarketGateError(f"missing {field}")
    if proposal.get("network_feasible") is not True:
        raise MarketGateError("network constraints not verified")
