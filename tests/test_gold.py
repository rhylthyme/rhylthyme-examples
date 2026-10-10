#!/usr/bin/env python3
"""
Tests for the gold set in rhylthyme-examples/gold.

Each gold directory holds source.txt, context.json and program.json. Every
program must pass the Python validator (schema + logic) and, when node is
available, the JavaScript validator in rhylthyme-server/mcp-api/schedule.js.
Every step must carry metadata.sourceSpan whose quote is found in source.txt
at the stated occurrence (or be tagged inferred with a null span). The set as a
whole must hold the mix the PRD asks for (prd-agent-prompt-structure.md 5.1):
10 kitchen, 6 laboratory, 4 event, 4 fitness.
"""

import json
import shutil
import subprocess
from pathlib import Path

import jsonschema
import pytest

from rhylthyme.validate_program import validate_program_file_structured

GOLD_DIR = Path(__file__).resolve().parent.parent / "gold"
CONTEXT_SCHEMA = GOLD_DIR / "context.schema.json"
SCHEDULE_JS = (
    Path(__file__).resolve().parent.parent.parent
    / "rhylthyme-server"
    / "mcp-api"
    / "schedule.js"
)
SLUGS = (
    sorted(p.name for p in GOLD_DIR.iterdir() if (p / "program.json").exists())
    if GOLD_DIR.exists()
    else []
)
# The PRD mix (5.1). Exact, not a floor: a new gold program must be added
# together with a decision about which bucket it belongs to.
REQUIRED_DOMAINS = {"kitchen": 10, "laboratory": 6, "event": 4, "fitness": 4}
# A slug is <domain>-<short-name>; "laboratory" is spelled "lab" in slugs.
DOMAIN_PREFIX = {
    "kitchen": "kitchen",
    "laboratory": "lab",
    "event": "event",
    "fitness": "fitness",
    "other": "other",
}


def _load(slug):
    directory = GOLD_DIR / slug
    program = json.loads((directory / "program.json").read_text(encoding="utf-8"))
    source = (directory / "source.txt").read_text(encoding="utf-8")
    context = json.loads((directory / "context.json").read_text(encoding="utf-8"))
    return program, source, context


def _find_occurrence(text, quote, occurrence):
    """Independent re-implementation: n-th non-overlapping exact match."""
    position, found = 0, 0
    while True:
        index = text.find(quote, position)
        if index < 0:
            return None
        found += 1
        if found == occurrence:
            return index
        position = index + len(quote)


def _steps(program):
    for track in program["tracks"]:
        for step in track["steps"]:
            yield track, step


@pytest.mark.validation
@pytest.mark.unit
def test_gold_set_has_the_prd_domain_mix():
    assert GOLD_DIR.exists(), "gold/ directory missing"
    assert len(SLUGS) == sum(REQUIRED_DOMAINS.values()), SLUGS
    domains = {}
    for slug in SLUGS:
        _, _, context = _load(slug)
        domains[context["domain"]] = domains.get(context["domain"], 0) + 1
    assert domains == REQUIRED_DOMAINS, domains


@pytest.mark.validation
@pytest.mark.unit
@pytest.mark.parametrize("slug", SLUGS)
def test_slug_prefix_matches_domain(slug):
    _, _, context = _load(slug)
    domain = context["domain"]
    prefix = DOMAIN_PREFIX[domain]
    assert slug.startswith(prefix + "-"), (
        f"{slug}: domain {domain!r} wants slug prefix {prefix!r}-"
    )


@pytest.mark.validation
@pytest.mark.unit
@pytest.mark.parametrize("slug", SLUGS)
def test_gold_triple_is_complete(slug):
    directory = GOLD_DIR / slug
    for name in ("source.txt", "context.json", "program.json"):
        assert (directory / name).exists(), f"{slug}/{name} missing"
    program, source, _ = _load(slug)
    words = len(source.split())
    assert 150 <= words <= 600, f"{slug}: source.txt has {words} words"
    assert program.get("programId") and program.get("name")
    assert len(program["tracks"]) >= 2, "gold programs are multi-track"


@pytest.mark.validation
@pytest.mark.unit
@pytest.mark.parametrize("slug", SLUGS)
def test_gold_program_passes_python_validator(slug, schema_file):
    result = validate_program_file_structured(
        str(GOLD_DIR / slug / "program.json"), schema_file
    )
    assert not result["schema_errors"], result["schema_errors"]
    assert not result["logic_errors"], result["logic_errors"]


@pytest.mark.validation
@pytest.mark.integration
@pytest.mark.parametrize("slug", SLUGS)
def test_gold_program_passes_js_validator(slug):
    node = shutil.which("node")
    if node is None or not SCHEDULE_JS.exists():
        pytest.skip("node or schedule.js not available")
    program, _, _ = _load(slug)
    script = (
        "const s = require(process.argv[1]); let d = '';"
        "process.stdin.on('data', c => d += c);"
        "process.stdin.on('end', () => {"
        "  const v = s.validateProgram(JSON.parse(d));"
        "  process.stdout.write(JSON.stringify({valid: v.valid,"
        "    errors: (v.errors || []).map(e => e.message)}));"
        "});"
    )
    completed = subprocess.run(
        [node, "-e", script, str(SCHEDULE_JS)],
        input=json.dumps(program),
        capture_output=True,
        text=True,
        timeout=60,
        check=True,
    )
    payload = json.loads(completed.stdout)
    assert payload["valid"], payload["errors"]


