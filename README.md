# cortex-qm — Regelwerk für Qualitätsmanagement in der Arztpraxis

> **Cortex-Layer-Projekt** in einem Plattform-Modell (Aware-Health-/Aniva-
> Style): generisches Regelwerk für das Qualitätsmanagement-System
> einer ambulanten Arztpraxis (G-BA QM-Richtlinie, QEP, IfSG, MPDG,
> MPBetreibV, EU-MDR, KRINKO, ArbSchG, DSGVO).
>
> **Stand 2026-09-26:** Generisches Regelwerk, Demos und öffentliche
> Phase-B-Strukturvorlagen vorhanden. Public-Freigabe bleibt ein separater
> Schritt (siehe `OSS_PREP.md`).

## Phase-B-Vorlagen (2026-09-26)

Die öffentlichen Schablonen sind in [Umfang und Nutzung](docs/PHASE_B_VORLAGEN.md)
beschrieben und im [Vorlagenmanifest](docs/vorlagen-manifest.json) erfasst.
Sie enthalten ausschließlich Platzhalter; befüllte Kopien bleiben im privaten Tenant.

## Was ist hier drin

- **`rules/`** — kuratiertes Regelwerk (Versionierung, Sprache, Word-
  Kommentare als Arbeitsanweisungen, Datums-Konventionen, jährlicher
  Review-Zyklus), Ordner-Schema (12 Themenbereiche), Workflow-Skelette
  (Dokument bearbeiten · neue SOP · jährliche Überprüfung) und
  Beispiel-Katalog für jede der 12 Themen-Kategorien.
- **`docs/ENGINE_INTEGRATION.md`** — wie Tenants ein DOCX/PDF/OCR-
  Tooling anbinden.
- **`OSS_PREP.md`** — öffentlicher Lieferumfang und Freigabegrenzen.

## Was hier explizit NICHT drin ist

- **Konkrete Praxis-Inhalte** (Personal-Namen, konkrete Räumlichkeiten,
  individuelle Gerätelisten, patientenbezogene Schulungsnachweise) —
  diese leben im jeweiligen Tenant-Repo (z.B. `<tenant-repo>/qm/`).
- **Fertige QM-Handbücher / Hygienepläne / SOPs einer einzelnen
  Praxis** — das Regelwerk hier sagt, **wie** ein QM-Dokument aufgebaut
  ist und welche Compliance-Anker es treffen muss, nicht **welche
  konkreten Texte** in einer einzelnen Praxis stehen.
- **Produktives proprietäres Tooling** (Python-Module für DOCX-Unpack/Repack, PDF-OCR-
  Extraktion, automatisierte Begehungs-Audits) — bleibt in einem
  proprietären Engine-Bereich (in Vorbereitung). Andere
  Tenants haben zwei Optionen:
  1. **Eigenes Tooling bauen** nach diesem Regelwerk (Open-Source-
     Distribution).
  2. **Proprietäres Tooling lizenzieren** als Teil eines Tenant-
     Pakets.
- **Patientendaten in jeglicher Form** — gehören niemals in ein QM-
  Dokument (siehe `rules/CORE_RULES.md` R-007 + DSGVO).

Regelwerk und Demos sind öffentlich nutzbare Bausteine; ausgefüllte
Praxisdokumente bleiben privat. Die eigenständigen
[Integrationshinweise](docs/ENGINE_INTEGRATION.md) beschreiben die Schnittstelle.

## Regulatorische Basis (Auszug aus `rules/CORE_RULES.md`)

Das Regelwerk verankert in:

- **G-BA QM-Richtlinie** — Qualitätsmanagement vertragsärztliche Versorgung
- **QEP-System** — Qualität und Entwicklung in Praxen (KBV)
- **IfSG** — Infektionsschutzgesetz (Hygieneplan, Meldepflichten)
- **MPDG / MPBetreibV** — Medizinproduktebuch, STK, Einweisungen
- **EU-MDR 2017/745** — Klassifikation, Konformitätsbewertung
- **KRINKO / BfArM** — Aufbereitung von Medizinprodukten
- **ArbSchG / ArbStättV / BioStoffV** — Arbeitssicherheit, Gefährdungs-
  beurteilung
