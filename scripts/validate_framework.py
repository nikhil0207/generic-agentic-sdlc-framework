from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys

import yaml


EXPECTED_AGENTS = {
    "00-sdlc-orchestrator", "05-prompt-router", "10-business-analyst",
    "15-codebase-analyzer", "17-technology-lifecycle-analyst",
    "20-solution-architect", "30-uiux-engineer", "40-developer",
    "50-reviewer-overseer", "60-test-engineer", "70-automation-engineer",
    "80-security-performance-engineer", "90-build-deploy", "100-documentation",
}
SKILL_IDS = {"architecture-design", "decision-recording", "requirements-analysis", "tdd-implementation", "testing-strategy", "scope-control", "evidence-grounding"}
NON_SUCCESS = {"UNKNOWN", "BLOCKED", "DEFERRED", "PARTIAL", "NOT_TESTED", "FAILED", "REWORK_REQUIRED"}
PROHIBITED_AUTHORITY = {"approve", "merge", "deploy", "database_remediation", "security_remediation", "workflow_state_change", "silent_handoff", "status_coercion"}
SECRET_PATTERN = re.compile(r"(?i)(pat|password|secret|token)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{20,}")


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_skill_front_matter(path: Path):
    text = path.read_text(encoding="utf-8")
    parts = text.split("---", 2)
    if len(parts) < 3:
        raise ValueError("missing Skill front matter")
    return yaml.safe_load(parts[1])


def validate_instance(value, schema, path="$", errors=None):
    errors = [] if errors is None else errors
    expected = schema.get("type")
    type_ok = {
        "object": isinstance(value, dict), "array": isinstance(value, list),
        "string": isinstance(value, str), "integer": isinstance(value, int) and not isinstance(value, bool),
        "number": isinstance(value, (int, float)) and not isinstance(value, bool),
        "boolean": isinstance(value, bool), "null": value is None,
    }
    if isinstance(expected, list):
        if not any(type_ok.get(item, False) for item in expected):
            errors.append(f"{path}: expected one of {expected}")
            return errors
    elif expected and not type_ok.get(expected, False):
        errors.append(f"{path}: expected {expected}")
        return errors
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: value is not an allowed enum member")
    if "const" in schema and value != schema["const"]:
        errors.append(f"{path}: value must equal {schema['const']!r}")
    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            errors.append(f"{path}: string is shorter than minLength")
        if "pattern" in schema and not re.search(schema["pattern"], value):
            errors.append(f"{path}: string does not match pattern")
    if isinstance(value, (int, float)):
        if "minimum" in schema and value < schema["minimum"]:
            errors.append(f"{path}: value is below minimum")
        if "maximum" in schema and value > schema["maximum"]:
            errors.append(f"{path}: value is above maximum")
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            errors.append(f"{path}: fewer than minItems")
        if schema.get("uniqueItems") and len({json.dumps(item, sort_keys=True) for item in value}) != len(value):
            errors.append(f"{path}: duplicate array items")
        for index, item in enumerate(value):
            validate_instance(item, schema.get("items", {}), f"{path}[{index}]", errors)
    if isinstance(value, dict):
        for key in schema.get("required", []):
            if key not in value:
                errors.append(f"{path}: missing required field {key}")
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            for key in value:
                if key not in properties:
                    errors.append(f"{path}: unknown field {key}")
        for key, child in properties.items():
            if key in value:
                validate_instance(value[key], child, f"{path}.{key}", errors)
    for condition in schema.get("allOf", []):
        branch = condition.get("if", {})
        if isinstance(value, dict) and all(key in value and ("const" not in rule or value[key] == rule["const"]) for key, rule in branch.get("properties", {}).items()):
            validate_instance(value, condition.get("then", {}), path, errors)
    return errors


