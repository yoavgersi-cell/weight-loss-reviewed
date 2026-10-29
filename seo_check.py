#!/usr/bin/env python3
"""
SEO health check for Weight Loss Reviewed.

Rebuilds the site, then audits the generated output. Deterministic — no
network, no live-site access (the build output in the repo is the source of
truth). Prints a PASS/FAIL report.

Exit code:
  0  -> all hard checks passed (warnings may still be printed)
  1  -> one or more hard checks failed

Run:  python3 seo_check.py
"""
import os, re, sys, json, subprocess, datetime, importlib

ROOT = os.path.dirname(os.path.abspath(__file__))
TODAY = datetime.date.today()
STALE_DAYS = 120  # flag any provider price not re-checked within this window

errors, warnings, notes = [], [], []
def err(m): errors.append(m)
def warn(m): warnings.append(m)
def note(m): notes.append(m)

# --- 1. build must succeed -------------------------------------------------
r = subprocess.run([sys.executable, "build.py"], cwd=ROOT, capture_output=True, text=True)
if r.returncode != 0:
    print("FATAL: build.py failed\n" + r.stderr[-2000:])
    sys.exit(1)

# import the data model for cross-checks
sys.path.insert(0, ROOT)
build = importlib.import_module("build")
DOMAIN = build.SITE["domain"]

def html_files():
    for base, _, files in os.walk(ROOT):
        if "/.git" in base or "/assets" in base:
            continue
        for f in files:
            if f.endswith(".html"):
                yield os.path.join(base, f)

pages = list(html_files())
note(f"{len(pages)} HTML pages generated")

# --- 2. per-page head hygiene ---------------------------------------------
REQUIRED = {
    "<title>": re.compile(r"<title>[^<]{5,}</title>"),
    "meta description": re.compile(r'<meta name="description" content="[^"]{20,}"'),
    "canonical": re.compile(r'<link rel="canonical" href="https://(?:www\.)?weightlossreviewed\.com'),
    "hreflang x-default": re.compile(r'hreflang="x-default"'),
    "robots meta": re.compile(r'<meta name="robots"'),
    "og:title": re.compile(r'property="og:title"'),
    "viewport": re.compile(r'name="viewport"'),
}
for p in pages:
    if os.path.basename(p) == "404.html":
        continue
    s = open(p, encoding="utf-8").read()
    rel = os.path.relpath(p, ROOT)
    for label, rx in REQUIRED.items():
        if not rx.search(s):
            err(f"[head] {rel}: missing {label}")

# --- 3. JSON-LD must all parse --------------------------------------------
ld_total = ld_bad = 0
for p in pages:
    s = open(p, encoding="utf-8").read()
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        ld_total += 1
        try:
            json.loads(block)
        except Exception as e:
            ld_bad += 1
            err(f"[schema] {os.path.relpath(p, ROOT)}: invalid JSON-LD ({str(e)[:60]})")
note(f"{ld_total} JSON-LD blocks, {ld_bad} invalid")

# --- 4. sitemap: valid, apex host, coverage, resolves ----------------------
smp = os.path.join(ROOT, "sitemap.xml")
if not os.path.exists(smp):
    err("[sitemap] sitemap.xml missing")
else:
    sm = open(smp, encoding="utf-8").read()
    if "<urlset" not in sm:
        err("[sitemap] not a <urlset> sitemap")
    locs = re.findall(r"<loc>([^<]+)</loc>", sm)
    note(f"{len(locs)} URLs in sitemap")
    for loc in locs:
        if not loc.startswith(DOMAIN):
            err(f"[sitemap] non-apex or wrong host: {loc}")
        path = loc[len(DOMAIN):] or "/"
        # resolve to a built file (cleanUrls: /x -> x.html, / -> index.html)
        if path == "/":
            cand = os.path.join(ROOT, "index.html")
        else:
            cand = os.path.join(ROOT, path.lstrip("/") + ".html")
            if not os.path.exists(cand):
                cand = os.path.join(ROOT, path.lstrip("/"), "index.html")
        if not os.path.exists(cand):
            err(f"[sitemap] {loc} does not resolve to a built page")

