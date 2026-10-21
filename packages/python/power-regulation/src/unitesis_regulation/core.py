"""Pure policy boundary. No web access, side effects or fictitious regulatory certification."""
from pathlib import Path
import json

class RegulatoryBlock(ValueError):
    pass

def load_profile(profile_id: str, config_dir: Path) -> dict:
    if not profile_id or not all(c.isalnum() or c in "_-" for c in profile_id):
        raise RegulatoryBlock("Invalid profile id")
    path = config_dir / (profile_id + ".json")
    if not path.is_file():
        raise RegulatoryBlock("Profile not found: " + profile_id)
    profile = json.loads(path.read_text(encoding="utf-8"))
    if profile["profile_id"] != profile_id:
        raise RegulatoryBlock("Profile id mismatch")
    return profile

def check_profile_for_submission(profile: dict) -> None:
    if not profile.get("approved_for_automatic_certification", False):
        raise RegulatoryBlock("Regulatory certification BLOCKED: approved consolidated rules and human review required")

def evaluate_completeness(payload: dict) -> dict:
    required = ("project_id", "study_id", "regulatory_profile", "alternatives", "model_snapshot", "economic_currency", "reviewer")
    missing = sorted(x for x in required if not payload.get(x))
    return {"complete": not missing, "missing": missing, "status": "preliminary_not_certified"}