def validate_schema(path: Path, errors: list[str]):
    try:
        schema = load_json(path)
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid schema {path.name}: {exc}")
        return None
    if schema.get("additionalProperties") is not False:
        errors.append(f"schema {path.name} must close controlled properties")
    return schema


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    required = [
        "registry/agents.yaml", "registry/capabilities.yaml", "config/project.example.yaml",
        "governance/execution-policy.yaml", "governance/status-semantics.yaml",
        "governance/grounding-policy.yaml", "schemas/handoff.schema.json", "schemas/provider-event.schema.json",
    ]
    for relative in required:
        if not (root / relative).is_file():
            errors.append(f"missing required file: {relative}")
    if errors:
        return errors

    agents = {a["id"] for a in load_yaml(root / "registry/agents.yaml")["agents"]}
    if agents != EXPECTED_AGENTS:
        errors.append(f"agent inventory mismatch: missing={sorted(EXPECTED_AGENTS-agents)} extra={sorted(agents-EXPECTED_AGENTS)}")
    for agent_id in EXPECTED_AGENTS:
        path = root / ".github/agents" / f"{agent_id}.agent.md"
        if not path.is_file():
            errors.append(f"missing agent contract: {path.relative_to(root)}")
            continue
        text = path.read_text(encoding="utf-8")
        for marker in ("agents: []", "send: false", "Minimum Necessary Scope", "Grounding"):
            if marker not in text:
                errors.append(f"{path.relative_to(root)} missing marker {marker!r}")

    statuses = load_yaml(root / "governance/status-semantics.yaml")
    if {"PASS", "PASSED"} != set(statuses["success_statuses"]):
        errors.append("success status set changed")
    if not NON_SUCCESS.issubset(set(statuses["non_success_statuses"])):
        errors.append("Wave 1 non-success status set is incomplete")

    for path in (root / "workflows").glob("*.yaml"):
        workflow = load_yaml(path)
        for step in workflow.get("steps", []):
            agent = step.get("agent")
            if agent and agent not in agents:
                errors.append(f"{path.name} references unknown agent {agent}")

    skill_schema_path = root / "schemas/skill-contract.schema.json"
    skills_registry_path = root / "registry/skills.yaml"
    if not skill_schema_path.is_file() or not skills_registry_path.is_file():
        errors.append("missing Wave 1 Skill registry or Skill contract schema")
    else:
        skill_schema = validate_schema(skill_schema_path, errors)
        registry = load_yaml(skills_registry_path)
        if registry.get("schema_version") != "1.1.0":
            errors.append("Skill registry schema_version must be 1.1.0")
        records = registry.get("skills", [])
        ids = [record.get("id") for record in records]
        if len(records) != 7 or set(ids) != SKILL_IDS:
            errors.append(f"Skill inventory mismatch: expected exactly {sorted(SKILL_IDS)}")
        if len(ids) != len(set(ids)):
            errors.append("duplicate Skill ID")
        seen_paths = set()
        for record in records:
            if skill_schema:
                for problem in validate_instance(record, skill_schema, f"skill[{record.get('id', '?')}]"):
                    errors.append(problem)
            location = record.get("location")
            if location in seen_paths:
                errors.append(f"duplicate Skill path: {location}")
            seen_paths.add(location)
            if record.get("lifecycle_status") != "PLANNED" and not (root / location).is_file():
                errors.append(f"missing Skill file: {location}")
            if not set(record.get("prohibited_operations", [])) >= PROHIBITED_AUTHORITY:
                errors.append(f"Skill {record.get('id')} does not prohibit authority escalation")
            if (root / location).is_file():
                try:
                    front_matter = load_skill_front_matter(root / location)
                    for field in ("id", "version", "location", "authority_inheritance", "lifecycle_status"):
                        expected = location if field == "location" else record.get(field)
                        if front_matter.get(field) != expected:
                            errors.append(f"Skill {record.get('id')} metadata conflict: {field}")
                except (OSError, ValueError, yaml.YAMLError) as exc:
                    errors.append(f"invalid Skill metadata: {location}: {exc}")

    for schema_name in ("agent-contract.schema.json", "evidence.schema.json", "provider-contract.schema.json", "authority-denial.schema.json", "provider-event.schema.json"):
        validate_schema(root / "schemas" / schema_name, errors)

    provider_schema = root / "schemas/provider-contract.schema.json"
    if provider_schema.is_file():
        provider = load_json(provider_schema)
        if provider.get("properties", {}).get("mode", {}).get("enum") != ["DISABLED", "SHADOW", "ENABLED"]:
            errors.append("provider modes must be exactly DISABLED, SHADOW, ENABLED")
        if "REQUIRED" in provider.get("properties", {}).get("mode", {}).get("enum", []):
            errors.append("provider schema contains forbidden REQUIRED operating mode")
        if provider.get("properties", {}).get("evidence_authority", {}).get("enum") != ["SUPPLEMENTAL_ONLY", "NONE"]:
            errors.append("provider evidence authority enum is invalid")

    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".zip", ".docx", ".pptx"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if SECRET_PATTERN.search(text):
            errors.append(f"possible committed secret: {path.relative_to(root)}")
        if re.search(r"(?i)(sharjah|named customer|customer-specific|pilot-specific)", text) and path.name != "AGENTS.md":
            errors.append(f"project-specific leakage: {path.relative_to(root)}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Generic Agentic SDLC project template")
    parser.add_argument("root", nargs="?", default="project-template")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    errors = validate(root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Framework validation passed: {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
