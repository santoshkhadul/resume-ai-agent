
from pathlib import Path

from docx import Document

from app.services.resume_section_service import (
    normalize_heading,
    SECTION_ALIASES,
)


def _get_skills_headings() -> set[str]:
    """Return normalized headings recognized as Skills."""
    return {
        normalize_heading(alias)
        for alias in SECTION_ALIASES.get("skills", [])
    }


def add_keywords_to_docx_skills(
    input_path: str,
    output_path: str,
    keywords: list[str],
) -> dict:
    """
    Add verified keywords to an existing DOCX Skills section.

    The source document is never overwritten.
    Existing skill text is preserved.
    """

    source = Path(input_path)
    destination = Path(output_path)

    if not source.is_file():
        raise FileNotFoundError(
            f"Input DOCX file not found: {source}"
        )

    if source.suffix.lower() != ".docx":
        raise ValueError("Input file must be a DOCX document.")

    if destination.suffix.lower() != ".docx":
        raise ValueError("Output file must be a DOCX document.")

    if source.resolve() == destination.resolve():
        raise ValueError(
            "Output path must differ from the original resume path."
        )

    clean_keywords = []
    seen = set()

    for keyword in keywords:
        keyword = keyword.strip()

        if keyword and keyword.casefold() not in seen:
            clean_keywords.append(keyword)
            seen.add(keyword.casefold())

    if not clean_keywords:
        return {
            "success": True,
            "output_path": None,
            "added_keywords": [],
            "skipped_keywords": [],
            "message": "No keywords were provided.",
        }

    document = Document(str(source))
    skills_headings = _get_skills_headings()

    skills_heading_index = None

    for index, paragraph in enumerate(document.paragraphs):
        if normalize_heading(paragraph.text) in skills_headings:
            skills_heading_index = index
            break

    if skills_heading_index is None:
        raise ValueError(
            "Could not identify a Skills heading. "
            "The document was not modified."
        )

    paragraphs = document.paragraphs
    skills_heading = paragraphs[skills_heading_index]

    skills_content = []
    for paragraph in paragraphs[skills_heading_index + 1:]:
        if normalize_heading(paragraph.text) in {
            normalize_heading(alias)
            for aliases in SECTION_ALIASES.values()
            for alias in aliases
        }:
            break

        skills_content.append(paragraph)

    existing_text = " ".join(
        paragraph.text for paragraph in skills_content
    )

    added_keywords = []
    skipped_keywords = []

    for keyword in clean_keywords:
        import re

        pattern = (
            r"(?<!\w)"
            + re.escape(keyword)
            + r"(?!\w)"
        )

        if re.search(pattern, existing_text, flags=re.IGNORECASE):
            skipped_keywords.append(keyword)
        else:
            added_keywords.append(keyword)

    if not added_keywords:
        return {
            "success": True,
            "output_path": None,
            "added_keywords": [],
            "skipped_keywords": skipped_keywords,
            "message": "All selected keywords already exist in Skills.",
        }

    if skills_content:
        # Add to the final existing Skills paragraph.
        target_paragraph = skills_content[-1]
        separator = ", " if target_paragraph.text.strip() else ""
        target_paragraph.add_run(
            separator + ", ".join(added_keywords)
        )
    else:
        # Create a paragraph immediately after the Skills heading.
        new_paragraph = skills_heading.insert_paragraph_before("")
        new_paragraph.add_run(", ".join(added_keywords))
        new_paragraph._p.addnext(skills_heading._p)

    destination.parent.mkdir(parents=True, exist_ok=True)
    document.save(str(destination))

    return {
        "success": True,
        "output_path": str(destination),
        "added_keywords": added_keywords,
        "skipped_keywords": skipped_keywords,
        "message": "A new DOCX copy was created.",
    }
