# A Neurosymbolic Decision-Support System for Graph-Constrained mhGAP Guideline Traversal

Code, data, prompts and results for the ICCIT 2026 paper (`paper/`).

The WHO mhGAP-IG 2.0 guideline is encoded as a typed decision graph. An LLM only turns patient
answers into an allowed condition (YES / NO); a symbolic engine follows the matching graph edge.
Three navigation strategies are compared on the same 22 virtual-patient cases (286 executions):

| System | Who picks the next node | What it sees | Exact path match |
|---|---|---|---|
| **S1** Symbolic | Deterministic edge matching (Neo4j) | Graph edges | 17/22 (77.3%) |
| **S2** LLM + graph JSON | 6 navigator LLMs | `mhgap_decision_graph.json` | 75/132 (56.8%) |
| **S3** LLM + text | 6 navigator LLMs | `mhgap_clinical_logic.md` + node list | 41/132 (31.1%) |

## Repository layout

```
├── README.md
├── requirements.txt · .env.example · .gitignore
├── paper/                      the paper PDF
├── prompts/
│   ├── ALL_PROMPTS.md          ← every prompt in one file, with model and notebook
│   ├── 01_graph_extraction/    page OCR, text → graph JSON
│   ├── 02_case_generation/     reference-path generator, back-story generator
│   ├── 03_virtual_patient/     YES / NO / NO_ANSWER answerer (also the normalizer)
│   └── 04_navigators/          S2 and S3 navigator rules
├── configs/
│   ├── models.yaml             model per role, temperature, token limits
│   └── experiment.yaml         cases, 13 configurations, metrics
├── data/
│   ├── source/                 mhGAP-IG 2.0 PDF, per-module pages and OCR text
│   ├── graphs/<CODE>/          mhgap_decision_graph.json + mhgap_clinical_logic.md
│   ├── graph_stats.csv         nodes / edges / node types per module
│   └── cases/
│       ├── cases_22.json       final benchmark in one file (story + reference path)
│       ├── reference_paths/    generator output per module, after manual path check
│       └── virtual_patients/   same cases with hidden back-story (user_story)
├── notebooks/
│   ├── 01_graph_construction/  1a split PDF → 1b OCR → 1c text→JSON → 1d Neo4j
│   ├── 02_cases/               2a reference paths → 2b back-stories
│   ├── 03_experiments/         S1, S2, S3 runners
│   └── 04_analysis/            4a–4c per-system summaries → 4d Tables II–III, figures
├── scripts/
│   └── graph_stats.py          rebuilds data/graph_stats.csv
├── results/
│   ├── raw_runs/               one JSON per case × configuration (22 + 132 + 132 = 286)
│   ├── summaries/              one CSV per system
│   ├── tables/                 Tables II–III and extra comparisons as CSV
│   └── figures/
└── docs/
    ├── schema.md               node / edge types, ID prefixes, path format
    ├── reproduce.md            step-by-step run order
    └── paper_mapping.md        each paper claim → the file that backs it
```

## Modules

| Code | Module | Nodes | Edges |
|---|---|---|---|
| DEP | Depression | 23 | 33 |
| SUB | Disorders due to substance use | 65 | 72 |
| CMH | Child & adolescent mental and behavioural disorders | 47 | 67 |
| EPI | Epilepsy | 47 | 53 |
| PSY | Psychoses | 20 | 24 |
| SUI | Self-harm / suicide | 18 | 23 |
| **Benchmark total** | | **220** | **272** |
| OTH | Other significant complaints (referral target only) | 17 | 17 |

## Quick start

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # add keys, then: set -a; source .env; set +a
jupyter lab                   # see docs/reproduce.md for the run order
```

Rebuilding Tables II–III from the saved runs needs no API keys: run `notebooks/04_analysis/`
4a → 4d.

## Scope

Cases and reference paths come from the same graph that S1 traverses, so the results measure
conformance to the encoded graph, not diagnostic accuracy or clinical safety (paper §IX).

## Source guideline

mhGAP Intervention Guide version 2.0, World Health Organization, 2016
(https://www.who.int/publications/i/item/9789241549790), licensed CC BY-NC-SA 3.0 IGO.
