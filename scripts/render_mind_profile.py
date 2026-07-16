#!/usr/bin/env python3
from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def esc(v: Any) -> str:
    return html.escape(str(v), quote=True)


def stats(summary: dict[str, Any]) -> list[tuple[str, Any]]:
    ori = summary["ori_discord"]
    xs = summary["x_satellite"]
    return [
        ("ORI public messages", ori["message_count"]),
        ("ORI active days", ori["active_days"]),
        ("visible x-satellite records", xs["total_records"]),
        ("authored Faltz009 records", xs["authored_records"]),
        ("visible X engagement", sum(xs["visible_metrics_total"].values())),
    ]


def render_readme(summary: dict[str, Any], mind: dict[str, Any], profile: dict[str, Any]) -> str:
    sections = "\n\n".join(f"## {s['heading']}\n\n{s['body']}" for s in mind["template"]["sections"])
    memory = "\n".join(f"- {m['name']}: {m['claim']}\n  - Receipt: {m['receipt']}" for m in mind["memory"])
    stat_rows = "\n".join(f"- {k}: `{v}`" for k, v in stats(summary))
    themes = "\n".join(f"| {k} | {v} |" for k, v in summary["x_satellite"]["theme_counts"].items())
    tweets = "\n".join(f"- {t.get('created_at')} — {t.get('text')} ([source]({t.get('url')}))" for t in summary["x_satellite"]["selected_public_tweets"][:10])
    channels = "\n".join(f"- {c['channel']}: {c['messages']} messages" for c in summary["ori_discord"]["top_channels"])
    mentions = "\n".join(f"- {m['handle']}: {m['count']} mentions" for m in summary["ori_discord"]["frequent_mentions"])
    posts = "\n".join(f"- {p}" for p in summary["substack_surface"]["observed_posts"])
    return f"""# {mind['display_name']}

> Modeled public projection for `Walter / Faltz009`. Built from ORI aggregate receipts, a visible X profile scrape, and public Substack surface data.

{mind['projection_boundary']}

---

# {mind['template']['hero_title']}

{mind['template']['hero_subtitle']}

{mind['core_thesis']}

{sections}

## What the receipts say

{stat_rows}

Professor gate:

```text
{profile['professor_gate']}
```

Public surfaces:

- X: https://x.com/Faltz009
- Substack: https://liminalgravity.substack.com/

## Memory loaded into the projection

{memory}

## Recurrent public signal counts

| Signal | Count proxy |
|---|---:|
{themes}

## Selected visible X receipts

{tweets}

## Public Substack surface

{posts}

## ORI channel surface

{channels}

## ORI mention surface

{mentions}

## Boundary

This page is a projection system output. It makes the best organized public version of the receipts legible. It does not publish the raw x-satellite NDJSON, raw Discord text, numeric Discord IDs, hidden replies, DMs, actor-level likes, credentials, or private identity claims.

Generated from `{mind['schema']}`.
"""


def render_html(summary: dict[str, Any], mind: dict[str, Any], profile: dict[str, Any]) -> str:
    css = ":root{color-scheme:dark;--bg:#05070b;--panel:#101724;--text:#f5f2e9;--muted:#aaaec0;--line:#273a59;--blue:#8bd3ff;--violet:#bda7ff;--gold:#e9c46a}*{box-sizing:border-box}body{margin:0;background:radial-gradient(circle at top left,#263b76 0,#05070b 34rem);color:var(--text);font-family:ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;line-height:1.58}main{max-width:1120px;margin:0 auto;padding:48px 20px 80px}.hero,.section,.card{border:1px solid var(--line);background:rgba(16,23,36,.9);border-radius:22px;padding:28px}.eyebrow{color:var(--blue);text-transform:uppercase;letter-spacing:.15em;font-size:.78rem;font-weight:900}h1{font-size:clamp(2.3rem,6vw,5rem);line-height:.95;margin:.35em 0;max-width:980px}h2{color:var(--blue);margin:0 0 12px}a{color:var(--blue)}.muted{color:var(--muted)}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:14px;margin:22px 0}.stack{display:grid;gap:16px}.metric{font-size:2rem;color:var(--gold);font-weight:950}.cta{display:inline-block;margin:14px 10px 0 0;background:var(--blue);color:#061019;text-decoration:none;padding:12px 17px;border-radius:999px;font-weight:950}.ghost{background:transparent;color:var(--blue);border:1px solid var(--blue)}blockquote{border-left:3px solid var(--violet);padding-left:14px;color:#e7e0f6}.receipt{font-size:.9rem;color:var(--muted)}"
    section_html = "".join(f"<section class='section'><h2>{esc(s['heading'])}</h2><p>{esc(s['body'])}</p></section>" for s in mind["template"]["sections"])
    cards = "".join(f"<div class='card'><div class='metric'>{esc(v)}</div><div>{esc(k)}</div></div>" for k, v in stats(summary)[:4])
    tweets = "".join(f"<blockquote>{esc(t.get('text'))}</blockquote><p class='receipt'>{esc(t.get('created_at'))} · <a href='{esc(t.get('url'))}'>source</a></p>" for t in summary["x_satellite"]["selected_public_tweets"][:5])
    return f"<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>{esc(mind['display_name'])} — mind projection</title><style>{css}</style></head><body><main><section class='hero'><div class='eyebrow'>Build In Public University · mind projection</div><h1>{esc(mind['template']['hero_title'])}</h1><p class='muted'>{esc(mind['template']['hero_subtitle'])}</p><p>{esc(mind['projection_boundary'])}</p><a class='cta' href='{esc(profile['professor_gate'])}'>Open professor gate →</a><a class='cta ghost' href='https://x.com/Faltz009'>X surface →</a><a class='cta ghost' href='https://liminalgravity.substack.com/'>Substack →</a></section><div class='grid'>{cards}</div><div class='stack'>{section_html}</div><section class='section'><h2>Selected X receipts</h2>{tweets}</section><section class='section'><h2>Boundary</h2><p>Raw dumps and raw Discord text stay out of this repo.</p></section></main></body></html>\n"


def main() -> None:
    summary = load_json(ROOT / "data/walter-public-summary.json")
    mind = load_json(ROOT / "data/mind-memory.json")
    profile = load_json(ROOT / "profile.json")
    profile["display_name"] = mind["display_name"]
    profile["aliases"] = ["Walter", "Faltz009", "Walter Henrique Alves da Silva"]
    profile["external_links"] = summary["public_links"]
    profile["privacy_boundary"] = summary["source_boundary"]
    profile["mind_projection"] = {
        "schema": mind["schema"],
        "display_name": mind["display_name"],
        "role": mind["role"],
        "core_thesis": mind["core_thesis"],
        "projection_boundary": mind["projection_boundary"],
        "voice_model": mind["voice_model"],
        "memory_items": len(mind["memory"]),
        "renderer": "scripts/render_mind_profile.py",
    }
    profile["x_satellite_enhancement"] = {
        "summary_path": "data/walter-public-summary.json",
        "x_handle": summary["x_handle"],
        "records": summary["x_satellite"]["total_records"],
        "authored_records": summary["x_satellite"]["authored_records"],
        "raw_dump_committed": False,
    }
    (ROOT / "README.md").write_text(render_readme(summary, mind, profile))
    (ROOT / "index.html").write_text(render_html(summary, mind, profile))
    (ROOT / "profile.json").write_text(json.dumps(profile, indent=2, ensure_ascii=False) + "\n")
    print("rendered mind projection for walter")


if __name__ == "__main__":
    main()