# --- 5. robots.txt + llms.txt ---------------------------------------------
rob = os.path.join(ROOT, "robots.txt")
if not os.path.exists(rob):
    err("[robots] robots.txt missing")
else:
    rs = open(rob).read()
    if f"{DOMAIN}/sitemap.xml" not in rs:
        err("[robots] robots.txt does not reference the apex sitemap")
    for bot in ("GPTBot", "PerplexityBot", "ClaudeBot", "Google-Extended"):
        if bot not in rs:
            warn(f"[robots] AI crawler not explicitly welcomed: {bot}")
if not os.path.exists(os.path.join(ROOT, "llms.txt")):
    warn("[geo] llms.txt missing")

# --- 6. broken internal links + orphan pages -------------------------------
def resolves(href):
    href = href.split("#")[0].split("?")[0]
    if not href.startswith("/") or href.startswith("//"):
        return True  # external / anchor — skip
    if href in ("/",):
        return True
    p = href.lstrip("/")
    return (os.path.exists(os.path.join(ROOT, p + ".html"))
            or os.path.exists(os.path.join(ROOT, p))
            or os.path.exists(os.path.join(ROOT, p, "index.html")))

KNOWN_REDIRECTS = set()
vj = os.path.join(ROOT, "vercel.json")
if os.path.exists(vj):
    for red in json.load(open(vj)).get("redirects", []):
        KNOWN_REDIRECTS.add(red.get("source", ""))

broken = 0
for p in pages:
    s = open(p, encoding="utf-8").read()
    for href in set(re.findall(r'href="(/[^"]*)"', s)):
        if href.startswith("/assets/"):
            continue
        base = href.split("#")[0].split("?")[0]
        if base in KNOWN_REDIRECTS:
            continue
        if not resolves(href):
            broken += 1
            if broken <= 20:
                err(f"[links] {os.path.relpath(p, ROOT)} -> {href} (no such page)")
if broken:
    err(f"[links] {broken} broken internal link(s) total")

# orphans: built review/guide pages not linked from anywhere
linked = set()
for p in pages:
    s = open(p, encoding="utf-8").read()
    for href in re.findall(r'href="(/[^"#?]*)"', s):
        linked.add(href)
for slug in build.PROVIDER_ORDER:
    if build.review_url(slug) not in linked:
        warn(f"[orphan] review not linked internally: {build.review_url(slug)}")

# --- 7. stale price data ---------------------------------------------------
MONTHS = {m: i for i, m in enumerate(
    ["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"], 1)}
def parse_asof(s):
    s = s.strip().lower()
    m = re.match(r"([a-z]{3})[a-z]*\s+(\d{4})", s)
    if m and m.group(1)[:3] in MONTHS:
        return datetime.date(int(m.group(2)), MONTHS[m.group(1)[:3]], 1)
    m = re.match(r"(\d{4})$", s)
    if m:
        return datetime.date(int(m.group(1)), 1, 1)
    return None
for slug in build.PROVIDER_ORDER:
    d = build.PDATA[slug]
    ao = d.get("as_of", "")
    dt = parse_asof(ao)
    if not ao:
        warn(f"[price] {slug}: no as_of date")
    elif dt and (TODAY - dt).days > STALE_DAYS:
        warn(f"[price] {slug}: price last checked {ao} (>{STALE_DAYS}d ago) — re-verify")

# --- report ----------------------------------------------------------------
print("=" * 60)
print(f"SEO health check — {TODAY.isoformat()}")
print("=" * 60)
for m in notes:
    print("  ·", m)
if warnings:
    print(f"\nWARNINGS ({len(warnings)}):")
    for m in warnings:
        print("  ⚠ ", m)
if errors:
    print(f"\nFAILURES ({len(errors)}):")
    for m in errors:
        print("  ✗ ", m)
    print("\nRESULT: FAIL")
    sys.exit(1)
print(f"\nRESULT: PASS" + (f" (with {len(warnings)} warning(s))" if warnings else ""))
sys.exit(0)
