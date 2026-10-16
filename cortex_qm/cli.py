"""cortex-qm CLI — tenant-neutrale Werkzeuge ueber dem Regelwerk.

Unterbefehle:

- ``checkliste``  — Begehungs-Checkliste aus einer Kategorien-Datei erzeugen
- ``tracker``     — ausgefuellte Checklisten-CSV in Status-Reports ueberfuehren
- ``kommentare``  — Word-Kommentare einer DOCX als Massnahmen-Tabelle auswerten

Der Tenant (Praxisname, Rollen) wird immer explizit uebergeben; es gibt
keine eingebaute Praxis.
"""

from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path
from typing import Optional, Sequence

from . import CortexQmFehler, __version__, checkliste, kommentare, regelwerk, tracker
from .tenant import TenantProfil


def _parser_bauen() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cortex-qm",
        description="Tenant-neutrale QM-Werkzeuge ueber dem cortex-qm-Regelwerk.",
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    sub = parser.add_subparsers(dest="befehl", required=True)

    p_check = sub.add_parser(
        "checkliste", help="Begehungs-Checkliste aus Kategorien-Datei erzeugen"
    )
    p_check.add_argument(
        "--kategorien",
        required=True,
        type=Path,
        help="Kategorien-Datei nach rules/SCHEMA.md (z.B. rules/CATEGORIES_EXAMPLE.md)",
    )
    p_check.add_argument("--praxis", required=True, help="Tenant-Praxisname")
    p_check.add_argument(
        "--rolle",
        action="append",
        default=[],
        dest="rollen",
        help="Beteiligte Rolle (mehrfach angebbar)",
    )
    p_check.add_argument("--out-md", required=True, type=Path)
    p_check.add_argument("--out-html", type=Path, default=None)

    p_track = sub.add_parser(
        "tracker", help="Ausgefuellte Checklisten-CSV in Status-Reports ueberfuehren"
    )
    p_track.add_argument("--csv", required=True, type=Path)
    p_track.add_argument("--praxis", required=True, help="Tenant-Praxisname")
    p_track.add_argument(
        "--stichtag",
        default=date.today().isoformat(),
        help="ISO-Datum des Stichtags (Default: heute)",
    )
    p_track.add_argument("--out-md", required=True, type=Path)
    p_track.add_argument("--out-html", type=Path, default=None)

    p_komm = sub.add_parser(
        "kommentare", help="Word-Kommentare einer DOCX als Massnahmen-Tabelle auswerten"
    )
    p_komm.add_argument("docx", type=Path, help="Eingabe-DOCX")
    p_komm.add_argument("out_md", type=Path, help="Ausgabe-Markdown")

    return parser


def _checkliste(args: argparse.Namespace) -> int:
    tenant = TenantProfil(praxis=args.praxis, rollen=tuple(args.rollen))
    kategorien = regelwerk.lade_kategorien(args.kategorien)
    zeilen = checkliste.checklisten_zeilen(kategorien)
    checkliste.schreibe_md(zeilen, tenant, args.out_md)
    print(f"{len(zeilen)} Pruefpunkte erzeugt: {args.out_md}")
    if args.out_html is not None:
        checkliste.schreibe_html(zeilen, tenant, args.out_html)
        print(f"HTML erzeugt: {args.out_html}")
    return 0


def _tracker(args: argparse.Namespace) -> int:
    tenant = TenantProfil(praxis=args.praxis)
    try:
        stichtag = date.fromisoformat(args.stichtag)
    except ValueError:
        raise CortexQmFehler(
            f"--stichtag ist kein ISO-Datum: {args.stichtag!r}"
        ) from None
    zeilen = tracker.lese_zeilen(args.csv, stichtag)
    tracker.schreibe_md(zeilen, tenant, stichtag, args.out_md)
    print(f"{len(zeilen)} Tracker-Zeilen ausgewertet: {args.out_md}")
    if args.out_html is not None:
        tracker.schreibe_html(zeilen, tenant, stichtag, args.out_html)
        print(f"HTML erzeugt: {args.out_html}")
    return 0


def _kommentare(args: argparse.Namespace) -> int:
    zeilen = kommentare.auswerten(args.docx)
    kommentare.schreibe_md(zeilen, args.docx.name, args.out_md)
    print(f"{len(zeilen)} Kommentare extrahiert: {args.out_md}")
    return 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = _parser_bauen()
    args = parser.parse_args(argv)
    try:
        if args.befehl == "checkliste":
            return _checkliste(args)
        if args.befehl == "tracker":
            return _tracker(args)
        if args.befehl == "kommentare":
            return _kommentare(args)
        parser.error(f"Unbekannter Befehl: {args.befehl}")
        return 2
    except CortexQmFehler as fehler:
        print(f"cortex-qm: {fehler}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
