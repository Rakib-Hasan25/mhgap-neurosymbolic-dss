"""Structural checks on every module graph (paper Section III-A).

For each data/graphs/<CODE>/mhgap_decision_graph.json:
  1. node IDs are unique
  2. every edge points from and to an existing node
  3. exactly one node has "is_starting": true
  4. every node is reachable from the start node
  5. node type matches its ID prefix (_A, _M, _D, _R, _E)
  6. edge conditions are YES / NO / NEXT, and no node has two outgoing edges
     with the same condition (the engine would see an ambiguous transition)
  7. referral nodes name a target_module that exists and has a start node
  8. every path ends at a terminal (exit or referral); nodes with no outgoing
     edge must be exit or referral nodes

Checks 6 and 8 are deterministic-navigation checks: Eq. 1-2 need exactly one
matching edge per answer.

Usage: python scripts/validate_graphs.py      (exit code 1 if any check fails)
"""
import json
import sys
from collections import Counter, deque
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
GRAPHS = REPO / 'data' / 'graphs'
PREFIX = {'assessment': 'A', 'management': 'M', 'diagnosis': 'D', 'referral': 'R', 'exit': 'E'}
CONDITIONS = {'YES', 'NO', 'NEXT'}
TERMINAL = {'exit', 'referral'}


def load_all() -> dict:
    return {p.name: json.loads((p / 'mhgap_decision_graph.json').read_text(encoding='utf-8'))
            for p in sorted(GRAPHS.iterdir()) if (p / 'mhgap_decision_graph.json').exists()}


def check(code: str, g: dict, graphs: dict) -> list[str]:
    errors = []
    nodes = g['nodes']
    edges = g['relationships']

    # 1 unique IDs
    dup = [i for i, n in Counter(n['id'] for n in nodes).items() if n > 1]
    if dup:
        errors.append(f'duplicate node IDs: {dup}')
    by_id = {n['id']: n for n in nodes}

    # 2 edge endpoints exist
    for e in edges:
        for end in ('from', 'to'):
            if e[end] not in by_id:
                errors.append(f'edge {e["from"]} -> {e["to"]}: {end} node does not exist')

    # 3 one start node
    starts = [n['id'] for n in nodes if n.get('is_starting')]
    if len(starts) != 1:
        errors.append(f'expected 1 start node, found {len(starts)}: {starts}')

    # 5 type matches prefix
    for n in nodes:
        t = n.get('type')
        if t not in PREFIX:
            errors.append(f'{n["id"]}: unknown type {t!r}')
        elif not n['id'].startswith(f'{code}_{PREFIX[t]}'):
            errors.append(f'{n["id"]}: type {t} but ID prefix is not {code}_{PREFIX[t]}')

    # 6 conditions valid and unambiguous
    out = {i: [] for i in by_id}
    for e in edges:
        if e.get('condition') not in CONDITIONS:
            errors.append(f'edge {e["from"]} -> {e["to"]}: condition {e.get("condition")!r}')
        if e['from'] in out:
            out[e['from']].append(e)
    for nid, es in out.items():
        for cond, k in Counter(e.get('condition') for e in es).items():
            if k > 1:
                errors.append(f'{nid}: {k} outgoing edges with condition {cond} (ambiguous)')

    # 4 reachability from start
    if len(starts) == 1:
        seen, queue = {starts[0]}, deque([starts[0]])
        while queue:
            for e in out.get(queue.popleft(), []):
                if e['to'] in by_id and e['to'] not in seen:
                    seen.add(e['to'])
                    queue.append(e['to'])
        unreachable = sorted(set(by_id) - seen)
        if unreachable:
            errors.append(f'unreachable from {starts[0]}: {unreachable}')

    # 7 referral continuity
    for n in nodes:
        if n.get('type') != 'referral':
            continue
        target = n.get('target_module')
        if not target:
            errors.append(f'{n["id"]}: referral without target_module')
        elif target not in graphs:
            errors.append(f'{n["id"]}: target_module {target} has no graph')
        elif sum(1 for m in graphs[target]['nodes'] if m.get('is_starting')) != 1:
            errors.append(f'{n["id"]}: target_module {target} has no single start node')

    # 8 dead ends must be terminals
    for nid, es in out.items():
        if not es and by_id[nid].get('type') not in TERMINAL:
            errors.append(f'{nid}: no outgoing edge but type is {by_id[nid].get("type")}')

    return errors


def main() -> int:
    graphs = load_all()
    failed = 0
    for code, g in graphs.items():
        errors = check(code, g, graphs)
        status = 'OK  ' if not errors else 'FAIL'
        print(f'{status} {code}: {len(g["nodes"])} nodes, {len(g["relationships"])} edges')
        for err in errors:
            print(f'       - {err}')
        failed += bool(errors)
    print(f'\n{len(graphs) - failed}/{len(graphs)} graphs pass all structural checks')
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
