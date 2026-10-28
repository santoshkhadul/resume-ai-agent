from dataclasses import dataclass, field
from typing import Dict


@dataclass
class ResumeDocument:
    file_name: str
    file_type: str
    raw_text: str
    normalized_text: str
    page_count: int = 0
    sections: Dict[str, str] = field(default_factory=dict)