#!/usr/bin/env python3
"""Mechanical Obsidian clip processing helpers.

This script intentionally uses only the Python standard library. The vault's
front matter is simple enough that a small line-oriented parser is more reliable
than adding a package dependency to Codex runtimes that may not include PyYAML.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")


CLIP_DIR = Path("main/10_clip")
DONE_DIR = Path("main/11_clip_done")
SUMMARY_DIR = Path("main/20_ai_summary")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def rel(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def split_front_matter(content: str) -> tuple[str, str]:
    lines = content.splitlines()
    if not lines or lines[0].strip() != "---":
        return "", content

    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            front = "\n".join(lines[1:index])
            body = "\n".join(lines[index + 1 :]).lstrip("\n")
            return front, body

    return "", content


def quote_yaml(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def scalar_value(front: str, key: str) -> str:
    prefix = f"{key}:"
    for line in front.splitlines():
        stripped = line.strip()
        if stripped.startswith(prefix):
            value = stripped[len(prefix) :].strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
                return value[1:-1]
            return value
    return ""


def extract_tags(front: str) -> list[str]:
    lines = front.splitlines()
    for index, line in enumerate(lines):
        if line.strip() == "tags:":
            tags: list[str] = []
            for tag_line in lines[index + 1 :]:
                stripped = tag_line.strip()
                if not stripped:
                    continue
                if not stripped.startswith("- "):
                    break
                value = stripped[2:].strip()
                if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
                    value = value[1:-1]
                tags.append(value)
            return tags

        if line.strip().startswith("tags:") and line.strip() != "tags:":
            value = line.split(":", 1)[1].strip()
            if value.startswith("[") and value.endswith("]"):
                raw_tags = value[1:-1].split(",")
                return [tag.strip().strip("'\"") for tag in raw_tags if tag.strip()]

    return []


def field_block_end(lines: list[str], start: int) -> int:
    end = start + 1
    while end < len(lines):
        stripped = lines[end].strip()
        if not stripped:
            end += 1
            continue
        if lines[end].startswith((" ", "\t")):
            end += 1
            continue
        break
    return end


def replace_scalar(lines: list[str], key: str, value: str) -> list[str]:
    prefix = f"{key}:"
    replacement = f"{key}: {quote_yaml(value)}"
    for index, line in enumerate(lines):
        if line.strip().startswith(prefix):
            end = field_block_end(lines, index)
            return lines[:index] + [replacement] + lines[end:]
    return lines + [replacement]


def replace_tags(lines: list[str], tags: list[str]) -> list[str]:
    block = ["tags:"] + [f"  - {quote_yaml(tag)}" for tag in tags]
    for index, line in enumerate(lines):
        if line.strip().startswith("tags:"):
            end = field_block_end(lines, index)
            return lines[:index] + block + lines[end:]
    return lines + block


def add_tag_to_front(front: str, tag: str) -> str:
    tags = extract_tags(front)
    if tag not in tags:
        tags.append(tag)
    return "\n".join(replace_tags(front.splitlines(), tags))


def update_original_tag(content: str, tag: str) -> str:
    front, body = split_front_matter(content)
    if not front:
        front = "\n".join(["tags:", f"  - {quote_yaml(tag)}"])
    else:
        front = add_tag_to_front(front, tag)
    return f"---\n{front}\n---\n{body}"


def build_summary_content(source_content: str, description: str, tags: list[str], body: str) -> str:
    front, _ = split_front_matter(source_content)
    if not front:
        raise ValueError("source file is missing front matter")

    lines = front.splitlines()
    lines = replace_scalar(lines, "description", description)
    lines = replace_tags(lines, tags)
    summary_body = body.strip() + "\n"
    return f"---\n{'\n'.join(lines)}\n---\n\n{summary_body}"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_lines(root: Path, args: list[str]) -> list[str]:
    result = subprocess.run(
        ["git", *args],
        cwd=root,
        check=True,
        text=True,
        encoding="utf-8",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return [line.strip().strip('"') for line in result.stdout.splitlines() if line.strip()]


def git_pathspec(path: Path, root: Path) -> str:
    return rel(path, root)


def is_tracked(path: Path, root: Path) -> bool:
    result = subprocess.run(
        ["git", "ls-files", "--error-unmatch", "--", git_pathspec(path, root)],
        cwd=root,
        text=True,
        encoding="utf-8",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.returncode == 0


def move_to_done(path: Path, root: Path) -> None:
    dest = root / DONE_DIR / path.name
    if dest.exists():
        raise FileExistsError(f"destination already exists: {rel(dest, root)}")

    if is_tracked(path, root):
        subprocess.run(
            ["git", "mv", "--", git_pathspec(path, root), git_pathspec(dest, root)],
            cwd=root,
            check=True,
            text=True,
            encoding="utf-8",
        )
    else:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(path), str(dest))


def remove_duplicate(path: Path, root: Path) -> None:
    if is_tracked(path, root):
        subprocess.run(
            ["git", "rm", "--", git_pathspec(path, root)],
            cwd=root,
            check=True,
            text=True,
            encoding="utf-8",
        )
    else:
        path.unlink()


def matching_done_file(path: Path, root: Path) -> str | None:
    source_hash = sha256(path)
    for done in sorted((root / DONE_DIR).glob("*.md")):
        if sha256(done) == source_hash:
            return rel(done, root)
    return None


def summary_sources(root: Path) -> set[str]:
    sources: set[str] = set()
    for summary in sorted((root / SUMMARY_DIR).glob("*.md")):
        front, _ = split_front_matter(read_text(summary))
        source = scalar_value(front, "source")
        if source:
            sources.add(source)
    return sources


def scan(root: Path) -> dict[str, object]:
    summaries_by_source = summary_sources(root)
    items = []
    for path in sorted((root / CLIP_DIR).glob("*.md")):
        content = read_text(path)
        front, _ = split_front_matter(content)
        source_url = scalar_value(front, "source")
        done_match = matching_done_file(path, root)
        item = {
            "path": rel(path, root),
            "title": scalar_value(front, "title"),
            "published": scalar_value(front, "published"),
            "created": scalar_value(front, "created"),
            "source": source_url,
            "tags": extract_tags(front),
            "tracked": is_tracked(path, root),
            "matching_done_file": done_match,
            "matching_summary_source": source_url in summaries_by_source if source_url else False,
        }
        item["classification"] = (
            "duplicate"
            if item["matching_done_file"] and item["matching_summary_source"]
            else "new"
        )
        items.append(item)

    return {
        "clip_count": len(items),
        "new_count": sum(1 for item in items if item["classification"] == "new"),
        "duplicate_count": sum(1 for item in items if item["classification"] == "duplicate"),
        "items": items,
    }


def apply_manifest(root: Path, manifest_path: Path) -> None:
    manifest = json.loads(read_text(manifest_path))

    for entry in manifest.get("summaries", []):
        source = root / Path(entry["source"])
        summary = root / Path(entry["summary"])
        if not source.exists():
            raise FileNotFoundError(entry["source"])
        if summary.exists():
            raise FileExistsError(entry["summary"])

        source_content = read_text(source)
        body = entry["body"]
        if isinstance(body, list):
            body = "\n".join(body)
        summary_content = build_summary_content(
            source_content=source_content,
            description=entry["description"],
            tags=entry["tags"],
            body=body,
        )
        write_text(summary, summary_content)
        write_text(source, update_original_tag(source_content, "raw"))
        move_to_done(source, root)

    for entry in manifest.get("duplicates", []):
        source = root / Path(entry["source"])
        if not source.exists():
            continue
        if not matching_done_file(source, root):
            raise RuntimeError(f"duplicate has no byte-identical done file: {entry['source']}")
        remove_duplicate(source, root)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Process Obsidian clip markdown files.")
    parser.add_argument("--root", default=".", help="Repository root")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("scan", help="Inspect clips and print JSON")

    apply_parser = subparsers.add_parser("apply", help="Apply a JSON processing manifest")
    apply_parser.add_argument("--manifest", required=True, help="Path to manifest JSON")

    args = parser.parse_args(argv)
    root = Path(args.root).resolve()

    if args.command == "scan":
        print(json.dumps(scan(root), ensure_ascii=False, indent=2))
        return 0

    if args.command == "apply":
        apply_manifest(root, Path(args.manifest).resolve())
        return 0

    raise AssertionError(args.command)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
