from dataclasses import dataclass, field
import re
from collections import defaultdict

@dataclass
class Link:
    new_alt: str
    src: str = ''


def compute_links(html, resource_prefix) -> list[Link]:
    # Find all <img ... alt="..."> tags
    img_tags = re.findall(r'<img [^>]*alt="([^"]+)"[^>]*>', html)
    alt_counts = defaultdict(int)
    alt_indices = defaultdict(int)
    # Count occurrences of each alt
    for alt in img_tags:
        alt_counts[alt] += 1
    result = []
    for alt in img_tags:
        if alt_counts[alt] > 1:
            idx = alt_indices[alt]
            new_alt = f"{resource_prefix}{alt.replace('.', f'-{idx:02}.')}"
            alt_indices[alt] += 1
        else:
            new_alt = f"{resource_prefix}{alt}"
        result.append(Link(new_alt))
    return result

@dataclass
class FixImg:
    html: str
    resource_prefix: str
    links: list[Link] = field(default_factory=list)

    def __post_init__(self):
        self.links = compute_links(self.html, self.resource_prefix)
