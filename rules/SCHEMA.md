# Ordner-Schema — kanonischer Aufbau einer Praxis-QM-Arbeitsumgebung

## Top-Level-Ebene

```
01_Dokumente/                       ← Hauptdokumente (Originale + datierte Bearbeitungsversionen)
02_Vorlagen_und_Anlagen/            ← Themen-Bibliothek (01-12 thematisch geordnet)
03_Arbeitsdateien/                  ← MFA-Bearbeitungen + Analysen (Datums-Subfolder YYMMDD)
_config/                            ← projektlokale Regeln, Workflows, Fehlerprotokoll
```

| Ebene | Inhalt | Versionierung |
|---|---|---|
| `01_Dokumente/` | offizielle, vom Praxisinhaber freigegebene QM-Dokumente | Original auf erster Ebene; aktuelle Bearbeitungs-Iteration als `YYMMDD/`-Subfolder mit `_BEARBEITET`-Suffix |
| `02_Vorlagen_und_Anlagen/` | Referenz-Vorlagen, Lieferanten-Material, generische Schablonen | thematisch in `01_..` bis `12_..` |
| `03_Arbeitsdateien/` | laufende MFA-Bearbeitungen, Analysen, Extraktionen | ausschließlich in `YYMMDD/`-Subfolder |
| `_config/` | Regeln, Workflows, projektlokales Fehlerprotokoll | unter Versionskontrolle |

## Datums-Subfolder-Konvention

Format: `YYMMDD` (6-stellig, Jahr-Monat-Tag, ohne Trenner).

Beispiele:
- `260429` → 29.04.2026
- `260601` → 01.06.2026
- `270115` → 15.01.2027

**Warum 6-stellig ohne Trenner**: sortiert lexikografisch identisch
zur chronologischen Reihenfolge, ist unauffällig in Tabellen und
übersteht 75 Jahre (bis 2100) Praxis-Betrieb ohne Format-Bruch.
Für Dokumente mit Aufbewahrungsfristen > 30 Jahre (z.B. Strahlen-
schutz: 30 Jahre nach letzter Aufzeichnung, Personalakten: 10 Jahre
nach Austritt) ist die Datierung primär über Dokument-Metadaten,
sekundär über den Subfolder geregelt.

## Die 12 Themen-Kategorien

Verbindlich nummeriert von `01` bis `12`. Erweiterung durch nächste
freie Ziffer (`13`, `14`, …) ohne Bruch der bestehenden Reihenfolge.

| Nr | Themenordner | Hauptinhalte |
|---|---|---|
| 01 | `Hygiene_Desinfektion` | Hygieneplan, Reinigungs- und Desinfektionsplan, Hautschutz- und Handschuhplan |
| 02 | `Infektionsschutz_Meldewesen` | MRE-Richtlinien, Influenza/COVID/virale Diarrhoe-Verfahrensanweisungen, IfSG-Meldepflichten |
| 03 | `Notfallmanagement` | Notfallplan, Notfall-Triagekriterien, Notfallausstattung, Reanimations-Checkliste |
| 04 | `Patientenversorgung_Diagnostik` | Anamnese-SOP, Blutentnahme-SOP, Impfung-SOP, Wundversorgung-SOP, weitere klinische SOPs |
| 05 | `Terminmanagement_eRezept` | Terminerinnerung, eRezept-Checkliste, Onlinesprechstunde-Workflow |
| 06 | `Datenschutz_Aufbewahrung` | DSGVO-Hinweise, Schweigepflichtsbelehrung, Aufbewahrungsfristen, Patient-Datenexport-Verfahren |
| 07 | `Qualitaets_und_Risikomanagement` | QM-Handbuch (QEP-strukturiert), Leitbild, Qualitätsziele, Risiko-/Fehlermanagement, Praxisbegehungs-Checkliste, Managementbewertung |
| 08 | `Personal_Organisation` | Organigramm, Aufgaben/Verantwortlichkeiten-Matrix, Kürzelliste, Delegation, Schulungsplan |
| 09 | `Arbeitsschutz_Brandschutz` | Gefährdungsbeurteilung, Verfahrensanweisung Spitze/scharfe Gegenstände, Brandschutzordnung, PEP-Verfahrensanweisung |
| 10 | `Medizinprodukte_STK` | Medizinproduktebuch, MP-Bestandsverzeichnis, Geräteeinweisungen, STK-Termine, Übergabeprotokolle |
| 11 | `OP_Eingriffe_SSI` | SSI-Risikoeinstufung, OP-Vorbereitungs-SOPs, sterile Aufbereitung, Eingriffsprotokolle |
| 12 | `Abfallentsorgung` | Abfallentsorgungs-Anlage, AS-Schlüssel-Zuordnung, Sammelbehälter-Konvention |

