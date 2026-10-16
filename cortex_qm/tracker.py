"""Ausgefuellte Begehungs-Checkliste (CSV) in Status-Reports ueberfuehren.

Kern-Regel: ``erledigt`` gewinnt immer; alles andere wird am Stichtag
gemessen — Faelligkeit vor dem Stichtag ist ``ueberfaellig``, sonst
``offen``.
"""

from __future__ import annotations

import csv
import html
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Dict, List, Sequence

from . import CortexQmFehler
from .tenant import TenantProfil

PFLICHT_SPALTEN = (
    "id",
    "fundstelle",
    "pruefpunkt",
    "status",
    "faellig_am",
    "verantwortung",
    "bemerkung",
)


def status_normalisieren(roh_status: str, faellig: date, stichtag: date) -> str:
    status = roh_status.strip().lower()
    if status == "erledigt":
        return "erledigt"
    if faellig < stichtag:
        return "ueberfaellig"
    return "offen"


def lese_zeilen(csv_pfad: Path, stichtag: date) -> List[Dict[str, str]]:
    if not csv_pfad.is_file():
        raise CortexQmFehler(f"Tracker-CSV nicht gefunden: {csv_pfad}")
    zeilen: List[Dict[str, str]] = []
    with csv_pfad.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        feldnamen = reader.fieldnames or []
        fehlend = [spalte for spalte in PFLICHT_SPALTEN if spalte not in feldnamen]
        if fehlend:
            raise CortexQmFehler(
                f"Tracker-CSV {csv_pfad.name}: Pflichtspalten fehlen: "
                + ", ".join(fehlend)
            )
        for nummer, zeile in enumerate(reader, start=2):
            try:
                faellig = date.fromisoformat(zeile["faellig_am"])
            except ValueError:
                raise CortexQmFehler(
                    f"Tracker-CSV {csv_pfad.name}, Zeile {nummer} "
                    f"({zeile.get('id', '?')}): 'faellig_am' ist kein "
                    f"ISO-Datum: {zeile['faellig_am']!r}"
                ) from None
            zeile["status_report"] = status_normalisieren(
                zeile["status"], faellig, stichtag
            )
            zeilen.append(zeile)
    return zeilen


def schreibe_md(
    zeilen: Sequence[Dict[str, str]], tenant: TenantProfil, stichtag: date, out: Path
) -> None:
    counts = Counter(zeile["status_report"] for zeile in zeilen)
    lines = [
        "# Begehungs-Tracker Status-Report",
        "",
        f"Praxis: {tenant.praxis}",
        f"Stichtag: {stichtag.isoformat()}",
        "",
        f"- erledigt: {counts['erledigt']}",
        f"- offen: {counts['offen']}",
        f"- ueberfaellig: {counts['ueberfaellig']}",
        "",
        "| ID | Fundstelle | Pruefpunkt | Verantwortung | Faellig am | Status | Bemerkung |",
        "|---|---|---|---|---|---|---|",
    ]
    for zeile in zeilen:
        lines.append(
            f"| {zeile['id']} | {zeile['fundstelle']} | {zeile['pruefpunkt']} | "
            f"{zeile['verantwortung']} | {zeile['faellig_am']} | "
            f"{zeile['status_report']} | {zeile['bemerkung']} |"
        )
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")


def schreibe_html(
    zeilen: Sequence[Dict[str, str]], tenant: TenantProfil, stichtag: date, out: Path
) -> None:
    counts = Counter(zeile["status_report"] for zeile in zeilen)
    table_rows = []
    for zeile in zeilen:
        status = zeile["status_report"]
        table_rows.append(
            f'<tr class="{html.escape(status)}">'
            f"<td>{html.escape(zeile['id'])}</td>"
            f"<td>{html.escape(zeile['fundstelle'])}</td>"
            f"<td>{html.escape(zeile['pruefpunkt'])}</td>"
            f"<td>{html.escape(zeile['verantwortung'])}</td>"
            f"<td>{html.escape(zeile['faellig_am'])}</td>"
            f"<td>{html.escape(status)}</td>"
            f"<td>{html.escape(zeile['bemerkung'])}</td>"
            "</tr>"
        )
    out.write_text(
        f"""<!doctype html>
<html lang="de">
<meta charset="utf-8">
<title>Begehungs-Tracker Status-Report</title>
<style>
body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; margin: 32px; color: #1f2933; }}
h1 {{ font-size: 24px; margin: 0 0 8px; }}
.summary {{ display: flex; gap: 12px; margin: 18px 0; }}
.summary span {{ border: 1px solid #b8c2cc; padding: 6px 10px; }}
table {{ width: 100%; border-collapse: collapse; font-size: 12px; }}
th, td {{ border: 1px solid #b8c2cc; padding: 7px; vertical-align: top; }}
th {{ background: #eef2f7; text-align: left; }}
tr.erledigt td {{ background: #eef8ef; }}
tr.offen td {{ background: #fff8e6; }}
tr.ueberfaellig td {{ background: #fdeeee; }}
@media print {{ body {{ margin: 12mm; }} .summary {{ display: block; }} table {{ font-size: 10px; }} }}
</style>
<h1>Begehungs-Tracker Status-Report</h1>
<p>{html.escape(tenant.praxis)} · Stichtag {stichtag.isoformat()}</p>
<div class="summary">
  <span>erledigt: {counts['erledigt']}</span>
  <span>offen: {counts['offen']}</span>
  <span>ueberfaellig: {counts['ueberfaellig']}</span>
</div>
<table>
<thead><tr><th>ID</th><th>Fundstelle</th><th>Pruefpunkt</th><th>Verantwortung</th><th>Faellig am</th><th>Status</th><th>Bemerkung</th></tr></thead>
<tbody>
{''.join(table_rows)}
</tbody>
</table>
</html>
""",
        encoding="utf-8",
    )
