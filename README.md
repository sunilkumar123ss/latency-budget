# Voice Pipeline Critical-Path Planner

**Demo/starter · Python standard library only.**

Build an earliest-start schedule and critical path for a dependency graph of voice pipeline stages.

All bundled fixtures are synthetic and contain no customer data or secrets.

## Run

Use Python 3.9 or later (validated with Python 3.9.6). No installation or network access is needed. From this project directory:

```sh
python3 main.py
python3 main.py --input fixtures/demo.json
python3 -m unittest -v
```

The default CLI executes a deterministic working demo. Invalid input exits with a readable error and nonzero status.

## Behavior

Input JSON contains `stages` and `budget_ms`. Each stage has a unique `name`, finite nonnegative `duration_ms` and optional `depends_on` list. The result reports the schedule, critical path, total estimate and remaining budget. Parallel branches join with max(), not a sum. Duplicate names, missing dependencies and cycles are rejected.

## Limits and optional provider boundary

All fixture durations are synthetic planning inputs, not measured latency. The model assumes unlimited workers, deterministic durations and no contention or retries. There is a 500-stage limit. Equal-length critical paths use deterministic lexicographic tie-breaking.

Replace planning durations with measured ASR/LLM/TTS trace data if available. No inference or performance promise is included.

## Tests

`test_main.py` checks fixed expected results, edge cases and invalid inputs with `unittest`. These tests validate the local implementation, not real-world speech accuracy or production readiness. Run `python3 verify.py` to repeat this repository’s checks.

## Scope

This is an educational implementation with synthetic fixtures. Run the tests and inspect the documented limits before adapting it.

## Repository checks

```sh
python3 verify.py
```

This runs the isolated test suite, synthetic example, and CLI help. The included GitHub Actions workflow repeats these checks when the repository is published. No hosted CI result is claimed by the local verification report.
