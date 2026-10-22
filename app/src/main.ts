import { invoke } from "@tauri-apps/api/core";
import { applyTheme, cycleTheme, readTheme } from "./theme";

interface LicenseOverview {
  state: string;
  gebucht: boolean;
  hinweis: string;
}

interface RuleEntry {
  pfad: string;
  titel: string;
}

interface VorlageEntry {
  pfad: string;
  phase: string;
  typ: string;
}

interface AppInfo {
  version: string;
  app_id: string;
  bundle_id: string;
  klasse: string;
}

function el<K extends keyof HTMLElementTagNameMap>(
  tag: K,
  className?: string,
  text?: string,
): HTMLElementTagNameMap[K] {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

function isTauri(): boolean {
  return "__TAURI_INTERNALS__" in window;
}

async function loadRules(): Promise<RuleEntry[]> {
  if (!isTauri()) return [];
  return invoke<RuleEntry[]>("rules_list");
}

async function loadRule(path: string): Promise<string> {
  return invoke<string>("rules_read", { pfad: path });
}

async function loadVorlagen(): Promise<VorlageEntry[]> {
  if (!isTauri()) return [];
  return invoke<VorlageEntry[]>("vorlagen_list");
}

async function loadVorlage(path: string): Promise<string> {
  return invoke<string>("vorlagen_read", { pfad: path });
}

async function runChecklisteDemo(praxis: string, rolle: string): Promise<string> {
  return invoke<string>("checkliste_demo", { praxis, rolle });
}

async function loadLicense(): Promise<LicenseOverview> {
  if (!isTauri()) {
    return {
      state: "browser",
      gebucht: true,
      hinweis: "Vorschau im Browser — Lizenzprüfung nur in der nativen App.",
    };
  }
  return invoke<LicenseOverview>("lizenz_ueberblick");
}

async function loadInfo(): Promise<AppInfo | null> {
  if (!isTauri()) return null;
  return invoke<AppInfo>("app_info");
}

async function checkUpdate(line: HTMLElement): Promise<void> {
  line.textContent = "Suche nach Updates …";
  try {
    const version = await invoke<string | null>("updater_check");
    line.textContent = version
      ? `Update verfügbar: ${version}`
      : "Kein Update verfügbar (Stub-Feed).";
  } catch (err) {
    line.textContent = `Update-Prüfung: ${String(err)}`;
  }
}

function renderTabs(active: string, onSelect: (id: string) => void): HTMLElement {
  const nav = el("nav", "tabs");
  for (const tab of [
    ["regeln", "Regelwerk"],
    ["vorlagen", "Vorlagen"],
    ["werkzeuge", "Werkzeuge"],
    ["status", "Status"],
  ] as const) {
    const btn = el("button", tab[0] === active ? "active" : undefined, tab[1]);
    btn.addEventListener("click", () => onSelect(tab[0]));
    nav.appendChild(btn);
  }
  return nav;
}

async function render(): Promise<void> {
  const mount = document.getElementById("app");
  if (!mount) return;
  mount.replaceChildren();

  const shell = el("div", "shell");
  const header = el("header");
  const title = el("h1", undefined, "Cortex QM");
  const badge = el("span", "badge", "K0 · Qualitätsmanagement");
  const themeBtn = el("button", undefined, "Design umschalten");
  themeBtn.addEventListener("click", () => {
    const key = cycleTheme();
    themeBtn.textContent =
      key === "praxis2025" ? "Cyberpunk" : "Praxis 2025";
  });
  themeBtn.textContent = readTheme() === "praxis2025" ? "Cyberpunk" : "Praxis 2025";
  header.append(title, badge, themeBtn);
  shell.appendChild(header);

  let active = "regeln";
  const body = el("div");
  shell.appendChild(body);

  async function paint(): Promise<void> {
    body.replaceChildren(renderTabs(active, (id) => {
      active = id;
      void paint();
    }));

    if (active === "regeln") {
      const card = el("section", "card");
      card.appendChild(el("h2", undefined, "QM-Regelwerk (Framework)"));
      card.appendChild(
        el(
          "p",
          "muted",
          "Normatives Regelwerk aus diesem Repository — Schemata, Kernregeln und Beispiel-Kataloge, keine Tenant-Dateien.",
        ),
      );
      const list = el("ul", "rules");
      const viewer = el("pre", "viewer");
      viewer.textContent = "Datei auswählen …";
      const rules = await loadRules();
      for (const rule of rules) {
        const li = el("li");
        const btn = el("button", "link", rule.titel || rule.pfad);
        btn.addEventListener("click", () => {
          void loadRule(rule.pfad).then((text) => {
            viewer.textContent = text;
          });
        });
        li.appendChild(btn);
        list.appendChild(li);
      }
      card.append(list, viewer);
      body.appendChild(card);
    }

    if (active === "vorlagen") {
      const card = el("section", "card");
      card.appendChild(el("h2", undefined, "Phase-B-Strukturvorlagen"));
      const vorlagen = await loadVorlagen();
      const list = el("ul", "rules");
      const viewer = el("pre", "viewer");
      viewer.textContent = "Vorlage auswählen …";
      for (const v of vorlagen) {
        const li = el("li");
        const btn = el("button", "link", v.pfad);
        btn.addEventListener("click", () => {
          void loadVorlage(v.pfad).then((text) => {
            viewer.textContent = text;
          });
        });
        li.append(btn, el("span", "muted", ` · ${v.phase} · ${v.typ}`));
        list.appendChild(li);
      }
      card.append(list, viewer);
      body.appendChild(card);
    }

    if (active === "werkzeuge") {
      const card = el("section", "card");
      card.appendChild(el("h2", undefined, "CLI-Werkzeuge (Demo)"));
      card.appendChild(
        el(
          "p",
          "muted",
          "Begehungs-Checkliste aus rules/CATEGORIES_EXAMPLE.md — Praxisname frei wählbar, nur fiktive Kategorien.",
        ),
      );
      const praxisInput = el("input") as HTMLInputElement;
      praxisInput.placeholder = "Praxisname (Demo)";
      praxisInput.value = "Demo-Praxis";
      const rolleInput = el("input") as HTMLInputElement;
      rolleInput.placeholder = "Rolle";
      rolleInput.value = "QM-Beauftragte";
      const out = el("pre", "viewer");
      out.textContent = "Noch keine Ausgabe.";
      const runBtn = el("button", "primary", "Checkliste erzeugen");
      runBtn.addEventListener("click", () => {
        if (!isTauri()) {
          out.textContent = "Nur in der nativen App verfügbar.";
          return;
        }
        out.textContent = "Erzeuge …";
        void runChecklisteDemo(praxisInput.value, rolleInput.value)
          .then((text) => {
            out.textContent = text;
          })
          .catch((err) => {
            out.textContent = String(err);
          });
      });
      card.append(praxisInput, rolleInput, runBtn, out);
      body.appendChild(card);
    }

    if (active === "status") {
      const lic = await loadLicense();
      const info = await loadInfo();
      const card = el("section", "card");
      card.appendChild(el("h2", undefined, "Lizenz & Marketplace"));
      card.appendChild(el("p", undefined, lic.hinweis));
      card.appendChild(
        el("p", "mono", `Zustand: ${lic.state} · gebucht: ${lic.gebucht ? "ja" : "nein"}`),
      );
      if (info) {
        card.appendChild(
          el(
            "p",
            "mono",
            `${info.app_id} · ${info.bundle_id} · v${info.version} · ${info.klasse}`,
          ),
        );
      }
      const updateLine = el("p", "muted");
      const updateBtn = el("button", undefined, "Nach Updates suchen");
      updateBtn.addEventListener("click", () => void checkUpdate(updateLine));
      if (!isTauri()) updateBtn.disabled = true;
      card.append(updateBtn, updateLine);

      const hinweis = el("section", "card");
      hinweis.appendChild(el("h2", undefined, "Tenant-Grenze"));
      hinweis.appendChild(
        el(
          "p",
          "muted",
          "Ausgefüllte QM-Dokumente, Personal- und Gerätelisten bleiben im privaten Tenant — nicht in dieser K0-App.",
        ),
      );
      body.append(card, hinweis);
    }
  }

  mount.appendChild(shell);
  await paint();
}

void render();
