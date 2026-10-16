"""Kernlogik: Status-Normalisierung und CSV-Einlesen des Trackers."""

from __future__ import annotations

import unittest
from datetime import date
from pathlib import Path
from tempfile import TemporaryDirectory

from cortex_qm import CortexQmFehler
from cortex_qm.tracker import lese_zeilen, status_normalisieren

from .pfade import AUDIT_DEMO

STICHTAG = date(2026, 7, 25)


class TestStatusNormalisieren(unittest.TestCase):
    def test_erledigt_gewinnt_auch_ueberfaellig(self) -> None:
        self.assertEqual(
            status_normalisieren("erledigt", date(2026, 1, 1), STICHTAG), "erledigt"
        )

    def test_erledigt_ist_case_insensitiv(self) -> None:
        self.assertEqual(
            status_normalisieren("  Erledigt ", date(2026, 1, 1), STICHTAG), "erledigt"
        )

    def test_faellig_vor_stichtag_ist_ueberfaellig(self) -> None:
        self.assertEqual(
            status_normalisieren("offen", date(2026, 7, 24), STICHTAG), "ueberfaellig"
        )

    def test_faellig_am_stichtag_ist_offen(self) -> None:
        # Grenzfall: Faelligkeit genau am Stichtag gilt noch als offen.
        self.assertEqual(status_normalisieren("offen", STICHTAG, STICHTAG), "offen")

    def test_unbekannter_status_wird_nach_datum_bewertet(self) -> None:
        self.assertEqual(
            status_normalisieren("in arbeit", date(2026, 8, 1), STICHTAG), "offen"
        )
        self.assertEqual(
            status_normalisieren("in arbeit", date(2026, 7, 1), STICHTAG), "ueberfaellig"
        )


class TestLeseZeilenFixture(unittest.TestCase):
    """Gegen die mitgelieferte Demo-Fixture (nur lesend)."""

    def test_fixture_zaehlt_wie_der_committete_report(self) -> None:
        zeilen = lese_zeilen(AUDIT_DEMO / "tracker_fixture.csv", STICHTAG)
        status = [z["status_report"] for z in zeilen]
        self.assertEqual(len(zeilen), 4)
        self.assertEqual(status.count("erledigt"), 1)
        self.assertEqual(status.count("offen"), 1)
        self.assertEqual(status.count("ueberfaellig"), 2)


class TestLeseZeilenFehler(unittest.TestCase):
    def test_fehlende_datei(self) -> None:
        with self.assertRaises(CortexQmFehler):
            lese_zeilen(Path("/nirgendwo/tracker.csv"), STICHTAG)

    def test_fehlende_pflichtspalte(self) -> None:
        with TemporaryDirectory() as tmp:
            pfad = Path(tmp) / "kaputt.csv"
            pfad.write_text("id,status\nCHK-01-01,offen\n", encoding="utf-8")
            with self.assertRaises(CortexQmFehler) as ctx:
                lese_zeilen(pfad, STICHTAG)
            self.assertIn("faellig_am", str(ctx.exception))

    def test_ungueltiges_datum_nennt_zeile(self) -> None:
        with TemporaryDirectory() as tmp:
            pfad = Path(tmp) / "datum.csv"
            pfad.write_text(
                "id,fundstelle,pruefpunkt,status,faellig_am,verantwortung,bemerkung\n"
                "CHK-01-01,T01,Punkt,offen,25.07.2026,Rolle,\n",
                encoding="utf-8",
            )
            with self.assertRaises(CortexQmFehler) as ctx:
                lese_zeilen(pfad, STICHTAG)
            self.assertIn("CHK-01-01", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
