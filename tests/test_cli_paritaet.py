"""CLI-Ende-zu-Ende + Paritaet Framework vs. festgeschriebene Demo-Ausgaben.

Die Dateien unter ``examples/`` sind die eingefrorene Referenz des
Demo-Tenants. Die Framework-Schicht muss — mit dem Demo-Tenant als
Eingabe — exakt dieselben Artefakte erzeugen. examples/ wird dabei nur
gelesen, alle Ausgaben landen in Temp-Verzeichnissen.
"""

from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from cortex_qm.cli import main

from .pfade import (
    AUDIT_DEMO,
    DEMO_PRAXIS,
    DEMO_ROLLEN,
    DOCX_DEMO,
    KATEGORIEN_BEISPIEL,
)


class TestParitaetMitDemos(unittest.TestCase):
    def test_checkliste_byte_identisch_zur_demo(self) -> None:
        referenz_md = (AUDIT_DEMO / "begehungs_checkliste.md").read_text(encoding="utf-8")
        referenz_html = (AUDIT_DEMO / "begehungs_checkliste.html").read_text(encoding="utf-8")
        with TemporaryDirectory() as tmp:
            out_md = Path(tmp) / "checkliste.md"
            out_html = Path(tmp) / "checkliste.html"
            rc = main(
                [
                    "checkliste",
                    "--kategorien", str(KATEGORIEN_BEISPIEL),
                    "--praxis", DEMO_PRAXIS,
                    "--rolle", DEMO_ROLLEN[0],
                    "--rolle", DEMO_ROLLEN[1],
                    "--out-md", str(out_md),
                    "--out-html", str(out_html),
                ]
            )
            self.assertEqual(rc, 0)
            self.assertEqual(out_md.read_text(encoding="utf-8"), referenz_md)
            self.assertEqual(out_html.read_text(encoding="utf-8"), referenz_html)

    def test_tracker_byte_identisch_zur_demo(self) -> None:
        referenz_md = (AUDIT_DEMO / "status_report.md").read_text(encoding="utf-8")
        referenz_html = (AUDIT_DEMO / "status_report.html").read_text(encoding="utf-8")
        with TemporaryDirectory() as tmp:
            out_md = Path(tmp) / "report.md"
            out_html = Path(tmp) / "report.html"
            rc = main(
                [
                    "tracker",
                    "--csv", str(AUDIT_DEMO / "tracker_fixture.csv"),
                    "--praxis", DEMO_PRAXIS,
                    "--stichtag", "2026-07-25",
                    "--out-md", str(out_md),
                    "--out-html", str(out_html),
                ]
            )
            self.assertEqual(rc, 0)
            self.assertEqual(out_md.read_text(encoding="utf-8"), referenz_md)
            self.assertEqual(out_html.read_text(encoding="utf-8"), referenz_html)

    def test_kommentare_byte_identisch_zur_demo(self) -> None:
        referenz = (DOCX_DEMO / "auswertung.md").read_text(encoding="utf-8")
        with TemporaryDirectory() as tmp:
            out_md = Path(tmp) / "auswertung.md"
            rc = main(
                [
                    "kommentare",
                    str(DOCX_DEMO / "fixture_qm_kommentare.docx"),
                    str(out_md),
                ]
            )
            self.assertEqual(rc, 0)
            self.assertEqual(out_md.read_text(encoding="utf-8"), referenz)


class TestCliFehlerwege(unittest.TestCase):
    def test_fachfehler_ergibt_exit_1(self) -> None:
        with TemporaryDirectory() as tmp:
            rc = main(
                [
                    "checkliste",
                    "--kategorien", str(Path(tmp) / "fehlt.md"),
                    "--praxis", "Testpraxis",
                    "--out-md", str(Path(tmp) / "out.md"),
                ]
            )
            self.assertEqual(rc, 1)

    def test_ungueltiger_stichtag_ergibt_exit_1(self) -> None:
        with TemporaryDirectory() as tmp:
            rc = main(
                [
                    "tracker",
                    "--csv", str(AUDIT_DEMO / "tracker_fixture.csv"),
                    "--praxis", "Testpraxis",
                    "--stichtag", "25.07.2026",
                    "--out-md", str(Path(tmp) / "out.md"),
                ]
            )
            self.assertEqual(rc, 1)


if __name__ == "__main__":
    unittest.main()
