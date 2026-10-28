import re

from app.services.jd_text_service import normalize_job_description


SECTION_NAMES = {
    "requirements": [
        "requirements",
        "qualifications",
        "required qualifications",
        "required skills",
        "what we're looking for",
        "what we are looking for",
    ],
    "responsibilities": [
        "responsibilities",
        "responsibilities and duties",
        "duties",
        "job responsibilities",
        "what you'll do",
        "what you will do",
    ],
    "skills": [
        "skills",
        "technical skills",
        "required skills",
        "key skills",
        "technologies",
        "technical requirements",
    ],
    "experience": [
        "experience",
        "required experience",
        "professional experience",
    ],
    "education": [
        "education",
        "educational qualifications",
        "academic qualifications",
    ],
}


KEYWORD_PATTERNS = [
    # Programming languages
    "python",
    "c",
    "c++",
    "cpp",
    "c#",
    "java",
    "javascript",
    "typescript",
    "php",
    "go",
    "golang",
    "rust",
    "kotlin",
    "swift",

    # Python / Backend
    "django",
    "flask",
    "fastapi",
    "spring",
    "spring boot",
    "express",
    "node",
    ".net",
    "asp.net",

    # Frontend
    "frontend",
    "front-end",
    "react",
    "angular",
    "vue",
    "next",
    "html",
    "css",
    "bootstrap",
    "tailwind",
    "mui",
    "redux",
    "vite",
    "webpack",
    "responsive design",
    "accessibility",
    "dom",
    "browser",
    "cross-browser",

    # Backend / Full Stack
    "backend",
    "full stack",
    "web development",
    "web application",
    "server-side",

    # APIs
    "rest api",
    "graphql",
    "websocket",
    "socket.io",
    "microservices",

    # C++ / Software Engineering
    "stl",
    "oop",
    "data structures",
    "algorithms",
    "dsa",
    "pointers",
    "memory management",
    "multithreading",
    "concurrency",
    "templates",
    "inheritance",
    "polymorphism",
    "encapsulation",
    "abstraction",
    "smart pointers",
    "lambda expressions",
    "exception handling",
    "debugging",
    "gdb",
    "cmake",
    "makefile",
    "gcc",
    "g++",
    "visual studio",
    "qt",
    "boost",

    # Database
    "sql",
    "mysql",
    "postgresql",
    "sqlite",
    "mongodb",
    "redis",
    "oracle",
    "database",
    "database design",
    "database management",
    "database optimization",

    # ORM
    "sqlalchemy",
    "django orm",
    "hibernate",
    "entity framework",
    "orm",

    # Authentication / Security
    "jwt",
    "json web token",
    "authentication",
    "authorization",
    "oauth",
    "oauth2",
    "rbac",
    "bcrypt",
    "security",
    "cors",

    # Software Engineering
    "software engineer",
    "software engineering",
    "software development",
    "application development",
    "system design",
    "system architecture",
    "object-oriented design",
    "design patterns",
    "problem solving",
    "clean code",
    "code review",
    "performance optimization",
    "scalable applications",
    "scalable systems",
    "distributed systems",
    "low-level design",
    "high-level design",

    # AI / ML
    "ai engineer",
    "ai engineering",
    "artificial intelligence",
    "machine learning",
    "deep learning",
    "ml engineer",
    "machine learning engineer",
    "generative ai",
    "genai",
    "llm",
    "nlp",
    "computer vision",
    "neural networks",
    "tensorflow",
    "pytorch",
    "keras",
    "scikit-learn",
    "hugging face",
    "transformers",
    "langchain",
    "langgraph",
    "openai api",
    "prompt engineering",
    "rag",
    "retrieval augmented generation",
    "vector database",
    "embeddings",
    "fine-tuning",
    "model deployment",
    "mlops",
    "feature engineering",
    "model evaluation",
    "model training",
    "model inference",

    # Testing
    "testing",
    "unit testing",
    "integration testing",
    "pytest",
    "unittest",
    "test automation",
    "tdd",

    # Version Control
    "git",
    "github",
    "gitlab",
    "bitbucket",
    "version control",

    # DevOps
    "docker",
    "docker compose",
    "kubernetes",
    "ci/cd",
    "jenkins",
    "github actions",
    "nginx",

    # Cloud
    "aws",
    "azure",
    "google cloud",
    "gcp",
    "ec2",
    "s3",
    "lambda",

    # Tools
    "postman",
    "swagger",
    "openapi",
    "vs code",
    "visual studio code",
    "jira",

    # Web
    "http",
    "https",
    "json",
    "xml",
    "ajax",
    "fetch api",

    # Architecture
    "mvc",
    "rest architecture",
    "modular architecture",
    "monolithic architecture",
    "microservices architecture",

    # Agile
    "agile",
    "scrum",
    "sprint",
]


