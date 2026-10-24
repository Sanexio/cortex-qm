"""Marketplace-Manifest gegen das angeheftete Katalogschema pruefen.

Hintergrund und die eine bewusst gelockerte Stelle stehen in
``marketplace/schema/README.md``. Kurzfassung:

* ``marketplace/app.json`` ist das Manifest **einer** App.
* ``marketplace/schema/manifest.schema.json`` (Kopie aus
  ``Sanexio/praxiszentrum-theme``) beschreibt den **Katalog** des
  Storefront-Moduls: ``manifest_version`` / ``store`` / ``apps[]``.

Beides sind verschiedene Dokumentarten. Geprueft wird deshalb die
**Katalogprojektion**: der Eintrag, den das Storefront aus ``app.json``
in ``apps[]`` aufnehmen wuerde, gegen ``#/$defs/app`` — mit echtem
Validator, nicht mit nachgebauten Feldpruefungen.

Benoetigt ``jsonschema`` (Test-Extra, keine Laufzeit-Abhaengigkeit):
``pip install -e .[test]``. Der Import ist bewusst hart — ein
uebersprungener Test waere ein gruener Test, der nichts belegt.
"""

from __future__ import annotations

import copy
import hashlib
import json
import unittest

from jsonschema import Draft202012Validator

from .pfade import REPO

MARKETPLACE = REPO / "marketplace"
APP_JSON = MARKETPLACE / "app.json"
SCHEMA_DATEI = MARKETPLACE / "schema" / "manifest.schema.json"
HERKUNFT_DATEI = MARKETPLACE / "schema" / "HERKUNFT.json"

TAURI_CONF = REPO / "app" / "src-tauri" / "tauri.conf.json"
PACKAGE_JSON = REPO / "app" / "package.json"

# Pflichtfelder aus #/$defs/app, die sich aus app.json (noch) nicht
# ableiten lassen. Fuer `downloads` braucht es HTTPS-Paket-URLs eines
# oeffentlichen Release; cortex-qm hat keinen (docs/EINZELAPP_20261022.md,
# "BA2 Release-Haertung"). URLs werden nicht erfunden.
NOCH_NICHT_ABLEITBAR = frozenset({"downloads"})


def _lies(pfad):
    return json.loads(pfad.read_text(encoding="utf-8"))


def katalogprojektion(app_manifest):
    """Den Katalogeintrag bauen, den das Storefront aus app.json ableitet.

    Nur Felder, die ``app.json`` tatsaechlich traegt. Nichts wird
    erfunden, nichts mit Platzhaltern aufgefuellt.
    """
    eintrag = {
        "id": app_manifest["id"],
        "name": app_manifest["name"],
        "summary": app_manifest["kurzbeschreibung"],
        "version": app_manifest["version"],
    }
    symbol = app_manifest.get("symbol")
    if symbol:
        eintrag["icon"] = symbol
    feed = (app_manifest.get("update_feed") or {}).get("url") or app_manifest.get(
        "update_kanal"
    )
    if feed:
        eintrag["update_feed"] = feed
    return eintrag


def _app_teilschema(schema, ohne_pflicht):
    """``#/$defs/app`` als eigenstaendiges Schema, Pflichtliste gelockert."""
    teil = copy.deepcopy(schema["$defs"]["app"])
    teil["required"] = [f for f in teil["required"] if f not in ohne_pflicht]
    # ``$ref: "#/$defs/download"`` muss weiter aufloesen.
    teil["$defs"] = copy.deepcopy(schema["$defs"])
    return teil


class TestSchemaVerankerung(unittest.TestCase):
    """Die Kopie muss die angeheftete Revision sein, nicht irgendeine."""

    def test_kopie_entspricht_der_angehefteten_revision(self) -> None:
        herkunft = _lies(HERKUNFT_DATEI)
        rohdaten = SCHEMA_DATEI.read_bytes()
        self.assertEqual(
            hashlib.sha256(rohdaten).hexdigest(),
            herkunft["sha256"],
            "Schema-Kopie weicht von der in HERKUNFT.json angehefteten "
            "Revision ab — Kopie und Herkunftsangabe gemeinsam nachziehen.",
        )
        self.assertEqual(len(rohdaten), herkunft["groesse_bytes"])

    def test_herkunft_benennt_quelle_vollstaendig(self) -> None:
        herkunft = _lies(HERKUNFT_DATEI)
        self.assertEqual(herkunft["herkunft_repository"], "Sanexio/praxiszentrum-theme")
        self.assertEqual(
            herkunft["herkunft_pfad"], "inc/marketplace/schema/manifest.schema.json"
        )
        for feld in ("herkunft_commit", "herkunft_git_blob"):
            wert = herkunft[feld]
            self.assertRegex(wert, r"^[0-9a-f]{40}$", f"{feld} muss volle Commit-/Blob-ID sein")

    def test_schema_ist_gueltiges_json_schema(self) -> None:
        Draft202012Validator.check_schema(_lies(SCHEMA_DATEI))


