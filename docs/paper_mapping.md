# Paper claims → files

| Paper | Claim | Backed by |
|---|---|---|
| §III-A | Guideline pages processed with OCR | `data/source/modules/<CODE>/extracted_pages/`, `prompts/01_graph_extraction/` |
| §III-A | Six-stage construction to JSON and Neo4j | `notebooks/01_graph_construction/1a`–`1d` |
| §III-A | Structural checks (unique IDs, edge targets, start node, reachable terminals, referral continuity) | `scripts/validate_graphs.py` (all 7 graphs pass) |
| §III-B | Five node types, prefixes `_A _M _D _R _E` | `docs/schema.md`, `data/graphs/` |
| §III-B | 220 nodes, 272 edges (six modules); per-module counts | `data/graph_stats.csv` (rebuild with `scripts/graph_stats.py`); 237 / 289 with OTH |
| §IV-B | LLM normalizes responses to a condition | `prompts/03_virtual_patient/` — the virtual-patient call returns YES / NO / NO_ANSWER directly; there is no separate normalizer |
| §V | Reference paths by GPT-5.5-Pro with strict schema | `notebooks/02_cases/2a_generate_reference_paths.ipynb`, `prompts/02_case_generation/reference_path_*` |
| §V | All 22 paths checked by hand | `data/cases/reference_paths/` (no review log stored) |
| §V / §VII | Reference paths valid; three end at a diagnosis node (truncated) | `scripts/oracle_replay.py`: 19 OK, 3 TRUNCATED (CMH_single_hop_positive_1, CMH_to_SUI_multi_hop_positive_1, DEP_SUI_MHP_001), 0 broken |
| §V | Back-stories by GPT-5.5 | `notebooks/02_cases/2b_*.ipynb`, `prompts/02_case_generation/backstory_*` |
| §V | 6 SH-pos, 6 SH-neg, 10 MH-pos | `data/cases/cases_22.json` |
| §VI-A | 13 configurations, 286 executions | `configs/experiment.yaml`, `results/raw_runs/` |
| §VI-A | Six navigator models | `configs/models.yaml` |
| §VII | Table II | `results/tables/system_level_comparison.csv` (finding accuracy = per-run mean) |
| §VII | Table III | `results/tables/category_level_comparison.csv` |
| §VII-B | Per-navigator exact match | `results/tables/navigator_model_comparison.csv` |
| App. A | Prompts | `prompts/ALL_PROMPTS.md` |

## Differences between paper text and code

1. **S3 input.** The paper says "original guideline text"; the S3 navigator receives
   `mhgap_clinical_logic.md`, an LLM-written text summary of each module.
2. **Virtual-patient model differs between systems.** S1 uses `gpt-4.1-mini` (code default; the
   model is not written to the S1 logs); S2 and S3 use `gpt-4o-mini`.
3. **Graph-building prompt not kept.** The only text→JSON prompt in the notebooks produces a
   different schema (`Question` nodes, `NEXT_YES` edges) from the final graphs. The prompt used
   for the final graphs and for `mhgap_clinical_logic.md` was not saved; see
   `prompts/01_graph_extraction/text_to_graph_json_final.MISSING.txt`. The final graphs are
   released as data and checked with `scripts/validate_graphs.py`.
4. **Edge types.** The paper lists YES, NO, NEXT and REFERRAL edges; the graphs contain only
   YES, NO and NEXT. Referrals are nodes with a `target_module` field.
5. **Six modules.** OTH is also used, as the referral target in DEP→OTH and SUI→OTH.
