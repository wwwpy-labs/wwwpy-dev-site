from dataclasses import dataclass, field
import re
from collections import defaultdict, UserList
from typing import Tuple


@dataclass
class Link:
    new_src: str
    src: str
    location: Tuple[int, int] = (0, 0)


class Links(UserList[Link]):
    @property
    def new_src_list(self) -> list[str]:
        return [link.new_src for link in self.data]

    @property
    def only_src_list(self) -> list[str]:
        return [link.src for link in self.data]


@dataclass
class FixImg:
    html: str
    resource_prefix: str
    new_html: str = ''
    links: Links[Link] = field(default_factory=Links)

    def __post_init__(self):
        compute_calculated_fields(self)


def extract_img_alt_src(tag: str) -> tuple[str, str]:
    """Extract alt and src attributes from an <img> tag, return ('', '') if missing."""
    alt_match = re.search(r'alt=["\']([^"\']*)["\']', tag)
    src_match = re.search(r'src=["\']([^"\']*)["\']', tag)
    alt = alt_match.group(1) if alt_match else ''
    src = src_match.group(1) if src_match else ''
    return alt, src


def compute_calculated_fields(fix_img: FixImg) -> None:
    html, resource_prefix = fix_img.html, fix_img.resource_prefix
    # Find all <img ...> tags and their positions
    img_matches = list(re.finditer(r'<img[^>]*>', html))
    alt_counts = defaultdict(int)
    alt_indices = defaultdict(int)
    img_info = []
    for match in img_matches:
        tag = match.group(0)
        start, end = match.start(), match.end()
        alt, src = extract_img_alt_src(tag)
        img_info.append((alt, src, (start, end)))
        alt_counts[alt] += 1
    result = []
    for alt, src, location in img_info:
        if alt and alt_counts[alt] > 1:
            idx = alt_indices[alt]
            new_src = f"{resource_prefix}{alt.replace('.', f'-{idx:02}.')}"
            alt_indices[alt] += 1
        elif alt:
            new_src = f"{resource_prefix}{alt}"
        else:
            new_src = ''
        result.append(Link(new_src, src, location))
    fix_img.links = Links(result)

    # Generate new_html: replace each <img ...> with <img src="new_src">
    new_html_parts = []
    last_idx = 0
    for link in fix_img.links:
        start, end = link.location
        new_html_parts.append(html[last_idx:start])
        new_html_parts.append(f'<img src="{link.new_src}">')
        last_idx = end
    new_html_parts.append(html[last_idx:])
    fix_img.new_html = ''.join(new_html_parts)

