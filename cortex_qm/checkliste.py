"""Begehungs-Checkliste aus Themen-Kategorien erzeugen (Markdown + HTML)."""

from __future__ import annotations

import html
from pathlib import Path
from typing import Dict, List, Sequence

from .regelwerk import Kategorie
from .tenant import TenantProfil

PFLICHT_FALLBACK = "Pflicht-Inhalte im Tenant-Kontext pruefen"


def checklisten_zeilen(kategorien: Sequence[Kategorie]) -> List[Dict[str, str]]:
    """Je Pflicht-Inhalt eine Pruefzeile mit stabiler ID ``CHK-<NN>-<nn>``."""
    zeilen: List[Dict[str, str]] = []
    for kategorie in kategorien:
        pflicht = list(kategorie.pflicht) or [PFLICHT_FALLBACK]
        for nummer, punkt in enumerate(pflicht, start=1):
            zeilen.append(
                {
                    "id": f"CHK-{kategorie.nr}-{nummer:02d}",
                    "bereich": f"{kategorie.nr} {kategorie.name}",
                    "pruefpunkt": punkt,
                    "anker": kategorie.anker,
                }
            )
    return zeilen


def schreibe_md(zeilen: Sequence[Dict[str, str]], tenant: TenantProfil, out: Path) -> None:
    lines = [
        "# Begehungs-Checkliste",
        "",
        f"Praxis: {tenant.praxis}",
        f"Rollen: {tenant.rollen_text}",
        "",
        "| ID | Bereich | Pruefpunkt | Regulatorischer Anker | Status | Notiz |",
        "|---|---|---|---|---|---|",
    ]
    for zeile in zeilen:
        lines.append(
            f"| {zeile['id']} | {zeile['bereich']} | {zeile['pruefpunkt']} | "
            f"{zeile['anker']} | offen |  |"
        )
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")


def schreibe_html(zeilen: Sequence[Dict[str, str]], tenant: TenantProfil, out: Path) -> None:
    body = "\n".join(
        "<tr>"
        f"<td>{html.escape(zeile['id'])}</td>"
        f"<td>{html.escape(zeile['bereich'])}</td>"
        f"<td>{html.escape(zeile['pruefpunkt'])}</td>"
        f"<td>{html.escape(zeile['anker'])}</td>"
        "<td>offen</td><td></td>"
        "</tr>"
        for zeile in zeilen
    )
    kopf = html.escape(f"{tenant.praxis} · Rollen: {tenant.rollen_text}")
    out.write_text(
        f"""<!doctype html>
<html lang="de">
<meta charset="utf-8">
<title>Begehungs-Checkliste</title>
<style>
body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; margin: 32px; color: #1f2933; }}
h1 {{ font-size: 24px; margin: 0 0 8px; }}
p {{ margin: 0 0 20px; }}
table {{ width: 100%; border-collapse: collapse; font-size: 12px; }}
th, td {{ border: 1px solid #b8c2cc; padding: 7px; vertical-align: top; }}
th {{ background: #eef2f7; text-align: left; }}
@media print {{ body {{ margin: 12mm; }} table {{ font-size: 10px; }} }}
</style>
<h1>Begehungs-Checkliste</h1>
<p>{kopf}</p>
<table>
<thead><tr><th>ID</th><th>Bereich</th><th>Pruefpunkt</th><th>Regulatorischer Anker</th><th>Status</th><th>Notiz</th></tr></thead>
<tbody>
{body}
</tbody>
</table>
</html>
""",
        encoding="utf-8",
    )
