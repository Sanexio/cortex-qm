"""Gemeinsame Pfade fuer die Testsuite (Repo-Wurzel, Regeln, Demos).

Die Demos unter ``examples/`` werden ausschliesslich LESEND verwendet:
sie sind die festgeschriebene Referenz fuer die Paritaetstests der
Framework-Schicht.
"""

from __future__ import annotations

from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
RULES = REPO / "rules"
KATEGORIEN_BEISPIEL = RULES / "CATEGORIES_EXAMPLE.md"
AUDIT_DEMO = REPO / "examples" / "audit-checkliste-demo"
DOCX_DEMO = REPO / "examples" / "docx-kommentar-demo"

# Fiktiver Demo-Tenant (Demo-Praxis Musterstadt) — lebt NUR in
# examples/ und in den Tests, nie in der Framework-Schicht.
DEMO_PRAXIS = "Demo-Praxis Musterstadt"
DEMO_ROLLEN = ("QM-Beauftragte", "Aerztliche Leitung")
