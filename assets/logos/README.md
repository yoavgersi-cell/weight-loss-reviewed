# Provider logos

Drop each provider's logo in this folder, named by the provider **slug**.
`build.py` picks it up automatically on the next `python3 build.py` — no code
changes needed. If a logo is missing, the site simply shows the provider's
text name (nothing breaks).

## Exact filenames to use

| Provider | Filename (any one extension) |
|----------|------------------------------|
| Embody   | `embody.svg` / `embody.png` / `embody.webp` |
| Ro       | `ro.svg` / `ro.png` / `ro.webp` |
| AltRx    | `altrx.svg` / `altrx.png` / `altrx.webp` |
| TrimRx   | `trimrx.svg` / `trimrx.png` / `trimrx.webp` |
| BMIMD    | `bmimd.svg` / `bmimd.png` / `bmimd.webp` |

Accepted extensions (checked in this order): `svg`, `png`, `webp`, `jpg`, `jpeg`.

## Tips for best results

- **SVG or transparent PNG** looks best (no white box around the logo).
- Logos render at ~30–46px tall; a **wordmark** (name-style) logo reads better
  than a tiny icon in the comparison chart.
- Aim for a transparent background so it sits cleanly on white and tinted cards.
