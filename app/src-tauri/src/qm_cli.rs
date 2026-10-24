// Native render of the existing K0 example checklist; no external process or temporary document.
const VORLAGE: &str = include_str!("checkliste-vorlage.md");
pub fn checkliste_demo(praxis: &str, rolle: &str) -> Result<String, String> {
    fn safe(s: &str) -> bool {
        !s.trim().is_empty()
            && s.len() <= 200
            && !s
                .chars()
                .any(|c| c.is_control() || c == '|' || c == '{' || c == '}')
    }
    if !safe(praxis) || !safe(rolle) {
        return Err("Name/Rolle ungueltig (1–200 Zeichen, keine Steuerzeichen)".into());
    }
    Ok(VORLAGE
        .replace("{{PRAXIS}}", praxis.trim())
        .replace("{{ROLLE}}", rolle.trim()))
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn existing_demo_is_preserved_without_external_runtime() {
        let s = checkliste_demo("Demo-Praxis", "QM-Beauftragte").unwrap();
        assert!(s.contains("Demo-Praxis"));
        assert!(s.contains("CHK-01-01"));
        assert!(!s.contains("{{"));
    }
    #[test]
    fn hostile_labels_denied() {
        for s in ["", "x\n# injection", "x|table", "{{ROLLE}}"] {
            assert!(checkliste_demo(s, "QM").is_err());
        }
    }
}