## Originale vs. Bearbeitungs-Versionen

```
01_Dokumente/
├── Hygieneplan.docx                       ← Original (vom Praxisinhaber freigegeben)
├── QM-Handbuch.docx                       ← Original
├── Medizinproduktebuch_und_STK.docx       ← Original
├── Aktionsplan_Praxisbegehung.docx        ← Original
└── 260429/                                 ← aktive Bearbeitungs-Iteration vom 29.04.2026
    ├── Hygieneplan_BEARBEITET.docx
    ├── QM-Handbuch_BEARBEITET.docx
    ├── Medizinproduktebuch_und_STK_BEARBEITET.docx
    ├── Aktionsplan_Praxisbegehung_BEARBEITET.docx
    ├── Arbeitsauftraege_MFA.docx
    └── README.md                           ← Iterations-Zusammenfassung
```

**Regel:** Solange in einer Iteration gearbeitet wird, bleibt der
Original-Stand auf erster Ebene unverändert. Erst nach Freigabe durch
den Praxisinhaber wird `_BEARBEITET` über den Original-Stand kopiert
(alte Version wandert nach `01_Dokumente/_archiv/` mit Datums-Suffix).

## Arbeitsdateien-Konvention

```
03_Arbeitsdateien/
├── 260414/
│   ├── HYGIENE_DOCUMENTS_ANALYSIS.txt
│   ├── EXTRACTION_SUMMARY.txt
│   ├── README_EXTRACTION.txt
│   └── COMPLETE_HYGIENE_EXTRACTION.txt
└── 260429/
    ├── Hygieneplan.docx                   ← MFA-Entwurf
    ├── QM-Handbuch-2.docx
    ├── Hautschutzplan_Praxis.docx
    ├── QC_Protokoll_POCT.docx
    ├── PEP_Verfahrensanweisung_NEU.docx
    └── …
```

Hier liegen alle laufenden MFA-Arbeitsstände, Analysen,
Text-Extraktionen aus Referenzmaterial. Niemals direkt unter
`01_Dokumente/` ablegen — nur freigegebene Endstände dort.

## Dateinamenskonvention

Siehe `CORE_RULES.md` R-005:

- Hauptdokumente in `01_Dokumente/` mit führendem `_` als Markierung
  des „offiziellen" Status sind möglich, aber nicht erzwungen.
- Bearbeitungs-Suffix `_BEARBEITET` nur in datiertem Subfolder, nicht
  auf erster Ebene.
- SOP-Format: `SOP_<Prozessname>_<YYYY-MM-DD>.docx` (z.B.
  `SOP_Blutentnahme_2026-04-13.docx`).
- STK-Protokolle: `STK_<Geraetekennung>_<YYYY-Q?>.docx` (z.B.
  `STK_Roentgen-1_2026-Q2.docx`).
- Vorlagen in `02_Vorlagen_und_Anlagen/` behalten oft die Lieferanten-
  oder Hersteller-Originalbenennung (PDF) — die Themen-Zuordnung
  passiert über den Subfolder, nicht über den Dateinamen.

## Erweiterung um eine 13. Themen-Kategorie

Wenn eine Praxis eine neue Themen-Kategorie aufnehmen will (z.B.
`13 Telemedizin_Videosprechstunde/`), gilt:

1. Nächste freie Ziffer (`13_`) verwenden.
2. Bestehende 01-12 NICHT umnummerieren (würde alle bestehenden
   Querverweise und MFA-Schulungsstände brechen).
3. Eintrag in `02_Vorlagen_und_Anlagen/README.md` (Tenant-File) mit
   Begründung, ab wann die neue Kategorie geführt wird.
4. Wenn die Kategorie ein generisches Thema betrifft, das auch andere
   Praxen brauchen → PR gegen `cortex-qm/rules/SCHEMA.md` und
   `rules/CATEGORIES_EXAMPLE.md`.

## Anti-Patterns

- ❌ Dokumente direkt in `02_Vorlagen_und_Anlagen/` ohne Themen-
  Subfolder ablegen — gehört in eine der `01..12`-Kategorien oder
  bekommt eine neue 13+ Kategorie.
- ❌ MFA-Arbeitsstände in `01_Dokumente/` ablegen — gehören in
  `03_Arbeitsdateien/YYMMDD/`.
- ❌ Bearbeitungs-Versionen ohne Datums-Subfolder direkt neben dem
  Original ablegen — bricht die Versions-Historie.
- ❌ Datums-Subfolder mit `YYYY-MM-DD` (mit Trennern) statt `YYMMDD`
  benennen — sortiert in mixed-folder-views inkonsistent.
- ❌ Patientennamen oder mitarbeiterbezogene Klartext-Daten in
  Dateinamen — DSGVO-Verstoß, siehe `CORE_RULES.md` R-007.
