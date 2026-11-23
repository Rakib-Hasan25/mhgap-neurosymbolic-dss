# Reproducing the paper

All steps run in Jupyter. Notebooks under `notebooks/02_*` to `notebooks/04_*` start with a cell
that finds the repository root, so they can be opened from any folder.

## 0. Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env            # fill in keys
set -a; source .env; set +a
jupyter lab
```

## 1. Build the graph (paper §III) — optional, outputs are already in `data/`

These notebooks ran in Google Colab and still use `/content/drive/...` paths. Point `input_path`
/ `output_path` at the matching folder in `data/` to rerun them.

| Step | Notebook | Output |
|---|---|---|
| Split guideline into module PDFs | `notebooks/01_graph_construction/1a_split_guideline_into_modules.ipynb` | `data/source/modules/<CODE>/source_pages.pdf` |
| OCR each page | `1b_extract_page_text_ocr.ipynb` | `data/source/modules/<CODE>/extracted_pages/` |
| Text → graph JSON | `1c_text_to_graph_json.ipynb` | `data/graphs/<CODE>/mhgap_decision_graph.json` |
| Load into Neo4j | `1d_load_graph_into_neo4j.ipynb` | Neo4j database (needed by S1) |

Graphs were then checked by hand against the source pages.

## 2. Build the benchmark (paper §V) — optional, outputs are already in `data/cases/`

| Step | Notebook | Output |
|---|---|---|
| Reference paths (GPT-5.5-Pro) | `notebooks/02_cases/2a_generate_reference_paths.ipynb` | `data/cases/reference_paths/` |
| Manual check of all 22 paths against the graph | by hand | corrected files in `data/cases/reference_paths/` |
| Back-stories (GPT-5.5) | `2b_generate_virtual_patient_backstories.ipynb` | `data/cases/virtual_patients/` |

`data/cases/cases_22.json` puts all 22 final cases in one file.

## 3. Run the experiments (paper §VI)

| System | Notebook | Needs | Output |
|---|---|---|---|
| S1 symbolic | `notebooks/03_experiments/S1_symbolic_navigator.ipynb` | Neo4j + OpenAI | `results/raw_runs/S1_symbolic/` |
| S2 LLM + graph JSON | `S2_llm_navigator_graph_json.ipynb` | OpenAI + Gemini | `results/raw_runs/S2_llm_graph_json/` |
| S3 LLM + text | `S3_llm_navigator_raw_text.ipynb` | OpenAI + Gemini | `results/raw_runs/S3_llm_raw_text/` |

## 4. Rebuild Tables II–III (paper §VII) — no API keys needed

Run in order:

1. `notebooks/04_analysis/4a_summarize_S1_runs.ipynb` → `results/summaries/S1_symbolic_summary.csv`
2. `4b_summarize_S2_runs.ipynb` → `results/summaries/S2_llm_graph_json_summary.csv`
3. `4c_summarize_S3_runs.ipynb` → `results/summaries/S3_llm_raw_text_summary.csv`
4. `4d_compare_systems_tables_figures.ipynb` → `results/tables/`, `results/figures/`

Table II comes from `results/tables/system_level_comparison.csv`; Table III from
`results/tables/category_level_comparison.csv`. Finding accuracy in the paper is the per-run
mean of `finding_accuracy` in `results/tables/normalized_phase2_eval_rows.csv`.
