"""Deterministic optional-provider boundary; real providers are never installed or invoked."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

MODES = {"DISABLED", "SHADOW", "ENABLED"}
ORCHESTRATOR = "00-sdlc-orchestrator"
GRAPHIFY_CONSUMERS = {"15-codebase-analyzer", "20-solution-architect", "40-developer", "50-reviewer-overseer"}
HEADROOM_CONSUMERS = {"05-prompt-router", "15-codebase-analyzer", "20-solution-architect", "40-developer", "50-reviewer-overseer", "60-test-engineer", "100-documentation"}
REGISTERED_AGENTS = {"00-sdlc-orchestrator", "05-prompt-router", "10-business-analyst", "15-codebase-analyzer", "17-technology-lifecycle-analyst", "20-solution-architect", "30-uiux-engineer", "40-developer", "50-reviewer-overseer", "60-test-engineer", "70-automation-engineer", "80-security-performance-engineer", "90-build-deploy", "100-documentation"}
PROTECTED_CATEGORIES = {"approved_requirements", "acceptance_criteria", "approvals", "decisions", "structured_handoffs", "statuses", "exact_errors", "stack_traces", "commands", "arguments", "exit_codes", "paths", "filenames", "line_references", "ids", "hashes", "test_results", "security_findings", "database_findings", "deployment_evidence", "source_references", "provenance", "confidence", "verification_state"}


def _now():
    return datetime.now(timezone.utc).isoformat()


def _digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def _baseline(config):
    return config.get("rollback", {}).get("baseline", "NO_PROVIDER" if config["provider_id"] == "graphify" else "ORIGINAL_CONTEXT")


def event(config, request, operation, status, reason, **extra):
    provider_id = config["provider_id"]
    mode = config.get("mode", "DISABLED")
    result = {"event_id": f"evt-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f')}", "timestamp": _now(), "workflow_id": request.get("workflow_id"), "work_item_id": request.get("work_item_id"), "provider_id": provider_id, "provider_type": config.get("provider_type"), "expected_version": config.get("provider_version_expected", ""), "observed_version": None, "provider_mode": mode, "transport": config.get("transport"), "requesting_agent": request.get("requesting_agent"), "submitting_agent": request.get("submitting_agent"), "consumer_agent": request.get("consumer_agent"), "rejected_identity_field": None, "operation": operation, "query": request.get("query"), "source_paths": request.get("source_paths", []), "source_commit": request.get("source_commit"), "request_timestamp": request.get("request_timestamp", _now()), "response_timestamp": _now(), "duration_ms": 0, "health_check_attempted": False, "health_check_result": "NOT_ATTEMPTED", "connection_timeout_seconds": config.get("connection_timeout_seconds"), "execution_timeout_seconds": config.get("execution_timeout_seconds"), "invocation_attempted": False, "exit_code": None, "http_status": None, "timeout_type": "NONE", "output_classification": "QUARANTINED", "evidence_authority": "SUPPLEMENTAL_ONLY" if provider_id == "graphify" else "NONE", "confidence": None, "provenance": {}, "provenance_validation_result": "NOT_APPLICABLE", "index_timestamp": None, "index_freshness_result": "NOT_APPLICABLE", "coverage_result": "NOT_APPLICABLE", "repository_corroboration_result": "NOT_APPLICABLE", "disagreement_result": "NONE", "repository_precedence_applied": False, "protected_evidence_comparison_result": "NOT_APPLICABLE", "immutable_original_reference": request.get("original_reference"), "original_hash": None, "derived_hash": None, "selected_context": None, "shadow_quarantined": mode == "SHADOW", "fallback_used": True, "fallback_baseline": _baseline(config), "rollback_used": False, "runtime_disabled": False, "secrets_redacted": True, "human_approval_reference": request.get("human_approval_reference"), "status": status, "failure_reason": reason, "exact_error": None}
    result.update(extra)
    return result


def _reject(config, request, operation, status, reason, **extra):
    return event(config, request, operation, status, reason, **extra)


def _load_payload(fixture):
    return json.loads(Path(fixture).read_text(encoding="utf-8")) if fixture else {}


def _run_transport(config, request, fixture):
    payload = _load_payload(fixture)
    if config.get("transport") == "EXECUTABLE" and request.get("allow_test_double"):
        executable = Path(config.get("executable_or_endpoint", ""))
        if executable.name != "fake_provider.py" or not executable.is_file():
            return payload, {"transport_error": "only fake_provider.py may execute in tests"}
        try:
            completed = subprocess.run([sys.executable, str(executable), json.dumps(request.get("transport_request", {}))], capture_output=True, text=True, timeout=config["execution_timeout_seconds"], shell=False, check=False)
        except subprocess.TimeoutExpired as exc:
            return payload, {"timeout": True, "timeout_type": "EXECUTION", "exact_error": str(exc)}
        if completed.returncode:
            return payload, {"exit_code": completed.returncode, "exact_error": completed.stderr}
        try:
            return json.loads(completed.stdout), {"exit_code": 0}
        except json.JSONDecodeError as exc:
            return payload, {"exact_error": str(exc)}
    if config.get("transport") == "HTTP":
        opener = request.get("http_opener")
        if opener is None:
            return payload, {"transport_error": "HTTP requires injected local test double"}
        try:
            response = opener(request.get("http_request", {}), timeout=config["connection_timeout_seconds"])
            if response.get("status", 200) >= 400:
                return payload, {"http_status": response["status"], "exact_error": "HTTP failure"}
            return response.get("body", {}), {"http_status": response.get("status", 200)}
        except (TimeoutError, urllib.error.URLError) as exc:
            return payload, {"timeout": isinstance(exc, TimeoutError), "timeout_type": "CONNECTION", "exact_error": str(exc)}
    return payload, {}


def _graphify_validation(config, request, payload, base):
    provenance = payload.get("provenance")
    required = {"provider_version", "source_commit", "query_timestamp", "index_timestamp", "confidence"}
    if payload.get("unsupported") or "unsupported" in payload.get("reason", ""):
        return _reject(config, request, "validate", "REWORK_REQUIRED", "unsupported Graphify input", **base)
    if not isinstance(provenance, dict) or not required.issubset(provenance):
        return _reject(config, request, "validate", "REWORK_REQUIRED", "missing Graphify provenance", **base)
    if not payload.get("fresh", False):
        return _reject(config, request, "validate", "REWORK_REQUIRED", "stale Graphify index", **base)
    if payload.get("coverage", "COMPLETE") != "COMPLETE":
        return _reject(config, request, "validate", "REWORK_REQUIRED", "partial Graphify coverage", **base)
    if payload.get("repository_corroboration") != "CORROBORATED":
        return _reject(config, request, "validate", "REWORK_REQUIRED", "repository corroboration required", **base)
    if payload.get("disagreement"):
        return _reject(config, request, "validate", "REWORK_REQUIRED", "repository evidence wins disagreement", **base, provenance=provenance, disagreement_result="DISAGREEMENT", repository_precedence_applied=True, provenance_validation_result="VALID")
    return event(config, request, "invoke", "PASS", "", **base, output_classification="SUPPLEMENTAL", fallback_used=False, observed_version=provenance["provider_version"], provenance=provenance, provenance_validation_result="VALID", source_commit=provenance["source_commit"], query=provenance.get("query", request.get("query")), index_timestamp=provenance["index_timestamp"], index_freshness_result="FRESH", coverage_result="COMPLETE", repository_corroboration_result="CORROBORATED", confidence=provenance["confidence"])


def _headroom_validation(config, request, payload, base):
    original = request.get("original_context")
    if original is None or not request.get("original_reference"):
        return _reject(config, request, "validate", "REWORK_REQUIRED", "immutable original context is required", **base)
    original_hash = _digest(original)
    if request.get("simulate_retrieval_failure"):
        return _reject(config, request, "retrieve", "FAILED", "original context retrieval failure", **base, original_hash=original_hash, protected_evidence_comparison_result="RETRIEVAL_FAILED")
    derived = payload.get("derived_context", original)
    for category in PROTECTED_CATEGORIES:
        if category in original and derived.get(category) != original[category]:
            return _reject(config, request, "compare", "REWORK_REQUIRED", f"protected evidence changed: {category}", **base, original_hash=original_hash, derived_hash=_digest(derived), selected_context="ORIGINAL_CONTEXT", protected_evidence_comparison_result="MISMATCH")
    if config.get("mode") == "ENABLED" and (not request.get("human_approval_reference") or not request.get("fidelity_pass")):
        return _reject(config, request, "enable", "BLOCKED", "human approval and PASS fidelity evidence required", **base, original_hash=original_hash, derived_hash=_digest(derived), protected_evidence_comparison_result="PASS")
    status = "FAILED" if config.get("mode") == "SHADOW" else "PASS"
    return event(config, request, "invoke", status, "shadow output quarantined" if status == "FAILED" else "", **base, original_hash=original_hash, derived_hash=_digest(derived), protected_evidence_comparison_result="PASS", output_classification="QUARANTINED" if status == "FAILED" else "DERIVED_CONTEXT", fallback_used=status != "PASS", shadow_quarantined=config.get("mode") == "SHADOW")


def invoke(config, request, fixture=None, runtime_state=None):
    """Run only deterministic test doubles; every result is an auditable event."""
    runtime_state = runtime_state if runtime_state is not None else {}
    provider_id = config.get("provider_id")
    mode = config.get("mode", "DISABLED")
    if provider_id not in {"graphify", "headroom"}:
        return _reject(config, request, "validate", "REWORK_REQUIRED", "invalid provider identity")
    if mode not in MODES:
        return _reject(config, request, "validate", "REWORK_REQUIRED", "invalid mode")
    consumers = GRAPHIFY_CONSUMERS if provider_id == "graphify" else HEADROOM_CONSUMERS
    requester = request.get("requesting_agent")
    if requester not in REGISTERED_AGENTS or requester not in consumers:
        return _reject(config, request, "authorize", "BLOCKED", "requesting agent not allowed", rejected_identity_field="requesting_agent")
    if request.get("submitting_agent") != ORCHESTRATOR:
        return _reject(config, request, "authorize", "BLOCKED", "Agent 00 submission required", rejected_identity_field="submitting_agent")
    consumer = request.get("consumer_agent")
    if consumer not in consumers:
        return _reject(config, request, "authorize", "BLOCKED", "consumer not allowlisted", rejected_identity_field="consumer_agent")
    if requester != consumer:
        return _reject(config, request, "authorize", "BLOCKED", "requesting and consumer agents must match", rejected_identity_field="consumer_agent")
    if request.get("operation") == "runtime_disable":
        runtime_state[provider_id] = {"disabled_by": ORCHESTRATOR, "scope": config["runtime_disable"]["scope"], "reason": request.get("reason", "safety disable"), "timestamp": _now()}
        return event(config, request, "runtime_disable", "FAILED", request.get("reason", "safety disable"), runtime_disabled=True, rollback_used=True, rollback_result="BASELINE_SELECTED")
    if runtime_state.get(provider_id):
        return _reject(config, request, "invoke", "BLOCKED", "runtime disabled", runtime_disabled=True)
    if mode == "DISABLED":
        return event(config, request, "invoke", "NOT_TESTED", "provider disabled")
    if not request.get("human_approval_reference"):
        return _reject(config, request, "enable", "BLOCKED", "human activation approval required")
    payload = _load_payload(fixture)
    if config.get("health_check", {}).get("active") and (payload.get("health_failure") or "health check" in payload.get("reason", "")):
        return _reject(config, request, "health", "FAILED", "health check failed", health_check_attempted=True, health_check_result="FAILED")
    payload, transport = _run_transport(config, request, fixture)
    base = {"invocation_attempted": True, "health_check_attempted": config.get("health_check", {}).get("active", False), "health_check_result": "PASS" if config.get("health_check", {}).get("active") else "NOT_ATTEMPTED", **transport}
    if transport.get("timeout"):
        return _reject(config, request, "invoke", "FAILED", f"{transport['timeout_type'].lower()} timeout", **base, rollback_used=True)
    if transport.get("transport_error") or transport.get("exit_code") not in {None, 0} or transport.get("http_status", 0) >= 400:
        return _reject(config, request, "invoke", "FAILED", transport.get("transport_error", "transport failure"), **base, rollback_used=True)
    if payload.get("malformed"):
        return _reject(config, request, "normalize", "REWORK_REQUIRED", "malformed provider output", **base, exact_error="malformed output")
    if payload.get("failure") or payload.get("timeout"):
        return _reject(config, request, "invoke", "FAILED", payload.get("reason", "provider failure"), **base, rollback_used=True)
    expected = config.get("provider_version_expected")
    provenance = payload.get("provenance") if isinstance(payload.get("provenance"), dict) else {}
    observed = payload.get("provider_version") or provenance.get("provider_version")
    if provider_id == "graphify" and expected and observed != expected:
        return _reject(config, request, "validate", "REWORK_REQUIRED", "incompatible provider version", **base, observed_version=observed)
    return _graphify_validation(config, request, payload, base) if provider_id == "graphify" else _headroom_validation(config, request, payload, base)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--request", required=True)
    parser.add_argument("--fixture")
    args = parser.parse_args()
    print(json.dumps(invoke(json.loads(Path(args.config).read_text(encoding="utf-8")), json.loads(Path(args.request).read_text(encoding="utf-8")), args.fixture), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
