# Einzel-App Cortex QM (2026-10-22)

## Auftrag

Native Tauri-2-Einzelapp für `cortex-qm` auf Zweig `einzelapp-20261022`, Marketplace-Manifest, lauffähiger unsignierter Build, Tests grün.

## Gebaut

| Baustein | Ort | Zweck |
|----------|-----|--------|
| Tauri 2 + Vite/TS | `app/` | Eigenständiges Programm `Cortex QM`, Bundle-ID `de.sanexio.cortex-qm`, Version 0.1.0 |
| `cortex-app-core` | Pfadabhängigkeit in `app/src-tauri/Cargo.toml` | Andock-Manifest, signierte Lizenzprüfung (öffentlicher Schlüssel zur Build-Zeit) |
| UI | `app/src/` | QM-Regelwerk (`rules/`), Phase-B-Vorlagen (`dokumente/`, `arbeitsdateien/` per Manifest), Demo-Checkliste via `cortex_qm` CLI |
| Design | `app/src/themes.css`, `theme.ts` | **Praxis 2025** (Default) und **Cyberpunk** (`cyber-dark`) umschaltbar |
| Marketplace | `marketplace/app.json` + `icon.png` / `icon-qr.png` | Katalog-Metadaten für den Cortex-Marketplace |
| Lizenz-Stub | `app/schluessel/lizenz-oeffentlich.txt` | Ed25519-Öffentlichkeit (wie Nexus Marketplace); keine Zahlung, Freischaltung über signierte `lizenz.json` |
| Updater-Stub | `tauri-plugin-updater` + Platzhalter-Feed in `tauri.conf.json` | Manuelle Prüfung im UI; Artefakt-Signierung aus (Codex/Beglaubigung offen) |

### Funktionsumfang v0.1.0

- Lesender Zugriff auf das **QM-Regelwerk** im Repo (`rules/`, Pfad-Allowlist, keine `*_TENANT.md`).
- Anzeige und Lesen der **Phase-B-Platzhalter** aus `docs/vorlagen-manifest.json` (`dokumente/`, `arbeitsdateien/`).
- **Demo-Werkzeug:** Begehungs-Checkliste über eingebettete Python-Bibliothek (`rules/CATEGORIES_EXAMPLE.md` nur).
- Beim Start: **Andock-Manifest** unter `~/Library/Application Support/Cortex/apps/cortex-qm.json` (macOS).
- **Kein** Zugriff auf private Tenant-Arbeitsordner (`01_Dokumente/` …) oder gitignored Tenant-Listen.

### Build (lokal, unsigniert)

```sh
cd app
npm ci
npm run build
npm exec tauri build
```

Ergebnis (macOS): `app/src-tauri/target/release/bundle/macos/Cortex QM.app`

### Tests

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover
cd app && npm test
cd app/src-tauri && cargo test
```

## Noch offen (bewusst nicht in diesem Zweig)

- **Code-Signing / Notarisierung** (macOS) und Windows-Signatur — Auftrag Codex.
- **Minisign-Update-Schlüssel** und echter Update-Feed (aktuell Platzhalter-URL + `REPLACE_WITH_MINISIGN_PUBLIC_KEY`).
- **Tracker- und Kommentar-Werkzeuge** in der UI (CLI vorhanden, noch ohne Datei-Dialog und Tenant-Pfadwahl).
- **Nexus-Brücke** (Cargo-Feature wie App-Template) — nicht aktiviert.
- **CI** (GitHub Actions, drei OS) — folgt Marketplace-Welle.
- Symbol **Sanexio-QR**: `marketplace/icon-qr.png` ist vorerst dieselbe Rastergrafik wie `icon.png`; dedizierte QR-Markenvariante durch Design/Codex.

## Referenzen

- `Nexus/specs/app-marketplace/00_KONZEPT.md`, `02_CORTEX_APP_DESIGN.md`
- `Nexus/_rules/design-theme.md`
- Vorlage: `projects/cortex-desk/app/` (Einzelapp-Welle 2026-10-22), `projects/cortex-app-core`