class TestKatalogprojektion(unittest.TestCase):
    """app.json gegen das Katalogschema — ueber die Projektion."""

    def setUp(self) -> None:
        self.schema = _lies(SCHEMA_DATEI)
        self.app_manifest = _lies(APP_JSON)
        self.eintrag = katalogprojektion(self.app_manifest)

    def test_projektion_erfuellt_app_teilschema(self) -> None:
        validator = Draft202012Validator(
            _app_teilschema(self.schema, NOCH_NICHT_ABLEITBAR)
        )
        fehler = sorted(validator.iter_errors(self.eintrag), key=lambda e: list(e.path))
        self.assertEqual(
            [],
            [f"{list(e.path) or ['<wurzel>']}: {e.message}" for e in fehler],
            "Katalogprojektion aus marketplace/app.json verletzt das Schema.",
        )

    def test_luecke_ist_genau_benannt(self) -> None:
        """Die Lockerung darf nicht stillschweigend wachsen.

        Faellt ein weiteres Pflichtfeld weg oder liefert app.json
        eines Tages Download-URLs, muss dieser Test rot werden.
        """
        pflicht = set(self.schema["$defs"]["app"]["required"])
        fehlend = pflicht - set(self.eintrag)
        self.assertEqual(
            set(NOCH_NICHT_ABLEITBAR),
            fehlend,
            "Die Menge der nicht ableitbaren Pflichtfelder hat sich geaendert — "
            "marketplace/schema/README.md und NOCH_NICHT_ABLEITBAR nachziehen.",
        )

    def test_keine_unbekannten_felder_in_der_projektion(self) -> None:
        erlaubt = set(self.schema["$defs"]["app"]["properties"])
        self.assertLessEqual(set(self.eintrag), erlaubt)

    def test_beispielkatalog_des_schemas_bleibt_gueltig(self) -> None:
        """Positivkontrolle gegen das volle Schema.

        Belegt, dass der Validator das Schema wirklich anwendet und
        nicht nur alles durchwinkt: ein Katalog mit der Projektion als
        einzigem Eintrag ist ohne `downloads` ungueltig.
        """
        katalog = {
            "manifest_version": 1,
            "store": {"name": "Cortex Marketplace"},
            "apps": [self.eintrag],
        }
        validator = Draft202012Validator(self.schema)
        self.assertTrue(
            list(validator.iter_errors(katalog)),
            "Ohne downloads muesste der volle Katalog ungueltig sein — "
            "tut er es nicht, prueft der Validator nichts.",
        )


class TestManifestKonsistenz(unittest.TestCase):
    """app.json, Tauri-Schale und Paket duerfen nicht auseinanderlaufen."""

    def setUp(self) -> None:
        self.app_manifest = _lies(APP_JSON)
        self.tauri = _lies(TAURI_CONF)
        self.package = _lies(PACKAGE_JSON)

    def test_version_ist_ueberall_gleich(self) -> None:
        self.assertEqual(self.app_manifest["version"], self.tauri["version"])
        self.assertEqual(self.app_manifest["version"], self.package["version"])

    def test_bundle_kennung_passt_zur_tauri_schale(self) -> None:
        self.assertEqual(self.app_manifest["bundle_id"], self.tauri["identifier"])

    def test_app_kennung_ist_in_sich_stimmig(self) -> None:
        kennung = self.app_manifest["id"]
        self.assertEqual(self.app_manifest["lizenz_app_kennung"], kennung)
        self.assertTrue(self.app_manifest["repository"].endswith("/" + kennung))

    def test_klasse_ist_k0(self) -> None:
        """K0 = Code/Betrieb. Eine App mit Patientenbezug gehoert hier nicht her."""
        self.assertEqual(self.app_manifest["klasse"], "K0")

    def test_symbole_liegen_neben_dem_manifest(self) -> None:
        for feld in ("symbol", "symbol_qr"):
            name = self.app_manifest.get(feld)
            if name:
                self.assertTrue(
                    (MARKETPLACE / name).is_file(), f"{feld}: {name} fehlt in marketplace/"
                )


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
