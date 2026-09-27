# QM-Demo-Tooling

Diese Beispiele zeigen als **Pseudo-Engine**, wie ein Tenant das
Regelwerk aus `rules/` mit einfachem Tooling verbinden koennte. Alle
Daten sind fiktiv und beziehen sich auf die "Demo-Praxis Musterstadt".
Personen werden nur als Rollen benannt, z.B. "QM-Beauftragte" oder
"Aerztliche Leitung".

Das echte Tooling-Bundle ist nicht Teil dieses Repos. Fuer Sanexio-
Tenants ist es Bestandteil des Tenant-Vertrags; Details stehen in
`docs/ENGINE_INTEGRATION.md`.

## Start

Vom Repo-Root aus:

```bash
bash examples/run-demo.sh
```

Der Einstiegspunkt fuehrt beide Demos nacheinander aus und bricht bei
Fehlern mit einem Exit-Code ungleich 0 ab.

## Demo 1: DOCX-Kommentar-Workflow

Ordner: `examples/docx-kommentar-demo/`

- `make_fixture.py` erzeugt eine minimale echte `.docx`-Datei mit Word-
  Kommentaren.
- `fixture_qm_kommentare.docx` ist die eingecheckte Fixture.
- `extract_comments.py` liest nur mit `python3`-Standardbibliothek aus
  `word/document.xml` und `word/comments.xml`.
- Ergebnis: `auswertung.md` mit Fundstelle, Kommentar und abgeleiteter
  QM-Massnahme.

## Demo 2: Audit-Checklisten-Automation

Ordner: `examples/audit-checkliste-demo/`

- `generate_checklist.py` liest die Struktur aus `rules/` und erzeugt
  eine Begehungs-Checkliste als Markdown und selbstenthaltenes HTML.
- `tracker.py` liest `tracker_fixture.csv` und erzeugt einen Status-
  Report als Markdown und HTML.
- PDF-Ausgabe ist optional: `run-demo.sh` nutzt macOS-Bordmittel, wenn
  verfuegbar, und ueberspringt die PDF-Erzeugung sonst sauber.

Die Demos duplizieren keine produktiven Tenant-Daten und schreiben nur
in `examples/`.