def detect_sections(text: str) -> dict:
    """
    Detect common JD sections and capture their content.

    Supports:

    Requirements
    Python
    FastAPI

    Requirements: Python, FastAPI
    """

    normalized_text = normalize_job_description(text)

    if not normalized_text:
        return {}

    lines = normalized_text.splitlines()

    sections = {}

    section_lookup = {}

    for section, names in SECTION_NAMES.items():
        for name in names:
            section_lookup[name.lower()] = section

    current_section = None
    current_content = []

    for line in lines:
        clean_line = line.strip()

        if not clean_line:
            continue

        # ---------------------------------
        # Format: "Requirements: Python..."
        # ---------------------------------
        if ":" in clean_line:
            heading, content = clean_line.split(":", 1)

            heading = heading.strip().lower()

            if heading in section_lookup:

                if current_section and current_content:
                    sections[current_section] = "\n".join(
                        current_content
                    ).strip()

                current_section = section_lookup[heading]
                current_content = []

                content = content.strip()

                if content:
                    current_content.append(content)

                continue

        # ---------------------------------
        # Format: "Requirements"
        # ---------------------------------
        heading = clean_line.rstrip(":").strip().lower()

        if heading in section_lookup:

            if current_section and current_content:
                sections[current_section] = "\n".join(
                    current_content
                ).strip()

            current_section = section_lookup[heading]
            current_content = []

            continue

        # ---------------------------------
        # Normal section content
        # ---------------------------------
        if current_section:
            current_content.append(clean_line)

    # ---------------------------------
    # Save final section
    # ---------------------------------
    if current_section and current_content:
        sections[current_section] = "\n".join(
            current_content
        ).strip()

    return sections


def extract_keywords(text: str) -> list[str]:
    """
    Extract relevant software-development keywords
    from a job description using safe word-boundary matching.
    """

    normalized_text = normalize_job_description(text)

    if not normalized_text:
        return []

    text_lower = normalized_text.lower()

    found_keywords = []

    for keyword in KEYWORD_PATTERNS:
        keyword_lower = keyword.lower()

        pattern = (
            r"(?<!\w)"
            + re.escape(keyword_lower)
            + r"(?!\w)"
        )

        if re.search(pattern, text_lower):
            found_keywords.append(keyword)

    return list(dict.fromkeys(found_keywords))

def extract_required_skills(text: str) -> list[str]:
    """
    Extract required technical skills from a job description.
    """

    keywords = extract_keywords(text)

    skill_categories = {
        "python", "java", "javascript", "typescript",
        "c++", "c#", "php", "go", "rust",
        "django", "flask", "fastapi", "react",
        "angular", "vue", "node", "express",
        "html", "css", "tailwind", "bootstrap",
        "sql", "mysql", "postgresql", "sqlite",
        "mongodb", "redis", "oracle",
        "rest api", "graphql", "websocket",
        "docker", "docker compose", "kubernetes",
        "aws", "azure", "google cloud", "gcp",
        "git", "github", "gitlab",
        "machine learning", "deep learning",
        "generative ai", "tensorflow", "pytorch",
        "scikit-learn", "nlp", "rag",
        "pytest", "unit testing", "testing",
        "fastapi", "django orm", "sqlalchemy",
        "postman", "swagger", "openapi",
    }

    return [
        keyword
        for keyword in keywords
        if keyword.lower() in skill_categories
    ]