@pytest.mark.validation
@pytest.mark.unit
@pytest.mark.parametrize("slug", SLUGS)
def test_every_step_has_a_located_span(slug):
    program, source, _ = _load(slug)
    problems = []
    for _, step in _steps(program):
        metadata = step.get("metadata")
        if not isinstance(metadata, dict) or "sourceSpan" not in metadata:
            problems.append(f"{step['stepId']}: no metadata.sourceSpan")
            continue
        span = metadata["sourceSpan"]
        if span is None:
            if not metadata.get("inferred"):
                problems.append(f"{step['stepId']}: null span without inferred: true")
            continue
        quote, occurrence = span.get("quote"), span.get("occurrence", 1)
        if not isinstance(quote, str) or not quote:
            problems.append(f"{step['stepId']}: empty quote")
            continue
        if not isinstance(occurrence, int) or occurrence < 1:
            problems.append(f"{step['stepId']}: bad occurrence {occurrence!r}")
            continue
        if _find_occurrence(source, quote, occurrence) is None:
            found = source.count(quote)
            problems.append(
                f"{step['stepId']}: {quote!r} occurrence {occurrence} not found "
                f"(text contains it {found} time(s))"
            )
    assert not problems, "\n".join(problems)


@pytest.mark.validation
@pytest.mark.unit
@pytest.mark.parametrize("slug", SLUGS)
def test_context_matches_schema(slug):
    program, _, context = _load(slug)
    schema = json.loads(CONTEXT_SCHEMA.read_text(encoding="utf-8"))
    jsonschema.validate(context, schema)
    assert context["environmentType"] == program.get("environmentType")


@pytest.mark.validation
@pytest.mark.unit
@pytest.mark.parametrize("slug", SLUGS)
def test_gold_program_has_cross_track_triggers(slug):
    program, _, _ = _load(slug)
    track_of = {}
    for track, step in _steps(program):
        track_of[step["stepId"]] = track["trackId"]
    cross = 0
    for track, step in _steps(program):
        trigger = step["startTrigger"]
        subs = trigger.get("triggers", [trigger])
        for sub in subs:
            anchor = sub.get("stepId")
            if anchor and track_of.get(anchor) not in (None, track["trackId"]):
                cross += 1
    assert cross >= 1, f"{slug}: no cross-track trigger"


@pytest.mark.validation
@pytest.mark.unit
@pytest.mark.parametrize("slug", SLUGS)
def test_gold_tasks_are_declared(slug):
    program, _, _ = _load(slug)
    declared = {c["task"] for c in program.get("resourceConstraints", [])}
    used = {step["task"] for _, step in _steps(program) if step.get("task")}
    assert used <= declared, used - declared


@pytest.mark.validation
@pytest.mark.integration
@pytest.mark.parametrize("slug", SLUGS)
def test_gold_program_has_no_resource_conflicts(slug):
    """The expert schedule must be feasible, not merely well-formed.

    Neither validator checks `maxConcurrent` against the resolved timeline,
    so a gold program can declare "one oven" and still put two dishes in it.
    `analyzeSchedule` resolves every trigger to absolute seconds and
    sweep-lines each task, so an empty `resourceConflicts` is the statement
    that one person with the declared resources could actually run this.
    """
    node = shutil.which("node")
    if node is None or not SCHEDULE_JS.exists():
        pytest.skip("node or schedule.js not available")
    program, _, _ = _load(slug)
    script = (
        "const s = require(process.argv[1]); let d = '';"
        "process.stdin.on('data', c => d += c);"
        "process.stdin.on('end', () => {"
        "  const a = s.analyzeSchedule(JSON.parse(d));"
        "  process.stdout.write(JSON.stringify({"
        "    conflicts: (a.resourceConflicts || []).map(c => ({"
        "      kind: c.kind, task: c.task, demand: c.demand,"
        "      cap: c.maxConcurrent === undefined ? c.maxInFlight : c.maxConcurrent,"
        "      start: c.startSeconds, end: c.endSeconds, steps: c.steps})),"
        "    makespan: a.makespanSeconds}));"
        "});"
    )
    completed = subprocess.run(
        [node, "-e", script, str(SCHEDULE_JS)],
        input=json.dumps(program),
        capture_output=True,
        text=True,
        timeout=60,
        check=True,
    )
    payload = json.loads(completed.stdout)
    conflicts = payload["conflicts"]
    detail = "; ".join(
        f"{c['kind']} on '{c['task']}': {c['demand']} concurrent vs cap {c['cap']} "
        f"at {c['start']}-{c['end']}s ({', '.join(c['steps'])})"
        for c in conflicts
    )
    assert not conflicts, f"{slug}: over-subscribed resources — {detail}"
