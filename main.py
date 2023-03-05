"""Calculate critical-path latency for a DAG of voice-pipeline stages."""
import argparse
import json
import math
from pathlib import Path

def analyze(stages, budget_ms):
    if isinstance(budget_ms, bool) or not isinstance(budget_ms, (int, float)) or (not math.isfinite(budget_ms)) or (budget_ms < 0):
        raise ValueError('budget_ms must be finite and nonnegative')
    if not isinstance(stages, list) or len(stages) > 500:
        raise ValueError('stages must be a list of at most500items')
    lookup = {}
    for stage in stages:
        if not isinstance(stage, dict):
            raise ValueError('Stage must be an object')
        (name, duration, deps) = (stage.get('name'), stage.get('duration_ms'), stage.get('depends_on', []))
        if not isinstance(name, str) or not name.strip() or name in lookup:
            raise ValueError('Stage names must be unique nonempty strings')
        if isinstance(duration, bool) or not isinstance(duration, (int, float)) or (not math.isfinite(duration)) or (duration < 0):
            raise ValueError('Durations must be finite and nonnegative')
        if not isinstance(deps, list) or any((not isinstance(x, str) for x in deps)) or len(set(deps)) != len(deps):
            raise ValueError('Dependencies must be unique name strings')
        lookup[name] = {'duration_ms': duration, 'depends_on': deps}
    for stage in lookup.values():
        if any((x not in lookup for x in stage['depends_on'])):
            raise ValueError('Unknown dependency')
    done = {}
    remaining = set(lookup)
    while remaining:
        ready = sorted((name for name in remaining if all((dep in done for dep in lookup[name]['depends_on']))))
        if not ready:
            raise ValueError('Dependency cycle')
        for name in ready:
            candidates = [done[dep] for dep in lookup[name]['depends_on']]
            previous = max(candidates, key=lambda item: (item['finish_ms'], item['path']), default={'finish_ms': 0, 'path': []})
            done[name] = {'start_ms': previous['finish_ms'], 'finish_ms': previous['finish_ms'] + lookup[name]['duration_ms'], 'path': previous['path'] + [name]}
        remaining.difference_update(ready)
    critical = max(done.values(), key=lambda x: (x['finish_ms'], x['path']), default={'finish_ms': 0, 'path': []})
    total = critical['finish_ms']
    return {'critical_path': critical['path'], 'estimated_latency_ms': total, 'budget_ms': budget_ms, 'remaining_ms': budget_ms - total, 'within_budget': total <= budget_ms, 'schedule': done}
