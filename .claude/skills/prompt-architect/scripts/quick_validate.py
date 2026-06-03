#!/usr/bin/env python3
"""
Quick validation for prompt-architect artifacts (skills, commands, subagents).

Forked from skill-creator's quick_validate.py and extended to handle:
- skill  : directory containing SKILL.md
- command: single .md file under .claude/commands/
- subagent: single .md file under .claude/agents/

All three share the same frontmatter shape (name + description required, plus
optional license/allowed-tools/metadata/compatibility/model/hooks). The validator
checks the frontmatter against this superset.
"""

import argparse
import re
import sys
import textwrap
from pathlib import Path

# PyYAML is optional. These scripts are meant to run with zero third-party
# installs, so when PyYAML is absent we fall back to a small stdlib frontmatter
# parser that is sufficient for validation. Install PyYAML only if you want
# stricter YAML parsing — it is listed (commented) in the project-root
# requirements.txt as an optional convenience.
try:
    import yaml  # type: ignore
except ModuleNotFoundError:
    yaml = None


# Frontmatter fields allowed across all three artifact types. Kept in sync with
# the documented fields in references/{skill,command,subagent}-template.md — the
# validator must accept everything the templates teach (dogfooding).
ALLOWED_PROPERTIES = {
    # shared / skill / command
    "name", "description", "when_to_use", "license", "allowed-tools", "metadata",
    "compatibility", "model", "hooks", "disable-model-invocation", "argument-hint",
    "arguments", "context", "agent",
    # subagent
    "tools", "disallowedTools", "effort", "permissionMode", "isolation", "skills",
    "mcpServers", "memory", "maxTurns", "background", "color", "initialPrompt",
}


_TOP_KEY_RE = re.compile(r"^([A-Za-z_][\w-]*):(.*)$")
_BLOCK_INDICATORS = {"|", ">", "|-", ">-", "|+", ">+"}


def _load_frontmatter(text):
    """Parse YAML frontmatter into a dict. Uses PyYAML when installed, otherwise
    a stdlib fallback that extracts top-level keys (scalar and block-scalar
    values) — all this validator inspects."""
    if yaml is not None:
        return yaml.safe_load(text)
    return _parse_frontmatter_stdlib(text)


def _parse_frontmatter_stdlib(text):
    """Minimal, dependency-free frontmatter parser.

    Returns a dict of top-level keys. Scalar values come back as strings; block
    scalars (``key: |``) are dedented; nested mappings/sequences are collapsed to
    their (non-empty) text so the validator can still see the key is present.
    Intentionally not a general YAML parser — it only supports artifact
    frontmatter for the checks below.
    """
    result = {}
    lines = text.split("\n")
    i, n = 0, len(lines)
    while i < n:
        line = lines[i]
        if not line.strip() or line.lstrip().startswith("#") or line[:1].isspace():
            i += 1
            continue
        m = _TOP_KEY_RE.match(line)
        if not m:
            i += 1
            continue
        key, rest = m.group(1), m.group(2).strip()
        if rest in _BLOCK_INDICATORS or rest == "":
            block = []
            i += 1
            while i < n and (not lines[i].strip() or lines[i][:1].isspace()):
                block.append(lines[i])
                i += 1
            value = textwrap.dedent("\n".join(block)).strip()
            result[key] = value if value else None
        else:
            if len(rest) >= 2 and rest[0] in "\"'" and rest[-1] == rest[0]:
                rest = rest[1:-1]
            result[key] = rest
            i += 1
    return result


def resolve_md_path(artifact_path: Path) -> Path:
    """Resolve to the .md file holding the artifact's frontmatter."""
    if artifact_path.is_dir():
        return artifact_path / "SKILL.md"
    return artifact_path


def validate_artifact(artifact_path, artifact_type: str = "skill"):
    """Validate any artifact (skill / command / subagent) by frontmatter shape."""
    artifact_path = Path(artifact_path)

    if artifact_type == "skill" and not artifact_path.is_dir():
        return False, (f"Skill artifacts must be a directory containing SKILL.md "
                       f"(got file: {artifact_path}). Use --artifact-type command "
                       f"or --artifact-type subagent for single-file artifacts.")

    if artifact_type in ("command", "subagent") and not artifact_path.is_file():
        return False, (f"{artifact_type.capitalize()} artifacts must be a single .md "
                       f"file (got: {artifact_path}). Use --artifact-type skill for "
                       f"directory-format artifacts.")

    md_path = resolve_md_path(artifact_path)
    if not md_path.exists():
        return False, f"Artifact file not found: {md_path}"

    content = md_path.read_text()
    if not content.startswith("---"):
        return False, "No YAML frontmatter found"

    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format"

    frontmatter_text = match.group(1)
    try:
        frontmatter = _load_frontmatter(frontmatter_text)
    except Exception as e:  # PyYAML raises yaml.YAMLError; the stdlib fallback shouldn't raise
        return False, f"Invalid YAML in frontmatter: {e}"
    if not isinstance(frontmatter, dict):
        return False, "Frontmatter must be a YAML dictionary"

    unexpected_keys = set(frontmatter.keys()) - ALLOWED_PROPERTIES
    if unexpected_keys:
        return False, (
            f"Unexpected key(s) in frontmatter: {', '.join(sorted(unexpected_keys))}. "
            f"Allowed: {', '.join(sorted(ALLOWED_PROPERTIES))}"
        )

    if "name" not in frontmatter:
        return False, "Missing 'name' in frontmatter"
    if "description" not in frontmatter:
        return False, "Missing 'description' in frontmatter"

    name = frontmatter.get("name", "")
    if not isinstance(name, str):
        return False, f"Name must be a string, got {type(name).__name__}"
    name = name.strip()
    if name:
        if not re.match(r"^[a-z0-9-]+$", name):
            return False, f"Name '{name}' should be kebab-case (lowercase letters, digits, hyphens)"
        if name.startswith("-") or name.endswith("-") or "--" in name:
            return False, f"Name '{name}' cannot start/end with hyphen or contain consecutive hyphens"
        if len(name) > 64:
            return False, f"Name is too long ({len(name)} chars). Maximum is 64."

    description = frontmatter.get("description", "")
    if not isinstance(description, str):
        return False, f"Description must be a string, got {type(description).__name__}"
    description = description.strip()
    if description:
        if "<" in description or ">" in description:
            return False, "Description cannot contain angle brackets (< or >)"
        if len(description) > 1024:
            return False, f"Description is too long ({len(description)} chars). Maximum is 1024."

    compatibility = frontmatter.get("compatibility", "")
    if compatibility:
        if not isinstance(compatibility, str):
            return False, f"Compatibility must be a string, got {type(compatibility).__name__}"
        if len(compatibility) > 500:
            return False, f"Compatibility is too long ({len(compatibility)} chars). Maximum is 500."

    return True, f"{artifact_type.capitalize()} is valid!"


# Back-compat alias so package_skill.py's `from scripts.quick_validate import validate_skill` keeps working.
def validate_skill(skill_path):
    return validate_artifact(skill_path, "skill")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate an artifact's frontmatter")
    parser.add_argument("artifact_path", help="Path to skill directory or command/subagent .md file")
    parser.add_argument("--artifact-type", choices=["skill", "command", "subagent"], default="skill",
                        help="Artifact type. Skill = directory; command/subagent = single .md file.")
    args = parser.parse_args()

    valid, message = validate_artifact(args.artifact_path, args.artifact_type)
    print(message)
    sys.exit(0 if valid else 1)
