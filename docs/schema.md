# Graph schema

Each module is one file: `data/graphs/<CODE>/mhgap_decision_graph.json`.

```json
{
  "module": {"id": "DEP", "name": "Depression"},
  "nodes": [
    {"id": "DEP_A1", "type": "assessment", "is_starting": true, "text": "Has the person had ..."}
  ],
  "relationships": [
    {"from": "DEP_A1", "to": "DEP_A2", "condition": "YES"}
  ]
}
```

## Node types

| Type | ID prefix | Meaning |
|---|---|---|
| assessment | `_A` | A question asked to the person (answered YES / NO) |
| management | `_M` | An action or treatment step |
| diagnosis | `_D` | A diagnosis is reached |
| referral | `_R` | Hand-off to another module (`target_module`) |
| exit | `_E` | Assessment ends without this module's diagnosis |

Exactly one node per module has `"is_starting": true`.

## Edges

`relationships` are directed edges `{from, to, condition}` inside one module. Conditions used
across all graphs: `YES` (85), `NO` (85), `NEXT` (119, unconditional).

There are no cross-module edges. A referral is a `referral` node with a `target_module` field;
the engine jumps from it to the target module's `is_starting` node.

The symbolic navigator (S1) follows an edge only when exactly one outgoing edge matches the
normalized answer (paper Eq. 1–2). Zero matches → unmatched-condition error; more than one →
ambiguous-graph error.

## Sizes

See `data/graph_stats.csv` (rebuild with `python scripts/graph_stats.py`).

| | Nodes | Edges |
|---|---|---|
| Six benchmark modules (DEP, SUB, CMH, EPI, PSY, SUI) | 220 | 272 |
| Plus OTH (referral target only) | 237 | 289 |

## Reference path format (`data/cases/`)

Each case has a `node_sequence`: the graph nodes in order, each with `condition_met` = the edge
condition taken to reach the next node. On a referral node, `condition_met` is omitted and the
next node is the target module's start node.
