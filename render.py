"""Render the BetterAstralParty README, as GitHub shows it, into BetterAstralParty/index.html."""
import html
import json
import os
import pathlib
import re
import urllib.request

REPO = "TSM701/BetterAstralParty"
PAGE = "https://tsm701.github.io/BetterAstralParty/"
BANNER = "https://raw.githubusercontent.com/TSM701/BetterAstralParty/main/.github/assets/banner.png"
CSS = "https://cdn.jsdelivr.net/npm/github-markdown-css@5.8.1/github-markdown.min.css"


def api(path, accept):
    headers = {"Accept": accept, "X-GitHub-Api-Version": "2022-11-28", "User-Agent": "tsm701.github.io"}
    if os.environ.get("GH_TOKEN"):
        headers["Authorization"] = "Bearer " + os.environ["GH_TOKEN"]
    with urllib.request.urlopen(urllib.request.Request("https://api.github.com" + path, headers=headers)) as reply:
        return reply.read().decode("utf-8")


body = api(f"/repos/{REPO}/readme", "application/vnd.github.html+json")
description = json.loads(api(f"/repos/{REPO}", "application/vnd.github+json"))["description"] or ""

# GitHub prefixes heading ids with user-content- and maps #links to them with its own script.
body = body.replace('id="user-content-', 'id="')
# Repository-relative links point into the repository on GitHub.
body = re.sub(r'(href|src)="(?!https?:|#|mailto:|data:)([^"]+)"',
              lambda m: f'{m.group(1)}="https://github.com/{REPO}/blob/main/{m.group(2)}"', body)
assert "markdown-body" in body and 'id="user-content-' not in body

title = html.escape(f"BetterAstralParty | {description}" if description else "BetterAstralParty")
desc = html.escape(description)
page = f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{PAGE}">
<meta property="og:type" content="website">
<meta property="og:title" content="BetterAstralParty">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{PAGE}">
<meta property="og:image" content="{BANNER}">
<link rel="stylesheet" href="{CSS}">
<style>
body {{ margin: 0; background: #ffffff; }}
@media (prefers-color-scheme: dark) {{ body {{ background: #0d1117; }} }}
.markdown-body {{ box-sizing: border-box; min-width: 200px; max-width: 980px; margin: 0 auto; padding: 45px; }}
@media (max-width: 767px) {{ .markdown-body {{ padding: 16px; }} }}
.markdown-body .source {{ text-align: center; }}
</style>
</head>
<body>
{body}
<div class="markdown-body"><hr><p class="source"><a href="https://github.com/{REPO}">GitHub에서 보기 · View on GitHub</a></p></div>
</body>
</html>
"""
out = pathlib.Path(__file__).parent / "BetterAstralParty" / "index.html"
out.parent.mkdir(exist_ok=True)
out.write_text(page, encoding="utf-8", newline="\n")
print(f"wrote {out} ({len(page)} bytes)")