- **DSGVO / BDSG** — Datenschutz, Aufbewahrungsfristen
- **Länder-Hygiene-Verordnungen** (länderspezifisch — siehe
  Tenant-Inhalte)

## Ordner-Schema (Auszug aus `rules/SCHEMA.md`)

Eine Praxis-QM-Arbeitsumgebung gliedert sich in drei Top-Level-Ebenen:

```
01_Dokumente/                       ← Hauptdokumente (Originale + datierte Bearbeitungsversionen)
02_Vorlagen_und_Anlagen/            ← Themen-Bibliothek (01-12 thematisch geordnet)
03_Arbeitsdateien/                  ← MFA-Bearbeitungen + Analysen (Datums-Subfolder YYMMDD)
```

Die 12 Themen-Kategorien (`02_Vorlagen_und_Anlagen/01..12`):

```
01 Hygiene_Desinfektion          07 Qualitaets_und_Risikomanagement
02 Infektionsschutz_Meldewesen   08 Personal_Organisation
03 Notfallmanagement             09 Arbeitsschutz_Brandschutz
04 Patientenversorgung_Diagnostik 10 Medizinprodukte_STK
05 Terminmanagement_eRezept      11 OP_Eingriffe_SSI
06 Datenschutz_Aufbewahrung      12 Abfallentsorgung
```

Erweiterung durch nächste freie Ziffer (13, 14, …) ohne Bruch.
Bearbeitungs-Subfolder im Datumsformat `YYMMDD` (z.B. `260429/`).

## Quickstart für andere Praxen

```bash
# 1. Repo klonen
git clone https://github.com/Sanexio/cortex-qm.git
cd cortex-qm

# 2. Tenant-eigene Inhalte anlegen (gitignored, sicher gegen
#    versehentliches Commit ins OSS-Repo)
cp rules/PERSONAL_EXAMPLE.md      rules/PERSONAL_TENANT.md
cp rules/GERAETE_EXAMPLE.md       rules/GERAETE_TENANT.md
cp rules/RAEUMLICHKEITEN_EXAMPLE.md rules/RAEUMLICHKEITEN_TENANT.md
nano rules/PERSONAL_TENANT.md       # eigenes Team eintragen
nano rules/GERAETE_TENANT.md        # eigene Medizinprodukte eintragen
nano rules/RAEUMLICHKEITEN_TENANT.md # eigene Praxis-Räume eintragen

# 3. Arbeitsumgebung initialisieren
mkdir -p 01_Dokumente 02_Vorlagen_und_Anlagen 03_Arbeitsdateien
# Öffentliche Strukturvorlagen aus dokumente/ und arbeitsdateien/
# in einen privaten Arbeitsbereich kopieren und dort ausarbeiten
# (siehe docs/PHASE_B_VORLAGEN.md und rules/WORKFLOW.md).

# 4. Tooling-Optionen — siehe docs/ENGINE_INTEGRATION.md
#    (DOCX-Bearbeitung, PDF-OCR für gescannte Referenzdokumente,
#    Begehungs-Checklisten-Automation)
```

## Beitrags-Modell

Pull-Requests willkommen. Bevor du eine PR aufmachst:

- README + `docs/ENGINE_INTEGRATION.md` lesen
- Schema-Erweiterungen (neue Themen-Kategorie ≥13, neue Kern-Regel,
  Anpassung am Datums-Format) bitte zuerst als Issue diskutieren
- Tenant-spezifische Inhalte (Personal, konkrete Geräte, konkrete
  Räumlichkeiten, individuelle Hygienepläne) sind **nicht** Teil
  dieses Repos (siehe oben „Was hier explizit NICHT drin ist")
- Patienten- oder mitarbeiterbezogene Daten in PRs werden ohne
  Diskussion zurückgewiesen.

Maintenance: Projekt-Maintainer — 2-Personen-Approval bei PRs
mit Schema-Impact.

## Querverweise

- Sister-Repos im Cortex Layer (in Vorbereitung): `cortex-desk`,
  `cortex-rename`, ein generisches Praxiswebseiten-Theme.

## Lizenz

Regelwerk, Vorlagen, Demos und Hilfsskripte dieses Repos stehen unter der
Apache License 2.0 — siehe [LICENSE](LICENSE) und [NOTICE](NOTICE).
Optionale proprietäre Engines sind nicht Bestandteil dieser Lizenzierung.
