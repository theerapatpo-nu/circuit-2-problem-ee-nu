from __future__ import annotations

import re
import subprocess
from pathlib import Path


BASE = Path(__file__).resolve().parent
SRC = BASE / "ALL_SPANNING_TREES.md"
OUT = BASE / "image"
OUT.mkdir(parents=True, exist_ok=True)


EDGE_PATHS = {
    1: "M 177 180 C 132 153, 132 97, 187 75",
    2: "M 177 290 C 132 263, 132 207, 187 185",
    3: "M 200 70 L 200 180",
    4: "M 200 180 L 200 290",
    5: "M 520 70 L 200 70",
    6: "M 200 180 L 520 70",
    7: "M 520 180 L 200 180",
    8: "M 200 290 L 520 180",
    9: "M 200 290 L 520 290",
    10: "M 520 70 L 520 180",
    12: "M 520 180 L 520 290",
}

EDGE_LABELS = {
    1: (126, 132),
    2: (126, 242),
    3: (220, 132),
    4: (220, 242),
    5: (355, 53),
    6: (356, 123),
    7: (356, 166),
    8: (356, 236),
    9: (356, 316),
    10: (540, 132),
    12: (540, 242),
}


def parse_trees(md: str) -> list[tuple[int, tuple[int, ...]]]:
    rows: list[tuple[int, tuple[int, ...]]] = []
    for match in re.finditer(r"\|\s*(\d+)\s*\|\s*\{([^}]*)\}", md):
        idx = int(match.group(1))
        edges = tuple(int(x) for x in re.findall(r"\d+", match.group(2)))
        rows.append((idx, edges))
    rows.sort(key=lambda x: x[0])
    return rows


def svg_for_tree(idx: int, tree: tuple[int, ...]) -> str:
    twig_edges = set(tree)
    link_edges = set(EDGE_PATHS) - twig_edges
    twigs = ", ".join(str(x) for x in tree)
    twig_paths = "\n".join(
        f'    <path d="{EDGE_PATHS[e]}"/>' for e in sorted(twig_edges)
    )
    link_paths = "\n".join(
        f'    <path d="{EDGE_PATHS[e]}"/>' for e in sorted(link_edges)
    )
    labels = "\n".join(
        f'    <text x="{x}" y="{y}">{e}</text>' for e, (x, y) in EDGE_LABELS.items()
    )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="800" height="390" viewBox="0 0 800 390" role="img" aria-labelledby="title desc">
  <title id="title">Spanning tree {idx}</title>
  <desc id="desc">The directed graph for exercise 1.3 with twig branches {twigs} drawn as thick solid lines and links drawn as dashed lines.</desc>
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="8.4" refY="5" markerWidth="12" markerHeight="12" markerUnits="userSpaceOnUse" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#172033"/>
    </marker>
  </defs>
  <style>
    .twig {{ fill:none; stroke:#172033; stroke-width:7.5; stroke-linecap:round; stroke-linejoin:round; marker-end:url(#arrow); }}
    .link {{ fill:none; stroke:#172033; stroke-width:3; stroke-dasharray:9 7; stroke-linecap:round; stroke-linejoin:round; marker-end:url(#arrow); }}
    .node {{ fill:#172033; }}
    .node-name {{ font: italic 18px Georgia, serif; fill:#172033; }}
    .branch {{ font: 17px Arial, sans-serif; fill:#172033; }}
    .title {{ font: 700 23px Arial, sans-serif; fill:#172033; }}
    .note {{ font: 16px Arial, sans-serif; fill:#344056; }}
  </style>

  <rect width="800" height="390" fill="white"/>
  <text x="44" y="40" class="title">Spanning tree {idx:03d}</text>
  <text x="44" y="68" class="note">T = {{{twigs}}}; thick solid branches are twigs, dashed branches are links.</text>

  <g transform="translate(0 55)">
  <g class="link">
{link_paths}
  </g>

  <g class="twig">
{twig_paths}
  </g>

  <g class="branch">
{labels}
  </g>
  <g class="node">
    <circle cx="200" cy="70" r="8"/><circle cx="200" cy="180" r="8"/><circle cx="200" cy="290" r="8"/>
    <circle cx="520" cy="70" r="8"/><circle cx="520" cy="180" r="8"/><circle cx="520" cy="290" r="8"/>
  </g>
  <g class="node-name">
    <text x="183" y="54">A</text><text x="183" y="168">B</text><text x="183" y="316">C</text>
    <text x="532" y="54">D</text><text x="532" y="168">E</text><text x="532" y="316">F</text>
  </g>
  </g>

  <rect x="602" y="99" width="157" height="114" rx="10" fill="#f7f9fc" stroke="#d5dce8"/>
  <line x1="620" y1="130" x2="667" y2="130" stroke="#172033" stroke-width="7.5" stroke-linecap="round"/>
  <line x1="620" y1="169" x2="667" y2="169" stroke="#172033" stroke-width="3" stroke-dasharray="9 7" stroke-linecap="round"/>
  <text x="680" y="136" class="note">twig</text>
  <text x="680" y="175" class="note">link</text>
  <text x="602" y="250" class="note">6 nodes, 11 branches</text>
  <text x="602" y="274" class="note">|T| = n - 1 = 5</text>
</svg>
"""


def main() -> None:
    md = SRC.read_text(encoding="utf-8")
    trees = parse_trees(md)
    if len(trees) != 139:
        raise SystemExit(f"Expected 139 trees, found {len(trees)}")

    manifest = ["idx,tree,svg,png"]
    for idx, tree in trees:
        stem = f"tree-{idx:03d}"
        svg_path = OUT / f"{stem}.svg"
        png_path = OUT / f"{stem}.png"
        svg = svg_for_tree(idx, tree)
        svg_path.write_text(svg, encoding="utf-8")
        subprocess.run(
            ["rsvg-convert", "-o", str(png_path), str(svg_path)],
            check=True,
        )
        manifest.append(
            f'{idx},"{{{",".join(map(str, tree))}}}",{svg_path.name},{png_path.name}'
        )

    (OUT / "manifest.csv").write_text("\n".join(manifest) + "\n", encoding="utf-8")
    (OUT / "README.md").write_text(
        "# Generated spanning-tree images\n\n"
        "This folder contains 139 SVG and PNG files, one per spanning tree.\n"
        "File names use the numbering from ALL_SPANNING_TREES.md.\n\n"
        "Format convention: twigs are drawn as thick solid lines, while links are drawn as dashed lines. "
        "This convention is used so the tree graphs match the lecture format in "
        "../../lectures/303212S1Y2569lec01.pdf.\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
