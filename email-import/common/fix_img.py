from dataclasses import dataclass, field


@dataclass
class Link:
    new_alt: str


def compute_links(html, resource_prefix) -> list[Link]:
    return []


@dataclass
class FixImg:
    html: str
    resource_prefix: str
    links: list[Link] = field(default_factory=list)

    def __post_init__(self):
        self.links = compute_links(self.html, self.resource_prefix)
