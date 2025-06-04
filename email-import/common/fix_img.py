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
    # Find all <img ...> tags
    img_tags = re.findall(r'<img[^>]*>', html)
    alt_counts = defaultdict(int)
    alt_indices = defaultdict(int)
    img_info = []
    for tag in img_tags:
        alt_match = re.search(r'alt=["\']([^"\']*)["\']', tag)
        src_match = re.search(r'src=["\']([^"\']*)["\']', tag)
        alt = alt_match.group(1) if alt_match else ''
        src = src_match.group(1) if src_match else ''
        img_info.append((alt, src))
        alt_counts[alt] += 1
    result = []
    for alt, src in img_info:
        if alt and alt_counts[alt] > 1:
            idx = alt_indices[alt]
            new_alt = f"{resource_prefix}{alt.replace('.', f'-{idx:02}.')}"
            alt_indices[alt] += 1
        elif alt:
            new_alt = f"{resource_prefix}{alt}"
        else:
            new_alt = ''
        result.append(Link(new_alt, src))
    return Links(result)


@dataclass
class FixImg:
    html: str
    resource_prefix: str
    links: Links[Link] = field(default_factory=Links)

    def __post_init__(self):
        self.links = compute_links(self.html, self.resource_prefix)
