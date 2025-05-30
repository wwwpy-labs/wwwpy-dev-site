# wwwpy-dev-site

## Quick Start

1. Clone with submodules:
    ```bash
    git clone --recurse-submodules git@github.com:wwwpy-labs/wwwpy-dev-site.git
    cd wwwpy-dev-site
    ```

2. Install UV environment:
    https://docs.astral.sh/uv/getting-started/installation/
    ```bash
    uv sync
    ```

3. Build the site:

    ```bash
    source .venv/bin/activate
    cd pelican-site
    pelican
    pelican --listen
    ```

