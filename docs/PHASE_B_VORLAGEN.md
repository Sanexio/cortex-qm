# Phase B — öffentliche Vorlagen

Stand: 2026-09-26. B.4/B.5 werden nach Nutzerentscheid als generische
Strukturvorlagen aus dem vorhandenen Regelwerk bereitgestellt. Die frühere
Anlieferung konkreter Praxisdateien ist dafür nicht erforderlich.
Dies bestätigt keine Migration privater Bestände und keine fachliche Freigabe.

## Umfang und Ableitung

| Phase | Dateien | Muster aus dem Bestand |
|---|---|---|
| B.4 | `dokumente/hygieneplan.md`, `qm-handbuch.md`, `medizinproduktebuch.md`, `aktionsplan.md` | OSS_PREP: vier Hauptdokumente; CORE_RULES R-001 bis R-007; WORKFLOW |
| B.4 | `dokumente/sop.md` | WORKFLOW 2: sieben SOP-Abschnitte |
| B.5 | `arbeitsdateien/kommentar-uebersicht.md` | R-002 und WORKFLOW 1 |
| B.5 | `arbeitsdateien/reviewprotokoll.md`, `schulungsnachweis.md` | WORKFLOW 2/3 und R-007 |

Das [Vorlagenmanifest](vorlagen-manifest.json) listet jeden tatsächlichen
Repo-Pfad einzeln. Das Paketmanifest bleibt unverändert: reines Regelpaket,
K1, phi=false, kein installierter Selbsttest.

## Verwendung im privaten Tenant

1. Gewünschte Schablone in einen privaten Arbeitsbereich kopieren.
2. `{{SLOT_NAME}}` bezeichnet ausschließlich ein leeres Eingabefeld. Keine
   Beispiele mit Namen, Standorten, Geräten oder Behandlungsfällen ergänzen.
3. Markdown ist das öffentliche Austauschformat. Für den operativen
   Word-Workflow nach R-002/R-004 fehlende Angaben als Word-Kommentare mit
   Autor **QM-System** anlegen, statt Inline-Platzhalter stehenzulassen.
   Kommentar-IDs und Fundstellen in der Kommentarübersicht nachhalten.
4. Arbeitskopien nach `03_Arbeitsdateien/YYMMDD/` mit `_BEARBEITET`-Suffix
   ablegen. Vorlagen gehören in die passende Themenkategorie unter
   `02_Vorlagen_und_Anlagen/`; freigegebene Dokumente nach `01_Dokumente/`.
   Die Repo-Ordner `dokumente/` und `arbeitsdateien/` enthalten nur
   die öffentlichen Ausgangsschablonen.
5. Fachliche Inhalte, anwendbare Vorgaben, Herstellerangaben, Prüfintervalle
   und Zuständigkeiten im Tenant prüfen. Diese Schablonen setzen weder
   Fristen noch Konzentrationen oder medizinische Maßnahmen fest.
6. Vor Freigabe alle Slots ersetzen, Kommentare löschen, Version und
   Datumsfelder prüfen; Freigabe durch die Leitung dokumentieren. Kein
   Patientendatum gehört in QM-Dokumente. Personenbezogene
   Schulungsbestätigungen bleiben ausschließlich im privaten Tenant.

Die Platzhalter im öffentlichen Vorlagenformat sind keine Ausnahme von der
Platzhalterfreiheit freigegebener QM-Dokumente. Es werden keine DOCX-Dateien
oder ausgefüllten Praxis-Handbücher als freigegeben dargestellt.
