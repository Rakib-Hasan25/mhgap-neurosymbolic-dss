"""Replay the 22 reference paths through the graphs (paper Section V).

For each case in data/cases/cases_22.json, start at the source module's start
node and follow the reference path's conditions with the same rule as the
symbolic engine (exactly one outgoing edge must match; a referral node jumps to
the target module's start node). The script reports:

  - BREAK      the path uses an edge or referral that the graph does not have
  - TRUNCATED  the path is valid but stops before a terminal (exit or referral),
               e.g. at a diagnosis node whose management steps are not included
  - OK         the path is valid and ends at a terminal

Nothing is changed; reference paths are reported as they are scored in the paper.

Usage: python scripts/oracle_replay.py
"""
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
GRAPHS = REPO / 'data' / 'graphs'
CASES = REPO / 'data' / 'cases' / 'cases_22.json'
TERMINAL = {'exit', 'referral'}


def load_graphs() -> tuple[dict, dict, dict]:
    nodes, out, start = {}, {}, {}
    for p in sorted(GRAPHS.iterdir()):
        f = p / 'mhgap_decision_graph.json'
        if not f.exists():
            continue
        g = json.loads(f.read_text(encoding='utf-8'))
        for n in g['nodes']:
            nodes[n['id']] = n
            out.setdefault(n['id'], [])
            if n.get('is_starting'):
                start[p.name] = n['id']
        for e in g['relationships']:
            out.setdefault(e['from'], []).append(e)
    return nodes, out, start


def replay(case: dict, nodes: dict, out: dict, start: dict) -> tuple[str, str]:
    path = case['reference_path']
    if path[0]['id'] != start.get(case['source_module']):
        return 'BREAK', f'path starts at {path[0]["id"]}, module start is {start.get(case["source_module"])}'
    for step, nxt in zip(path, path[1:]):
        node = nodes.get(step['id'])
        if node is None:
            return 'BREAK', f'{step["id"]} is not in any graph'
        if node.get('type') == 'referral':
            target = start.get(node.get('target_module'))
            if nxt['id'] != target:
                return 'BREAK', f'referral {step["id"]} leads to {target}, path goes to {nxt["id"]}'
            continue
        match = [e for e in out[step['id']] if e['condition'] == step.get('condition_met')]
        if len(match) != 1:
            return 'BREAK', f'{step["id"]}: {len(match)} edges match {step.get("condition_met")}'
        if match[0]['to'] != nxt['id']:
            return 'BREAK', f'{step["id"]} --{step["condition_met"]}--> {match[0]["to"]}, path goes to {nxt["id"]}'
    last = nodes.get(path[-1]['id'])
    if last is None:
        return 'BREAK', f'{path[-1]["id"]} is not in any graph'
    if last.get('type') not in TERMINAL:
        return 'TRUNCATED', f'ends at {last["id"]} ({last.get("type")}); graph continues to {[e["to"] for e in out[last["id"]]]}'
    return 'OK', f'ends at {last["id"]} ({last["type"]}), {len(path)} nodes'


def main() -> None:
    nodes, out, start = load_graphs()
    cases = json.loads(CASES.read_text(encoding='utf-8'))['cases']
    counts = {}
    for c in cases:
        status, note = replay(c, nodes, out, start)
        counts[status] = counts.get(status, 0) + 1
        print(f'{status:<9} {c["case_id"]:<48} {note}')
    print('\n' + ', '.join(f'{k}: {v}' for k, v in sorted(counts.items())) + f' (of {len(cases)} cases)')


if __name__ == '__main__':
    main()
