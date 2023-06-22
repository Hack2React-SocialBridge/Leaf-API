from __future__ import annotations

from pathlib import Path

from jinja2 import Environment, FileSystemLoader

env = Environment(
    loader=FileSystemLoader(
        Path("leaf/static/templates/emails"),
    ),
)
