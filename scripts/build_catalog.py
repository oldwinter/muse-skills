#!/usr/bin/env python3
"""Build catalog/skills.json and catalog/INDEX.md from skills/."""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
CONFIG = ROOT / "config" / "skills.yaml"
SCOPES = ROOT / "runtime" / "skill-scopes.conf"
OUT_JSON = ROOT / "catalog" / "skills.json"
OUT_INDEX = ROOT / "catalog" / "INDEX.md"

GROUPS = {
    "workflow": [
        "wide-research",
        "goals",
        "skill-creator",
        "self-awareness",
        "forget",
        "muse_db",
    ],
    "artifacts": [
        "artifacts/document",
        "artifacts/markdown",
        "artifacts/pdf",
        "artifacts/presentation",
        "artifacts/spreadsheet",
        "artifacts/testing",
    ],
    "travel": [
        "travel-planning",
        "booking",
        "places-search",
        "duffel",
        "flightaware",
        "opentable",
        "ticketmaster",
    ],
    "office": [
        "gmail",
        "google-calendar",
        "google-contacts",
        "google-docs",
        "google-drive",
        "google-forms",
        "google-sheets",
        "google-slides",
        "google-tasks",
        "outlook-calendar",
        "outlook-contacts",
        "outlook-mail",
        "notion",
        "granola",
        "muse-mail",
        "calendly",
    ],
    "social": [
        "facebook-cli",
        "instagram",
        "instagram-messages",
        "messenger",
        "threads",
        "threads-messages",
    ],
    "commerce": ["shopping", "printify", "plaid"],
    "health": [
        "apple-healthkit",
        "google-health-connect",
        "function-health",
        "healthex",
        "peloton",
        "withings",
    ],
    "media": [
        "image-search",
        "media-library",
        "spotify",
        "generate_podcast",
        "magic-moment",
        "tts",
        "voice-design",
        "voice-selector",
    ],
    "devices": [
        "device-data",
        "wearable-device-skills",
        "wearables-comms",
        "philips-hue",
        "tessie",
        "tailscale",
    ],
    "product": [
        "muse-early-access",
        "muse-feedback",
        "share-ideas",
        "subscription-status",
    ],
}

GROUP_TITLES = {
    "workflow": "工作流与记忆",
    "artifacts": "文档、表格与产物验收",
    "travel": "旅行、地点与预订",
    "office": "办公、邮箱与知识库",
    "social": "社交与消息",
    "commerce": "购物与金融数据",
    "health": "健康与健身",
    "media": "图像、音频与视频",
    "devices": "设备、通信与网络",
    "product": "Muse 产品操作",
}

ALIASES = {
    "facebook": "facebook-cli",
    "meta-threads": "threads",
    "podcast": "generate_podcast",
    "voice-calls": "voice-selector",
}


def parse_frontmatter(text: str) -> dict:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}
    block = text[4:end]
    data = {}
    for key in ("name", "description", "icon", "title", "category"):
        match = re.search(rf"^{key}:\s*(.*)$", block, re.M)
        if not match:
            continue
        data[key] = match.group(1).strip().strip('"').strip("'")
    data["include_in_prompt"] = bool(
        re.search(r"includeInPrompt[\"'\s:]*true", block)
    )
    return data


def parse_skills_yaml(text: str) -> dict:
    entries = {}
    current = None
    for line in text.splitlines():
        key = re.match(r"^  ([A-Za-z0-9_]+):\s*$", line)
        if key:
            current = key.group(1)
            entries[current] = {}
            continue
        status = re.match(r"^    status:\s*(\S+)\s*$", line)
        if status and current:
            entries[current]["status"] = status.group(1)
    return entries


def manifest_stats(text: str) -> dict:
    connector = ""
    display = ""
    for line in text.splitlines():
        if line.startswith("connector:"):
            connector = line.split(":", 1)[1].strip()
        elif line.startswith("display_name:"):
            display = line.split(":", 1)[1].strip().strip('"')
    return {
        "connector": connector,
        "display_name": display,
        "default_allow": len(re.findall(r"^\s+default:\s+allow\s*$", text, re.M)),
        "default_ask": len(re.findall(r"^\s+default:\s+ask\s*$", text, re.M)),
    }


def scope_names(text: str) -> set:
    names = set()
    for line in text.splitlines():
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        names.update(parts[1:])
    return names


def skill_records():
    group_of = {path: name for name, paths in GROUPS.items() for path in paths}
    records = []
    seen = set()
    for path in sorted(SKILLS.rglob("SKILL.md")):
        rel = path.relative_to(SKILLS)
        if path.is_symlink():
            continue
        skill_id = str(rel.parent)
        seen.add(skill_id)
        front = parse_frontmatter(path.read_text(encoding="utf-8"))
        manifest_path = path.parent / "manifest.yaml"
        has_manifest = manifest_path.is_file() and not manifest_path.is_symlink()
        manifest = (
            manifest_stats(manifest_path.read_text(encoding="utf-8"))
            if has_manifest
            else None
        )
        has_eval = any(path.parent.rglob("eval/*"))
        records.append(
            {
                "id": skill_id,
                "group": group_of.get(skill_id),
                "name": front.get("name", ""),
                "description": front.get("description", ""),
                "icon": front.get("icon", ""),
                "title": front.get("title", ""),
                "include_in_prompt": front.get("include_in_prompt", False),
                "has_manifest": has_manifest,
                "has_eval": has_eval,
                "manifest": manifest,
                "path": f"skills/{skill_id}/SKILL.md",
            }
        )
    return records, seen, group_of


