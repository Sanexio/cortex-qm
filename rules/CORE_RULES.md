# Kern-Regeln R-001 bis R-007

> Generische Regeln für jedes Praxis-QM-System. Tenant-spezifische
> Inhalte (Personal-Liste, konkrete Geräte, konkrete Räumlichkeiten)
> gehören in die `*_TENANT.md`-Files (gitignored) bzw. ins jeweilige
> Tenant-Repo.

## Regulatorische Basis

Das Regelwerk verankert in:

- **G-BA QM-Richtlinie** (Qualitätsmanagement vertragsärztliche Versorgung)
- **QEP-System** (Qualität und Entwicklung in Praxen, KBV)
- **IfSG** (Infektionsschutzgesetz) — Hygieneplan, Meldepflichten
- **MPDG** (Medizinprodukterecht-Durchführungsgesetz) — Medizinproduktebuch
- **MPBetreibV** (Medizinprodukte-Betreiberverordnung) — STK, Einweisungen
- **EU-MDR 2017/745** — Klassifikation, Konformitätsbewertung
- **KRINKO/BfArM-Empfehlungen** — Aufbereitung Medizinprodukte
- **ArbSchG / ArbStättV / BioStoffV** — Arbeitssicherheit, Gefährdungsbeurteilung
- **DSGVO / BDSG** — Datenschutz, Aufbewahrungsfristen
- **Länderhygiene-Verordnungen** — länderspezifisch (siehe Tenant-Inhalte)

## R-001: Versionierung

Jedes QM-Dokument trägt **Versionsnummer, Erstelldatum, Freigabedatum
und Freigabe-Unterschrift des Praxisinhabers** (in der Regel ärztliche
Leitung).

- Versionsnummer im Format `vMAJOR.MINOR` (z.B. `v1.3`).
- Major-Sprung bei strukturellen Änderungen, Minor bei inhaltlichen
  Ergänzungen.
- **Mindestens jährliche Überprüfung** aller Dokumente (siehe R-007
  Review-Zyklus).
- Bei Gesetzes-Änderungen außerplanmäßiger Review.

Begründung: G-BA-QM-Richtlinie fordert nachweisbare Aktualität;
Aufsichtsbehörden prüfen primär Versionsdatum und Freigabe.

## R-002: Kommentare als Arbeitsanweisungen

Fehlende praxisspezifische Informationen werden als **Word-Kommentare**
mit Autor-Name **„QM-System"** eingetragen, nicht als Inline-
Platzhalter.

- Format: rechte Word-Kommentarspalte, Autor explizit auf `QM-System`
  gesetzt (nicht der jeweilige MFA-Benutzername).
- Kommentare gelten als **Arbeitsanweisungen an die MFA**: nach
  Abarbeitung sind sie zu löschen, nicht „resolved" zu setzen.
- Pendant in `03_Arbeitsdateien/YYMMDD/`: ein Übersichts-Markdown,
  das offene Kommentar-IDs auflistet.

Begründung: Word-Kommentare sind versions-sicher (bleiben in der
`.docx`-XML erhalten, auch bei Convert-Roundtrips über LibreOffice
oder Pages), Inline-Platzhalter wie `<FÜLLE-EIN>` werden in der Praxis
übersehen oder versehentlich finalisiert.

## R-003: Sprache und Ton

Alle Dokumente in **deutscher Fachsprache**, professioneller aber
verständlicher Ton.

- Zielgruppe: MFA-Team **und** Praxisleitung. Ein Dokument muss von
  einer MFA in der Erstbearbeitung verstanden werden, ohne dass die
  Praxisleitung jede Zeile nacherklären muss.
- Keine Anglizismen für Fachbegriffe mit deutscher Standard-Entsprechung
  („MFA" statt „Medical Assistant", „Praxisinhaber" statt „Owner").
