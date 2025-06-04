from dataclasses import dataclass, field
import re
from collections import defaultdict, UserList
from typing import Tuple


@dataclass
class Link:
    new_alt: str
    src: str
    location: Tuple[int, int] = (0, 0)


class Links(UserList[Link]):
    @property
    def new_alt_list(self) -> list[str]:
        return [link.new_alt for link in self.data]

    @property
    def only_src_list(self) -> list[str]:
        return [link.src for link in self.data]


def compute_links(html, resource_prefix) -> Links[Link]:
    # Find all <img ... alt="..." ... src="..."> tags
    img_tags = re.findall(r'<img [^>]*alt="([^"]+)"[^>]*src="([^"]+)"[^>]*>', html)
    alt_counts = defaultdict(int)
    alt_indices = defaultdict(int)
    # Count occurrences of each alt
    for alt, _ in img_tags:
        alt_counts[alt] += 1
    result = []
    for alt, src in img_tags:
        if alt_counts[alt] > 1:
            idx = alt_indices[alt]
            new_alt = f"{resource_prefix}{alt.replace('.', f'-{idx:02}.')}"
            alt_indices[alt] += 1
        else:
            new_alt = f"{resource_prefix}{alt}"
        result.append(Link(new_alt, src))
    return Links(result)


@dataclass
class FixImg:
    html: str
    resource_prefix: str
    links: Links[Link] = field(default_factory=Links)

    def __post_init__(self):
        self.links = compute_links(self.html, self.resource_prefix)
