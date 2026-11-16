#!/usr/bin/env python3
"""Generate editorial hero images for articles that don't have one yet.

Usage: python3 scripts/gen_article_images.py [N]   (default N=5)

Reads prompt + alt config from article_images.py, generates up to N images for
slugs missing assets/articles/<slug>.webp via the OpenAI image API (auth is
injected by the environment's HTTPS proxy, so no key is handled here), converts
to web-optimized .webp, and saves them. Idempotent: already-generated images are
skipped, so this can run daily until the backlog is cleared.
"""
import os, sys, json, base64, subprocess, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
from article_images import ARTICLE_IMAGES, STYLE  # noqa: E402

MODEL = "gpt-image-2"
N = int(sys.argv[1]) if len(sys.argv) > 1 else 5
OUT = os.path.join(ROOT, "assets", "articles")
os.makedirs(OUT, exist_ok=True)

todo = [s for s in ARTICLE_IMAGES if not os.path.exists(os.path.join(OUT, f"{s}.webp"))][:N]
if not todo:
    print("All article images already generated — nothing to do.")
    sys.exit(0)

print(f"Generating {len(todo)} image(s): {', '.join(todo)}")
made = []
for slug in todo:
    prompt = STYLE + ARTICLE_IMAGES[slug]["prompt"]
    payload = {"model": MODEL, "prompt": prompt, "size": "1536x1024", "quality": "medium", "n": 1}
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(payload, f)
        pf = f.name
    try:
        r = subprocess.run(
            ["curl", "-sS", "--max-time", "240", "-X", "POST",
             "https://api.openai.com/v1/images/generations",
             "-H", "Content-Type: application/json", "-d", "@" + pf],
            capture_output=True, text=True)
        data = json.loads(r.stdout or "{}")
    except Exception as e:  # noqa: BLE001
        print(f"  FAIL {slug}: {e}")
        continue
    finally:
        os.unlink(pf)
    if data.get("error") or not data.get("data"):
        print(f"  FAIL {slug}: {data.get('error')}")
        continue
    png = os.path.join(OUT, f"{slug}.png")
    with open(png, "wb") as f:
        f.write(base64.b64decode(data["data"][0]["b64_json"]))
    webp = os.path.join(OUT, f"{slug}.webp")
    subprocess.run(["convert", png, "-resize", "1536x", "-quality", "82", "-strip", webp], check=True)
    os.remove(png)
    made.append(slug)
    print(f"  OK {slug} -> assets/articles/{slug}.webp")

print(f"Done. Generated {len(made)} image(s).")
