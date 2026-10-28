import re


SECTION_ALIASES = {
    "summary": [
        "summary",
        "professional summary",
        "profile",
        "professional profile",
        "career summary",
        "about me",
    ],
    "objective": [
        "objective",
        "career objective",
        "professional objective",
    ],
    "skills": [
        "skills",
        "technical skills",
        "core skills",
        "technical competencies",
        "skills & technologies",
        "skills and technologies",
        "key skills",
    ],
    "experience": [
        "experience",
        "work experience",
        "professional experience",
        "employment history",
        "work history",
    ],
    "education": [
        "education",
        "educational background",
        "academic background",
        "academic qualifications",
    ],
    "projects": [
        "projects",
        "personal projects",
        "academic projects",
        "key projects",
        "project experience",
    ],
    "certifications": [
        "certifications",
        "certificates",
        "professional certifications",
    ],
    "achievements": [
        "achievements",
        "accomplishments",
        "awards",
    ],
    "languages": [
        "languages",
        "language skills",
    ],
}


def normalize_heading(text: str) -> str:
    """
    Normalize a possible resume section heading.
    """

    text = text.strip().lower()

    text = re.sub(r"[^a-z0-9& ]", "", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def detect_resume_sections(text: str) -> dict:
    """
    Detect common resume sections and return
    their text content.
    """

    if not text:
        return {}

    lines = text.splitlines()

    heading_lookup = {}

    for section, aliases in SECTION_ALIASES.items():
        for alias in aliases:
            heading_lookup[normalize_heading(alias)] = section

    sections = {}

    current_section = None
    current_content = []

    for line in lines:
        clean_line = line.strip()

        if not clean_line:
            continue

        normalized_heading = normalize_heading(clean_line)

        # Detect section heading
        if normalized_heading in heading_lookup:

            if current_section:
                sections[current_section] = "\n".join(
                    current_content
                ).strip()

            current_section = heading_lookup[
                normalized_heading
            ]

            current_content = []

            continue

        # Add content to current section
        if current_section:
            current_content.append(clean_line)

    # Save final section
    if current_section:
        sections[current_section] = "\n".join(
            current_content
        ).strip()

    return sections