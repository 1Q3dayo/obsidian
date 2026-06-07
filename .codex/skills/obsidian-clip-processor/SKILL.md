---
name: obsidian-clip-processor
description: Summarize and archive Markdown web clips in this Obsidian knowledge base. Use when Codex needs to process files under main/10_clip by creating AI summary notes in main/20_ai_summary, adding raw tags to original clip front matter, moving processed clips into main/11_clip_done, detecting already-processed duplicates, or preserving this vault's README workflow.
---

# Obsidian Clip Processor

## Workflow

Use this skill for the Obsidian vault rooted at the repository directory. Read `README.md` first if the requested workflow may have changed.

1. Inspect `main/10_clip/*.md` with UTF-8 encoding.
2. Run `scripts/clip_ops.py scan --root <repo>` to classify clips as new or already processed.
3. For each new clip, create a concise Japanese summary note in `main/20_ai_summary`.
4. Copy the source front matter into the summary, then replace:
   - `description`: a very short Japanese summary.
   - `tags`: keep `clippings`, add `ai_summary`, and add 1-5 English content tags.
5. Name summary files as `yyyymmdd_<25-char-or-shorter Japanese title>.md`.
   - Prefer `published`.
   - Fall back to `created` only when `published` is missing.
6. Add `raw` to the original clip's `tags` before archiving it.
7. Move processed originals to `main/11_clip_done`.
   - Use `git mv` for tracked files.
   - Use a normal filesystem move for untracked files.
8. If a `10_clip` file is byte-identical to a file already in `11_clip_done` and a matching summary already exists, remove only the duplicate from `10_clip`.

## Script Usage

Use the bundled helper for validation and mechanical file operations:

```bash
python .codex/skills/obsidian-clip-processor/scripts/clip_ops.py scan --root .
python .codex/skills/obsidian-clip-processor/scripts/clip_ops.py apply --root . --manifest manifest.json
```

`apply` expects a JSON manifest:

```json
{
  "summaries": [
    {
      "source": "main/10_clip/example.md",
      "summary": "main/20_ai_summary/20260601_要約タイトル.md",
      "description": "記事内容の超要約。",
      "tags": ["clippings", "ai_summary", "example"],
      "body": "## 概要\n...\n"
    }
  ],
  "duplicates": [
    {
      "source": "main/10_clip/already-done.md"
    }
  ]
}
```

## Summary Style

Match the existing notes in `main/20_ai_summary`:

- Keep the body compact.
- Use `## 概要` and `## 主要ポイント`.
- Use short `###` subsections only when they improve scanning.
- Prefer factual summaries over commentary.
- Do not preserve article counters, reaction counts, embeds, or raw screenshots in the summary body.

## Validation

After processing, verify:

- `main/10_clip` has no remaining `.md` files.
- New summary notes contain `ai_summary` plus at least one English content tag.
- Archived originals contain `raw`.
- `git status --short --branch` shows expected additions, moves, and removals.
