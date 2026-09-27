#!/usr/bin/env python3
"""Create a minimal DOCX fixture with Word comments, using stdlib only."""

from __future__ import annotations

import sys
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape


W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG_REL = "http://schemas.openxmlformats.org/package/2006/relationships"


COMMENTS = [
    {
        "id": "0",
        "target": "Versionsnummer: v1.0",
        "comment": "Bitte Review-Datum und Freigabe durch Aerztliche Leitung nach R-001 ergaenzen.",
    },
    {
        "id": "1",
        "target": "Hygieneplan der Demo-Praxis Musterstadt",
        "comment": "QM-Beauftragte prueft, ob der R&D-Plan im Themenordner 01 referenziert ist.",
    },
    {
        "id": "2",
        "target": "Medizinprodukte: Bestandsverzeichnis offen",
        "comment": "Rolle QM-Beauftragte: fiktiven Status mit Themenordner 10 abgleichen; keine echten Geraetedaten eintragen.",
    },
]


def paragraph(text: str) -> str:
    return f"<w:p><w:r><w:t>{escape(text)}</w:t></w:r></w:p>"


def commented_paragraph(comment_id: str, text: str) -> str:
    return (
        '<w:p>'
        f'<w:commentRangeStart w:id="{comment_id}"/>'
        f'<w:r><w:t>{escape(text)}</w:t></w:r>'
        f'<w:commentRangeEnd w:id="{comment_id}"/>'
        '<w:r><w:commentReference w:id="' + comment_id + '"/></w:r>'
        '</w:p>'
    )


def build_document_xml() -> str:
    body = [
        paragraph("Demo-Praxis Musterstadt - QM-Arbeitsfassung"),
        *(commented_paragraph(item["id"], item["target"]) for item in COMMENTS),
        paragraph("Diese Fixture enthaelt ausschliesslich fiktive Rollen- und Praxisdaten."),
    ]
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        f'<w:document xmlns:w="{W}" xmlns:r="{R}"><w:body>'
        + "".join(body)
        + '<w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1417" '
        'w:right="1417" w:bottom="1417" w:left="1417"/></w:sectPr></w:body></w:document>'
    )


def build_comments_xml() -> str:
    comments = []
    for item in COMMENTS:
        comments.append(
            f'<w:comment w:id="{item["id"]}" w:author="QM-System" '
            'w:date="2026-07-25T09:00:00Z">'
            f'<w:p><w:r><w:t>{escape(item["comment"])}</w:t></w:r></w:p>'
            '</w:comment>'
        )
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        f'<w:comments xmlns:w="{W}">' + "".join(comments) + '</w:comments>'
    )


FILES = {
    "[Content_Types].xml": """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/comments.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.comments+xml"/>
</Types>
""",
    "_rels/.rels": f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="{PKG_REL}">
  <Relationship Id="rId1" Type="{R}/officeDocument" Target="word/document.xml"/>
</Relationships>
""",
    "word/_rels/document.xml.rels": f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="{PKG_REL}">
  <Relationship Id="rId1" Type="{R}/comments" Target="comments.xml"/>
</Relationships>
""",
}


def main() -> int:
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "fixture_qm_kommentare.docx")
    out.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as docx:
        for name, content in FILES.items():
            docx.writestr(name, content)
        docx.writestr("word/document.xml", build_document_xml())
        docx.writestr("word/comments.xml", build_comments_xml())
    print(f"Fixture erzeugt: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
