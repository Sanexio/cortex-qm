#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DOCX_DIR="$ROOT_DIR/examples/docx-kommentar-demo"
AUDIT_DIR="$ROOT_DIR/examples/audit-checkliste-demo"

section() {
  printf '\n== %s ==\n' "$1"
}

maybe_pdf() {
  local input_html="$1"
  local output_pdf="$2"
  local tmp_pdf="${output_pdf}.tmp"

  if command -v cupsfilter >/dev/null 2>&1; then
    if cupsfilter "$input_html" >"$tmp_pdf" 2>/dev/null && [ -s "$tmp_pdf" ]; then
      mv "$tmp_pdf" "$output_pdf"
      printf 'PDF erzeugt: %s\n' "$output_pdf"
    else
      rm -f "$tmp_pdf" "$output_pdf"
      printf 'PDF uebersprungen: cupsfilter konnte %s nicht konvertieren.\n' "$input_html"
    fi
  else
    rm -f "$output_pdf"
    printf 'PDF uebersprungen: kein macOS-Konverter (cupsfilter) verfuegbar.\n'
  fi
}

section "Demo 1: DOCX-Kommentar-Workflow"
# Fixture nur erzeugen, wenn sie fehlt — Neu-Generierung aendert
# Zip-Timestamps und macht den Git-Tree bei jedem Demo-Lauf dirty.
if [[ ! -f "$DOCX_DIR/fixture_qm_kommentare.docx" ]]; then
  python3 "$DOCX_DIR/make_fixture.py" "$DOCX_DIR/fixture_qm_kommentare.docx"
fi
python3 "$DOCX_DIR/extract_comments.py" \
  "$DOCX_DIR/fixture_qm_kommentare.docx" \
  "$DOCX_DIR/auswertung.md"
sed -n '1,14p' "$DOCX_DIR/auswertung.md"

section "Demo 2: Audit-Checklisten-Automation"
python3 "$AUDIT_DIR/generate_checklist.py" \
  --rules-dir "$ROOT_DIR/rules" \
  --out-md "$AUDIT_DIR/begehungs_checkliste.md" \
  --out-html "$AUDIT_DIR/begehungs_checkliste.html"
python3 "$AUDIT_DIR/tracker.py" \
  --csv "$AUDIT_DIR/tracker_fixture.csv" \
  --out-md "$AUDIT_DIR/status_report.md" \
  --out-html "$AUDIT_DIR/status_report.html" \
  --today 2026-07-25
sed -n '1,18p' "$AUDIT_DIR/status_report.md"

section "Optionale PDF-Ausgabe"
maybe_pdf "$AUDIT_DIR/begehungs_checkliste.html" "$AUDIT_DIR/begehungs_checkliste.pdf"
maybe_pdf "$AUDIT_DIR/status_report.html" "$AUDIT_DIR/status_report.pdf"

section "Fertig"
printf 'Erzeugte Demo-Artefakte liegen unter examples/.\n'