- Bei behördlichen Pflicht-Begriffen (z.B. „SOP", „STK", „SSI") wird
  beim ersten Vorkommen die Langform in Klammern ergänzt.

## R-004: Keine Inline-Platzhalter

Informelle Marker wie `@FS:`, `<…>`, `[TODO]` sind durch **professionelle
Word-Kommentare (R-002)** zu ersetzen.

Begründung: Inline-Platzhalter erzeugen bei behördlichen Begehungen
einen Eindruck von Unfertigkeit, auch wenn das Dokument inhaltlich
vollständig ist. Word-Kommentare sind ein klar gekennzeichneter
Arbeitsraum, der vor Freigabe systematisch geleert wird.

## R-005: Dateinamenskonvention

- Hauptdokumente in `01_Dokumente/` können mit führendem `_` beginnen
  (`_QM-Handbuch.docx`), um den „offiziellen" Status zu signalisieren —
  nicht erzwungen.
- Vorlagen und Referenzmaterial liegen in `02_Vorlagen_und_Anlagen/`,
  thematisch in einer der 12 Kategorien (siehe `SCHEMA.md`).
- SOPs werden als `SOP_<Prozessname>_<YYYY-MM-DD>.docx` benannt
  (z.B. `SOP_Blutentnahme_2026-04-13.docx`).
- STK-Protokolle als `STK_<Geraetekennung>_<YYYY-Q?>.docx`
  (z.B. `STK_Roentgen-1_2026-Q2.docx`).
- Bearbeitungs-Versionen ausschließlich in `YYMMDD/`-Subfolder mit
  `_BEARBEITET`-Suffix.
- Keine Patientendaten, keine Mitarbeiter-Klarnamen, keine konkreten
  Patientenfall-Identifier in Dateinamen.

## R-006: Tooling (DOCX-Bearbeitung)

Word-Dokumente werden über den **unpack → edit XML → repack**-Workflow
bearbeitet, wenn programmatische Bearbeitung nötig ist (z.B. Massen-
Kommentar-Pflege, automatisierte Versionsnummer-Inkrementierung,
batch-Header-Update).

- Tooling lebt **außerhalb dieses Repos** (siehe
  `docs/ENGINE_INTEGRATION.md`). Empfohlene Stacks: `python-docx`
  (Python) oder direkter XML-Zugriff auf `word/document.xml` und
  `word/comments.xml` in der entpackten `.docx`.
- Manuelle Bearbeitung in Word/LibreOffice/Pages bleibt der Default
  für die MFA — Tooling ist Bulk- und Konsistenz-Werkzeug.

## R-007: Jährlicher Review-Zyklus

Reviews sind über das Jahr verteilt, um Spitzenlasten zu vermeiden
und sicherzustellen, dass jedes Dokument mindestens einmal pro Jahr
geprüft wird (R-001).

| Quartal | Dokumente |
|---|---|
| **Q1 (Januar)** | QM-Handbuch + Qualitätsziele |
| **Q2 (April)** | Hygieneplan + R&D-Plan |
| **Q3 (Juli)** | Medizinproduktebuch + STK-Termine |
| **Q4 (Oktober)** | SOPs + Schulungsnachweise |

Außerplanmäßiger Review wird ausgelöst durch:

- Gesetzes- oder Richtlinien-Änderung (z.B. IfSG-Update, neue
  KRINKO-Empfehlung, neue G-BA QM-Richtlinie)
- Begehungs-Befund mit Mangel-Vermerk
- internes Fehler-Ereignis aus dem Fehlerprotokoll
  (`FEHLERPROTOKOLL_TENANT.md`)
- Inbetriebnahme eines neuen Medizinprodukts (STK-Erst-Eintrag,
  Geräteeinweisung)

## DSGVO-Hardstop: Patientendaten

**Patientendaten haben in QM-Dokumenten nichts zu suchen.** Konkret:

- Keine Patientennamen, keine Geburtsdaten, keine Adressen
- Keine konkreten Behandlungsfälle mit Identifikations-Möglichkeit
- Statistiken sind erlaubt, sofern sie aggregiert sind und keinen
  Rückschluss auf einen Einzelfall erlauben (Mindestanzahl pro
  Aggregat-Bucket je nach Praxisgröße; Faustregel: keine Buckets mit
  n < 5 in regionalen Kontexten).
- Schulungsnachweise enthalten ausschließlich Mitarbeiternamen und
  Schulungs-Titel, keine konkreten Patientenbezüge.

Verstöße werden NICHT durch nachträgliche Anonymisierung „repariert"
— sondern führen zu Dokument-Neuauflage und einem Eintrag im
Fehlerprotokoll mit DSGVO-Verstoß-Klassifikation.

Aufbewahrungsfristen (siehe `02_Vorlagen_und_Anlagen/06`):
- QM-Dokumente: 10 Jahre nach Außerkraftsetzung
- Schulungsnachweise: 5 Jahre
- Strahlenschutz-Aufzeichnungen: 30 Jahre nach letzter Eintragung
- Personalakten: 10 Jahre nach Austritt
