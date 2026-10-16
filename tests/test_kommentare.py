"""Kernlogik: DOCX-Kommentar-Auswertung."""

from __future__ import annotations

import unittest
import zipfile
from pathlib import Path
from tempfile import TemporaryDirectory

from cortex_qm import CortexQmFehler
from cortex_qm.kommentare import KEINE_FUNDSTELLE, auswerten, massnahme_ableiten

from .pfade import DOCX_DEMO

FIXTURE = DOCX_DEMO / "fixture_qm_kommentare.docx"


class TestAuswertenFixture(unittest.TestCase):
    """Gegen die mitgelieferte Demo-DOCX (nur lesend)."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.zeilen = auswerten(FIXTURE)

    def test_drei_kommentare_in_id_reihenfolge(self) -> None:
        self.assertEqual(len(self.zeilen), 3)
        fundstellen = [zeile[0] for zeile in self.zeilen]
        self.assertEqual(fundstellen[0], "Versionsnummer: v1.0")
        self.assertNotIn(KEINE_FUNDSTELLE, fundstellen)

    def test_massnahmen_zugeordnet(self) -> None:
        massnahmen = [zeile[2] for zeile in self.zeilen]
        self.assertIn(
            "R-001 pruefen: Version, Review-Datum und Freigabe dokumentieren.",
            massnahmen,
        )


class TestMassnahmeAbleiten(unittest.TestCase):
    def test_r001_zweig(self) -> None:
        self.assertTrue(massnahme_ableiten("Freigabe fehlt").startswith("R-001"))

    def test_themenordner_01_zweig(self) -> None:
        self.assertIn("Themenordner 01", massnahme_ableiten("R&D-Plan verweisen"))

    def test_themenordner_10_zweig(self) -> None:
        self.assertIn("Themenordner 10", massnahme_ableiten("Geraetedaten abgleichen"))

    def test_default_zweig(self) -> None:
        self.assertIn("Arbeitsauftrag", massnahme_ableiten("Bitte Tippfehler korrigieren"))


class TestFehlerfaelle(unittest.TestCase):
    def test_fehlende_datei(self) -> None:
        with self.assertRaises(CortexQmFehler):
            auswerten(Path("/nirgendwo/datei.docx"))

    def test_docx_ohne_kommentare(self) -> None:
        with TemporaryDirectory() as tmp:
            pfad = Path(tmp) / "ohne.docx"
            with zipfile.ZipFile(pfad, "w") as docx:
                docx.writestr("word/document.xml", "<w:document/>")
            with self.assertRaises(CortexQmFehler) as ctx:
                auswerten(pfad)
            self.assertIn("comments.xml", str(ctx.exception))

    def test_keine_zip_datei(self) -> None:
        with TemporaryDirectory() as tmp:
            pfad = Path(tmp) / "kaputt.docx"
            pfad.write_text("kein zip", encoding="utf-8")
            with self.assertRaises(CortexQmFehler):
                auswerten(pfad)


if __name__ == "__main__":
    unittest.main()
