# Paper claims → files (camera-ready version)

| Paper | Claim | Backed by |
|---|---|---|
| §III-A | Gemini 2.5 Pro page transcription (300 DPI); second Gemini prompt text → JSON | `configs/models.yaml`, `prompts/01_graph_extraction/` (final text → JSON prompt still missing) |
| §III-A | Six-stage construction to JSON and Neo4j | `notebooks/01_graph_construction/1a`–`1d` |
| §III-A | Structural checks; all seven graphs pass | `python scripts/validate_graphs.py` |
| §III-A | Graphs checked by hand by the three authors | by hand (no review log stored) |
| §III-B | Edges carry YES / NO / NEXT; referrals are nodes with `target_module` | `docs/schema.md`, `data/graphs/` |
| §III-B | 237 nodes / 289 edges (7 graphs); 220 / 272 (6 benchmark modules) | `data/graph_stats.csv`, `scripts/validate_graphs.py` |
| §IV-B | Virtual-patient call returns YES / NO / NO_ANSWER and acts as the normalizer; gpt-4.1-mini (S1), gpt-4o-mini (S2, S3), temperature 0, 25 tokens | `prompts/03_virtual_patient/`, `configs/models.yaml` |
| §V | Reference paths by gpt-5.5-pro with strict schema; back-stories by gpt-5.5 | `notebooks/02_cases/`, `prompts/02_case_generation/` |
| §V | All 22 paths checked by hand by the three authors | `data/cases/reference_paths/` |
| §V | 6 SH-pos, 6 SH-neg, 10 MH-pos | `data/cases/cases_22.json` |
| §VI-A | 13 configurations, 286 executions; S3 reads the LLM-written `mhgap_clinical_logic.md` + node catalogue | `configs/experiment.yaml`, `results/raw_runs/` |
| §VII | Table II | `results/tables/system_level_comparison.csv` (finding accuracy = per-run mean) |
| §VII | Table III | `results/tables/category_level_comparison.csv` |
| §VII-B | Per-navigator exact match | `results/tables/navigator_model_comparison.csv` |
| §VII-D | Oracle replay: 22/22 reference paths as prefixes, 19/22 exact; attribution of S1's 5 non-matches | `python scripts/oracle_replay.py` |
| §VII-D | S1's 5 non-matches: 3 from reference paths that end at a diagnosis node, 2 from patient answers that differ from the gold condition (3 mismatched, 12 extra findings) | `python scripts/s1_failure_analysis.py` |
| App. A | Models, settings, prompts | `configs/models.yaml`, `prompts/ALL_PROMPTS.md` |

## Known differences between paper and code (stated in the paper's Limitations)

1. S3 receives `mhgap_clinical_logic.md`, an LLM-written text summary of each module, not the original guideline wording.
2. The virtual patient / normalizer model differs between S1 (gpt-4.1-mini, code default, not in the S1 logs) and S2/S3 (gpt-4o-mini).
3. Three reference paths (CMH single-hop positive, CMH→SUI, DEP→SUI) end at a diagnosis node although the graph continues through management nodes into further assessment questions.
4. The prompt and model that produced the final graph JSON are not recorded.
