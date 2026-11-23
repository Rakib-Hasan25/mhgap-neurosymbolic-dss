"""Explain S1's non-matching runs (paper Section VII-D). For every S1 run whose exact path match failed,
compare the virtual patient's answer with the gold condition at each assessment node on the reference path.
Usage: python scripts/s1_failure_analysis.py   (reads results/raw_runs/S1_symbolic, no API keys)"""
import json, glob, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
fails = answer_cases = extra_cases = 0
tot_mismatch = tot_extra = 0
for f in sorted(glob.glob(os.path.join(ROOT, "results/raw_runs/S1_symbolic/*/*__graph.json"))):
    d = json.load(open(f, encoding="utf-8")); ev = d["evaluation"]
    tot_mismatch += len(ev.get("mismatched_findings", [])); tot_extra += len(ev.get("extra_findings", []))
    if ev.get("exact_ok"): continue
    fails += 1
    gold = {x["id"]: x.get("condition_met") for x in d["expected_node_sequence"]}
    ans = {s["id"]: s.get("user_answer") for s in d["step_logs"]}
    diff = [(k, gold[k], ans[k]) for k in ans if gold.get(k) in ("YES", "NO") and ans[k] != gold[k]]
    kind = "patient answer differs from gold" if diff else "reference path ends early; engine continues"
    answer_cases += bool(diff); extra_cases += not diff
    print(f"{d['case_id']}: {kind}; differing answers={diff}; extra findings={len(ev.get('extra_findings', []))}")
print(f"\nS1 non-matching runs: {fails} | due to answers: {answer_cases} | due to early-ending reference: {extra_cases}")
print(f"S1 totals: mismatched findings={tot_mismatch}, extra findings={tot_extra}")
