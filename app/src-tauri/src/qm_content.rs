// Only these versioned framework files enter the app. No filesystem lookup at runtime.
use serde::Serialize;
#[derive(Debug, Serialize, Clone)]
pub struct RuleEntry {
    pub pfad: String,
    pub titel: String,
}
#[derive(Debug, Serialize, Clone)]
pub struct VorlageEntry {
    pub pfad: String,
    pub phase: String,
    pub typ: String,
}
const CONTENT: &[(&str, &str)] = &[
    (
        "rules/CATEGORIES_EXAMPLE.md",
        include_str!("../../../rules/CATEGORIES_EXAMPLE.md"),
    ),
    (
        "rules/CORE_RULES.md",
        include_str!("../../../rules/CORE_RULES.md"),
    ),
    (
        "rules/GERAETE_EXAMPLE.md",
        include_str!("../../../rules/GERAETE_EXAMPLE.md"),
    ),
    (
        "rules/PERSONAL_EXAMPLE.md",
        include_str!("../../../rules/PERSONAL_EXAMPLE.md"),
    ),
    (
        "rules/RAEUMLICHKEITEN_EXAMPLE.md",
        include_str!("../../../rules/RAEUMLICHKEITEN_EXAMPLE.md"),
    ),
    ("rules/SCHEMA.md", include_str!("../../../rules/SCHEMA.md")),
    (
        "rules/WORKFLOW.md",
        include_str!("../../../rules/WORKFLOW.md"),
    ),
    (
        "dokumente/aktionsplan.md",
        include_str!("../../../dokumente/aktionsplan.md"),
    ),
    (
        "dokumente/hygieneplan.md",
        include_str!("../../../dokumente/hygieneplan.md"),
    ),
    (
        "dokumente/medizinproduktebuch.md",
        include_str!("../../../dokumente/medizinproduktebuch.md"),
    ),
    (
        "dokumente/qm-handbuch.md",
        include_str!("../../../dokumente/qm-handbuch.md"),
    ),
    (
        "dokumente/sop.md",
        include_str!("../../../dokumente/sop.md"),
    ),
    (
        "arbeitsdateien/kommentar-uebersicht.md",
        include_str!("../../../arbeitsdateien/kommentar-uebersicht.md"),
    ),
    (
        "arbeitsdateien/reviewprotokoll.md",
        include_str!("../../../arbeitsdateien/reviewprotokoll.md"),
    ),
    (
        "arbeitsdateien/schulungsnachweis.md",
        include_str!("../../../arbeitsdateien/schulungsnachweis.md"),
    ),
];
fn read(pfad: &str) -> Result<String, String> {
    CONTENT
        .iter()
        .find(|(p, _)| *p == pfad)
        .map(|(_, s)| s.to_string())
        .ok_or_else(|| "Pfad nicht im eingebauten Framework-Katalog".into())
}
pub fn rules_list() -> Result<Vec<RuleEntry>, String> {
    Ok(CONTENT
        .iter()
        .filter(|(p, _)| p.starts_with("rules/"))
        .map(|(p, _)| RuleEntry {
            pfad: p.to_string(),
            titel: p
                .trim_start_matches("rules/")
                .trim_end_matches(".md")
                .replace('_', " "),
        })
        .collect())
}
pub fn rules_read(pfad: &str) -> Result<String, String> {
    if !pfad.starts_with("rules/") {
        return Err("Keine Regel".into());
    }
    read(pfad)
}
pub fn vorlagen_list() -> Result<Vec<VorlageEntry>, String> {
    let manifest: serde_json::Value =
        serde_json::from_str(include_str!("../../../docs/vorlagen-manifest.json"))
            .map_err(|e| e.to_string())?;
    Ok(manifest["vorlagen"]
        .as_array()
        .ok_or("Vorlagen fehlen")?
        .iter()
        .filter_map(|v| {
            let p = v["pfad"].as_str()?;
            if !CONTENT.iter().any(|(known, _)| *known == p) {
                return None;
            }
            Some(VorlageEntry {
                pfad: p.into(),
                phase: v["phase"].as_str().unwrap_or("").into(),
                typ: v["typ"].as_str().unwrap_or("").into(),
            })
        })
        .collect())
}
pub fn vorlagen_read(pfad: &str) -> Result<String, String> {
    if pfad.starts_with("rules/") {
        return Err("Keine Vorlage".into());
    }
    read(pfad)
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn standalone_content_is_embedded() {
        assert!(!rules_list().unwrap().is_empty());
        for v in vorlagen_list().unwrap() {
            assert!(!vorlagen_read(&v.pfad).unwrap().is_empty());
        }
    }
    #[test]
    fn traversal_unknown_absolute_and_tenant_are_denied() {
        for p in [
            "rules/../README.md",
            "/etc/passwd",
            "rules/CORE_RULES.md/../../secret",
            "rules/CATEGORIES_TENANT.md",
            "templates/unknown.md",
        ] {
            assert!(read(p).is_err(), "{p}");
        }
    }
}
