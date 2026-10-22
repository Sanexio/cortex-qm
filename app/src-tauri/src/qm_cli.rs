use std::process::Command;

use crate::qm_content::repo_root;

const DEMO_KATEGORIEN: &str = "rules/CATEGORIES_EXAMPLE.md";

/// Erzeugt eine Demo-Begehungs-Checkliste über die Python-Bibliothek (nur Beispiel-Kategorien).
pub fn checkliste_demo(praxis: &str, rolle: &str) -> Result<String, String> {
    if praxis.trim().is_empty() {
        return Err("Praxisname fehlt".into());
    }
    let root = repo_root();
    let kategorien = root.join(DEMO_KATEGORIEN);
    if !kategorien.is_file() {
        return Err("Beispiel-Kategorien nicht gefunden".into());
    }
    let out_md = std::env::temp_dir().join(format!(
        "cortex-qm-checkliste-{}.md",
        std::process::id()
    ));
    let mut cmd = Command::new("python3");
    cmd.current_dir(&root)
        .env("PYTHONPATH", &root)
        .args([
            "-m",
            "cortex_qm",
            "checkliste",
            "--kategorien",
            DEMO_KATEGORIEN,
            "--praxis",
            praxis.trim(),
            "--rolle",
            rolle.trim(),
            "--out-md",
        ])
        .arg(&out_md);
    let output = cmd.output().map_err(|e| format!("Python nicht startbar: {e}"))?;
    if !output.status.success() {
        let stderr = String::from_utf8_lossy(&output.stderr);
        return Err(format!("cortex-qm checkliste fehlgeschlagen: {stderr}"));
    }
    std::fs::read_to_string(&out_md).map_err(|e| e.to_string())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn demo_checkliste_erzeugt_markdown() {
        let text = checkliste_demo("Demo-Praxis", "QM-Beauftragte").expect("checkliste");
        assert!(text.contains("Demo-Praxis"));
        assert!(text.contains("Checkliste") || text.contains("checkliste"));
    }
}
