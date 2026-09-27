# Tooling-Integration — wie ein Tenant Werkzeuge anbindet

> Dieses Repo enthält Regelwerk, Vorlagen und freie Demos.
> Produktives proprietäres Tooling ist nicht enthalten.
> Tenants haben drei Optionen.

## Option 1: Sanexio-Tooling lizenzieren (empfohlen, wenn Sanexio-Tenant)

Wer Sanexio-Tenant ist (eine Praxis im Sanexio-Distributionsnetzwerk),
bekommt das Sanexio-QM-Tooling-Bundle als Teil des Tenant-Pakets. Das
Bundle läuft lokal in der Praxis und
besteht aus:

- **DOCX-Bearbeitungs-Toolkit** — unpack/edit/repack-Workflow für
  Word-Kommentar-Pflege (R-002) ohne Format-Verlust
- **PDF-OCR-Pipeline** — Tesseract-basierte Textextraktion für
  gescannte Referenzdokumente (Lieferanten-Hygieneleitfäden,
  IfSG-Behörden-Schreiben)
- **Audit-Checklisten-Automation** — Begehungs-Tracker, der die
  Praxisbegehungs-Checkliste in einen Hot-/Warm-/Cold-Status-Report
  überführt
- **STK-Termin-Reminder** — automatische Erinnerung 90/30/7 Tage vor
  dem nächsten STK-Termin pro Medizinprodukt
- **Versionsnummer-Konsistenz-Check** — prüft alle Dokumente in
  `01_Dokumente/` auf R-001-Konformität (Version, Datum, Freigabe)

Aufruf-Schema (geplant, Phase 3 der Cortex-Plattform-Roadmap):

```bash
# Tooling über Cortex-CLI ansprechen
cortex qm audit --workspace ./
cortex qm version-check ./01_Dokumente/
cortex qm stk-reminder --geraete ./rules/GERAETE_TENANT.md
```

Lieferumfang dieses Repos: Regelwerk, Strukturvorlagen und ausführbare
Demos unter `examples/`. Die oben gezeigten CLI-Befehle sind ein geplantes
Schnittstellenschema, keine hier ausgelieferten Befehle. Der manuelle
DOCX-Workflow kann über Microsoft Word / LibreOffice / Pages erfolgen.

## Option 2: Eigenes Tooling bauen nach diesem Regelwerk

Wer keinen Sanexio-Vertrag hat, kann eigenes Tooling implementieren.
Das Regelwerk in `rules/` ist die normative Spezifikation. Empfohlener
Stack:

| Schicht | Library/Tool | Zweck |
|---|---|---|
| DOCX-Lese-/Schreibzugriff | `python-docx` | Word-Kommentare, Header/Footer, Versionsnummer |
| DOCX-XML-Direkt | `zipfile` + `xml.etree.ElementTree` | tieferer Eingriff (Comments-XML, Styles) |
| PDF-Textextraktion (nativ) | `pdfplumber` oder `PyMuPDF` | Lieferanten-PDFs auslesen |
| OCR-Fallback | `tesseract` + `pytesseract` | gescannte Referenzdokumente |
| Bildverarbeitung für OCR | `Pillow` | Pre-Processing |
| Tabellen-Analyse | `pandas` + `openpyxl` | STK-Terminpläne, Bestandsverzeichnisse |
| Sprache | Python ≥3.11 oder vergleichbar | Konsistenz mit allgemeinem Cortex-Stack |

Architektur-Skelett (Pseudo-Code für ein typisches QM-Wartungs-Tool):