def availability(records):
    raw = parse_skills_yaml(CONFIG.read_text(encoding="utf-8"))
    ids = {item["id"] for item in records}
    mapped = []
    unmatched = []
    for key, body in raw.items():
        candidate = key.replace("_", "-")
        if candidate in ids:
            mapped.append({"config_key": key, "skill_id": candidate, **body})
        elif key == "messenger_read" and "messenger" in ids:
            mapped.append(
                {
                    "config_key": key,
                    "skill_id": "messenger",
                    "note": "config key does not match the directory name",
                    **body,
                }
            )
        else:
            unmatched.append(key)
    configured = {item["skill_id"] for item in mapped}
    return mapped, unmatched, sorted(ids - configured)


def render_index(records, aliases) -> str:
    by_group = {name: [] for name in GROUPS}
    for item in records:
        by_group[item["group"]].append(item)
    lines = [
        "# 技能索引",
        "",
        "由 `python3 scripts/build_catalog.py` 从 `skills/` 生成。不要手改。",
        "",
    ]
    for name, items in by_group.items():
        lines.append(f"## {GROUP_TITLES[name]}")
        lines.append("")
        lines.append("| 技能 | 是否进 prompt | manifest | eval | 说明 |")
        lines.append("| --- | --- | --- | --- | --- |")
        for item in items:
            prompt = "是" if item["include_in_prompt"] else ""
            manifest = "有" if item["has_manifest"] else ""
            evals = "有" if item["has_eval"] else ""
            desc = item["description"].replace("|", "\\|")
            lines.append(
                f"| [{item['id']}](../{item['path']}) | {prompt} | {manifest} | {evals} | {desc} |"
            )
        lines.append("")
    lines.append("## 别名")
    lines.append("")
    lines.append("| 入口 | 指向 |")
    lines.append("| --- | --- |")
    for alias, target in aliases.items():
        lines.append(f"| `{alias}` | `{target}` |")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    records, seen, group_of = skill_records()
    missing_group = sorted(seen - set(group_of))
    extra_group = sorted(set(group_of) - seen)
    problems = []
    if missing_group:
        problems.append(f"skills without a group: {', '.join(missing_group)}")
    if extra_group:
        problems.append(f"group entries with no SKILL.md: {', '.join(extra_group)}")
    for item in records:
        if not item["name"] or not item["description"]:
            problems.append(f"{item['id']} is missing name or description")
    for alias, target in ALIASES.items():
        link = SKILLS / alias / "SKILL.md"
        if not link.is_symlink():
            problems.append(f"{alias}/SKILL.md is not a symlink")
            continue
        if link.read_text(encoding="utf-8")[:1] == "-":
            pass
        if target not in seen:
            problems.append(f"alias {alias} points at missing {target}")
    mapped, unmatched, unconfigured = availability(records)
    scope_only = sorted(scope_names(SCOPES.read_text(encoding="utf-8")) - seen)
    catalog = {
        "source": "https://github.com/win4r/MuseAI-Skills",
        "skill_count": len(records),
        "alias_count": len(ALIASES),
        "include_in_prompt": sum(1 for item in records if item["include_in_prompt"]),
        "with_manifest": sum(1 for item in records if item["has_manifest"]),
        "with_eval": sum(1 for item in records if item["has_eval"]),
        "groups": {name: GROUPS[name] for name in GROUPS},
        "skills": records,
        "aliases": ALIASES,
        "availability": mapped,
        "availability_unmatched": unmatched,
        "skills_without_availability_entry": unconfigured,
        "channel_scope_names_absent_from_this_tree": scope_only,
    }
    text = json.dumps(catalog, ensure_ascii=False, indent=2) + "\n"
    index = render_index(records, ALIASES)
    if "--check" in sys.argv:
        same = OUT_JSON.read_text(encoding="utf-8") == text and OUT_INDEX.read_text(
            encoding="utf-8"
        ) == index
        if problems or not same:
            for problem in problems:
                print(problem, file=sys.stderr)
            if not same:
                print("catalog is stale; run python3 scripts/build_catalog.py", file=sys.stderr)
            return 1
        print(f"ok {len(records)} skills")
        return 0
    if problems:
        for problem in problems:
            print(problem, file=sys.stderr)
        return 1
    OUT_JSON.write_text(text, encoding="utf-8")
    OUT_INDEX.write_text(index, encoding="utf-8")
    print(
        f"skills={len(records)} prompt={catalog['include_in_prompt']} "
        f"manifest={catalog['with_manifest']} eval={catalog['with_eval']} "
        f"unconfigured={len(unconfigured)} scope_only={len(scope_only)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
