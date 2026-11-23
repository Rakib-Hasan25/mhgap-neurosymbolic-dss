"""Count nodes and edges per module graph and write data/graph_stats.csv.

Usage: python scripts/graph_stats.py
"""
import csv
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
GRAPHS = REPO / 'data' / 'graphs'
OUT = REPO / 'data' / 'graph_stats.csv'
BENCHMARK = ['DEP', 'SUB', 'CMH', 'EPI', 'PSY', 'SUI']
TYPES = ['assessment', 'management', 'diagnosis', 'referral', 'exit']


def main() -> None:
    rows = []
    for code in BENCHMARK + sorted({p.name for p in GRAPHS.iterdir() if p.is_dir()} - set(BENCHMARK)):
        g = json.loads((GRAPHS / code / 'mhgap_decision_graph.json').read_text(encoding='utf-8'))
        rows.append({
            'module_id': code,
            'module_name': g['module'].get('name', ''),
            'in_benchmark': code in BENCHMARK,
            'nodes': len(g['nodes']),
            'edges': len(g['relationships']),
            **{t: sum(1 for n in g['nodes'] if n.get('type') == t) for t in TYPES},
        })

    numeric = ['nodes', 'edges', *TYPES]
    total6 = {k: sum(r[k] for r in rows if r['in_benchmark']) for k in numeric}
    total_all = {k: sum(r[k] for r in rows) for k in numeric}

    with OUT.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
        w.writerow({'module_id': 'TOTAL_6', 'module_name': 'Six benchmark modules', 'in_benchmark': '', **total6})
        w.writerow({'module_id': f'TOTAL_{len(rows)}', 'module_name': 'All graphs', 'in_benchmark': '', **total_all})

    print(f'Six benchmark modules: {total6["nodes"]} nodes, {total6["edges"]} edges')
    print(f'All {len(rows)} graphs: {total_all["nodes"]} nodes, {total_all["edges"]} edges')
    print('Wrote', OUT.relative_to(REPO))


if __name__ == '__main__':
    main()