```python
from pathlib import Path
import docx
import datetime

def audit_versionierung(workspace: Path):
    """R-001: jedes Dokument in 01_Dokumente/ braucht Version + Datum + Freigabe."""
    findings = []
    for docx_path in (workspace / "01_Dokumente").glob("*.docx"):
        doc = docx.Document(docx_path)
        header_text = "\n".join(p.text for p in doc.paragraphs[:10])
        if not has_version_marker(header_text):
            findings.append((docx_path, "R-001: Versionsnummer fehlt"))
        if not has_freigabe_marker(header_text):
            findings.append((docx_path, "R-001: Freigabe-Unterschrift fehlt"))
        if version_older_than_1_year(header_text):
            findings.append((docx_path, "R-007: Review überfällig"))
    return findings

def audit_kommentare(workspace: Path):
    """R-002: offene Kommentare des Autors 'QM-System' sind unfertige
    Arbeitsanweisungen — vor Freigabe leer."""
    findings = []
    for docx_path in (workspace / "01_Dokumente").glob("*.docx"):
        offene = count_qm_system_comments(docx_path)
        if offene > 0:
            findings.append((docx_path, f"R-002: {offene} offene QM-System-Kommentare"))
    return findings

def audit_stk(geraete_file: Path):
    """STK-Termine prüfen: nächste fällige Termine in 90 Tagen?"""
    today = datetime.date.today()
    geraete = parse_geraete_markdown(geraete_file)
    upcoming = []
    for g in geraete:
        days = (g.naechste_stk - today).days
        if 0 <= days <= 90:
            upcoming.append((g.kennung, g.naechste_stk, days))
    return upcoming
```

## Option 3: Manuelles Verfahren ohne Tooling

Wer eine kleine Praxis ohne Tooling-Bedarf führt, kann das Regelwerk
auch vollständig manuell anwenden:

- Word/LibreOffice/Pages für DOCX-Bearbeitung mit Kommentar-Funktion
- Tabellenkalkulation (Excel/Numbers/Calc) für STK-Termin-Übersicht
  und Bestandsverzeichnisse
- Kalender-App für jährlichen Review-Zyklus (R-007 Q1-Q4)
- E-Mail / Schwarzes Brett für Team-Kommunikation nach Workflow-1-
  Nachbereitung

In dem Fall ist dieses Repo hauptsächlich eine Wissens-Quelle und
ein Audit-Selbst-Check (Checklisten in `rules/WORKFLOW.md` ausdrucken
und abhaken).

## Sanexio-Tooling-Lizenzierung (optional)

Wenn Tenants das Sanexio-Tooling-Bundle als Teil ihrer Plattform-
Anbindung nutzen wollen, gilt der Standard-Sanexio-Tenant-Vertrag.
Für Open-Source-Implementierungen ist dieses Regelwerk **frei nutzbar
unter Apache 2.0**.

Sanexio garantiert nicht, dass das eigene Tooling in jeder Praxis-
Umgebung lauffähig ist — das ist Teil des Tenant-Vertrags. Wer auf
sich selbst gestellt eigenes Tooling bauen will, hat hier die normative
Spec — das genügt für eine eigene robuste Implementierung.

## Schnittstellen zu anderen Cortex-Layer-Repos

- **cortex-rename** — wenn das QM-System eingehende Lieferanten-PDFs
  (z.B. Hygieneleitfäden) systematisch ablegen will, kann
  `cortex-rename` als Vor-Sortier-Schritt die Dateinamenskonvention
  vereinheitlichen, bevor die PDFs in `02_Vorlagen_und_Anlagen/` landen.
- **cortex-desk** — wenn Praxis-Eingangs-Dokumente per Mail/Fax/Post
  in einen zentralen Posteingang fließen, kann `cortex-desk` die
  Erst-Klassifikation übernehmen und QM-relevante Posten direkt in
  den passenden Themen-Ordner routen.
- **Praxiswebseiten-Theme** — wenn die Praxis-Webseite Patient-
  Informationen aus QM-Dokumenten ableitet (z.B. Datenschutz-Hinweise
  Themen 06), sollte die Web-Anzeige IMMER nur den freigegebenen
  Original-Stand aus `01_Dokumente/` zeigen, nie eine Bearbeitungs-
  Version aus `03_Arbeitsdateien/`.
