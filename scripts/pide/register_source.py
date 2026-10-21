"""Register a user-provided local PDF with SHA256; do NOT infer authenticity."""

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
# Untracked repository directory. Never commit source PDFs automatically.
DIR = ROOT / "storage" / "regulatory-originals"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf", required=True, type=Path)
    ap.add_argument("--origin-url", required=True)
    ap.add_argument(
        "--document-type",
        choices=["original_methodology_draft", "approved_regulation_candidate"],
        required=True,
    )
    a = ap.parse_args()
    if not a.pdf.is_file() or a.pdf.suffix.lower() != ".pdf":
        ap.error("Existing PDF required")
    data = a.pdf.read_bytes()
    if not data.startswith(b"%PDF-"):
        ap.error("Invalid PDF magic number")
    digest = hashlib.sha256(data).hexdigest()
    DIR.mkdir(parents=True, exist_ok=True)
    safe = DIR / f"{digest[:16]}.pdf"
    if not safe.exists():
        safe.write_bytes(data)
    manifest = {
        "original_filename": a.pdf.name,
        "sha256": digest,
        "bytes": len(data),
        "source_url_claimed": a.origin_url,
        "document_type_claimed": a.document_type,
        "authenticity_verified": False,
        "full_text_reviewed": False,
        "regulatory_approval_verified": False,
        "notes": "Local hash only; legal and format review pending",
    }
    (DIR / f"{digest[:16]}.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(json.dumps(manifest, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
