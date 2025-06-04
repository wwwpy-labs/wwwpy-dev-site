from dataclasses import dataclass, field
import re
from collections import defaultdict, UserList
from typing import Tuple


@dataclass
class Link:
    alt: str
    src: str
    location: Tuple[int, int]
    width: str
    height: str
    new_src: str


class Links(UserList[Link]):
    @property
    def new_src_list(self) -> list[str]:
        return [link.new_src for link in self.data]

    @property
    def only_src_list(self) -> list[str]:
        return [link.src for link in self.data]

    @property
    def only_width_list(self) -> list[str]:
        return [link.width for link in self.data]

    @property
    def only_height_list(self) -> list[str]:
        return [link.height for link in self.data]


@dataclass
class FixImg:
    html: str
    resource_prefix: str
    new_html: str = ''
    links: Links[Link] = field(default_factory=Links)

    def __post_init__(self):
        compute_calculated_fields(self)

    @property
    def recap_img_html(self) -> str:
        parts = []
        for link in self.links:
            parts.append(f'<div>{link.new_src}</div>')

            start, end = link.location
            original_link = self.html[start:end]
            parts.append(original_link)

        return "\n".join(parts)


def extract_img_alt_src(tag: str) -> tuple[str, str]:
    """Extract alt and src attributes from an <img> tag, return ('', '') if missing."""
    return extract_attribute_from_snippet(tag, 'alt'), extract_attribute_from_snippet(tag, 'src')


def extract_attribute_from_snippet(snippet: str, attr: str) -> str:
    """Extract the value of a specific attribute from an HTML snippet."""
    match = re.search(rf'{attr}=["\']([^"\']*)["\']', snippet)
    return match.group(1) if match else ''


def extract_attribute(tag: str, *attrs: str) -> tuple[str, ...]:
    """Extract multiple attributes from an HTML tag."""
    return tuple(extract_attribute_from_snippet(tag, attr) for attr in attrs)


def compute_calculated_fields(fix_img: FixImg) -> None:
    html, resource_prefix = fix_img.html, fix_img.resource_prefix
    # Find all <img ...> tags and their positions
    img_matches = list(re.finditer(r'<img[^>]*>', html))
    alt_counts = defaultdict(int)
    alt_indices = defaultdict(int)
    img_info = []
    result = []
    for match in img_matches:
        tag = match.group(0)
        start, end = match.start(), match.end()
        alt, src, width, height = extract_attribute(tag, 'alt', 'src', 'width', 'height')
        img_info.append((alt, src, (start, end), width, height))
        alt_counts[alt] += 1
        result.append(Link(alt, src, (start, end), width, height, ''))

    for link in result:
        alt, src = link.alt, link.src
        if alt and alt_counts[alt] > 1:
            idx = alt_indices[alt]
            new_src = f"{resource_prefix}{alt.replace('.', f'-{idx:02}.')}"
            alt_indices[alt] += 1
        elif alt:
            new_src = f"{resource_prefix}{alt}"
        else:
            new_src = ''
        link.new_src = new_src
    fix_img.links = Links(result)

    # Generate new_html: replace each <img ...> with <img src="new_src" width="..." height="...">
    new_html_parts = []
    last_idx = 0
    for link in fix_img.links:
        start, end = link.location
        new_html_parts.append(html[last_idx:start])
        attrs = [f'src="{link.new_src}"']
        if link.width:
            attrs.append(f'width="{link.width}"')
        if link.height:
            attrs.append(f'height="{link.height}"')
        new_html_parts.append(f'<img {" ".join(attrs)}>')
        last_idx = end
    new_html_parts.append(html[last_idx:])
    fix_img.new_html = ''.join(new_html_parts)
