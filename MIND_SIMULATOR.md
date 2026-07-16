# Mind simulator renderer

This repo renders Walter / Faltz009 from public-safe ORI aggregate receipts, a visible X profile scrape, and Walter's public Substack surface.

Files:

- `profile.json` — base ORI professor metadata.
- `data/walter-public-summary.json` — derived summary from ORI metadata, x-satellite counts, and public Substack surface. Raw dumps are not committed.
- `data/mind-memory.json` — projection memory: voice model, thesis, sections, and receipt-backed claims.
- `scripts/render_mind_profile.py` — deterministic renderer.

Run:

```bash
python3 scripts/render_mind_profile.py
```

Boundary checks before publishing:

- no raw Discord text
- no numeric Discord IDs
- no `*.ndjson` or `*.jsonl`
- no `.env` or credential files
- no claim that Closure/S3/geometry work is accepted science
- no private identity or affiliation claims

The renderer is dull because the judgment belongs in `data/mind-memory.json`.
