# All prompts

Every LLM prompt used in the paper pipeline, copied verbatim from the notebooks.
Each prompt also lives in its own file in this folder. `{...}` marks a value filled in at run time.

| # | Stage | Prompt | Model | File |
|---|---|---|---|---|
| 1 | Graph extraction | Page OCR (Gemini) | gemini-2.5-pro | `01_graph_extraction/page_ocr_gemini.txt` |
| 2 | Graph extraction | Page OCR (OpenAI variant) | gpt-5.3-chat-latest | `01_graph_extraction/page_ocr_openai.txt` |
| 3 | Graph extraction | Text to decision-graph JSON (early draft) | Gemini | `01_graph_extraction/text_to_graph_json_draft.txt` |
| 4 | Graph extraction | Text to final graph JSON + clinical logic MD | unknown | `01_graph_extraction/text_to_graph_json_final.MISSING.txt` |
| 5 | Case generation | Reference-path generator: developer message | gpt-5.5-pro | `02_case_generation/reference_path_generator_developer.txt` |
| 6 | Case generation | Reference-path generator: output JSON schema | gpt-5.5-pro | `02_case_generation/reference_path_output_schema.json` |
| 7 | Case generation | Reference-path generator: single-hop instructions | gpt-5.5-pro | `02_case_generation/reference_path_single_hop_instructions.txt` |
| 8 | Case generation | Reference-path generator: multi-hop instructions | gpt-5.5-pro | `02_case_generation/reference_path_multi_hop_instructions.txt` |
| 9 | Case generation | Back-story generator: developer message | gpt-5.5 | `02_case_generation/backstory_developer.txt` |
| 10 | Case generation | Back-story generator: task and requirements | gpt-5.5 | `02_case_generation/backstory_task_and_requirements.txt` |
| 11 | Virtual patient (answer normalization) | S1 virtual patient | gpt-4.1-mini | `03_virtual_patient/S1_virtual_patient.txt` |
| 12 | Virtual patient (answer normalization) | S2 / S3 virtual patient | gpt-4o-mini | `03_virtual_patient/S2_S3_virtual_patient.txt` |
| 13 | Navigators | S2 navigator (LLM + graph JSON) | gpt-4o | `04_navigators/S2_graph_json_rules.txt` |
| 14 | Navigators | S3 navigator (LLM + clinical-logic text) | gpt-4o | `04_navigators/S3_raw_text_rules.txt` |

## 1. Graph extraction

### 1. Page OCR (Gemini)

- **Model:** gemini-2.5-pro (page image + prompt)
- **Used in:** `notebooks/01_graph_construction/1b_extract_page_text_ocr.ipynb`
- **File:** `prompts/01_graph_extraction/page_ocr_gemini.txt`
- **Notes:** One call per guideline page image (300 DPI). Output saved to data/source/modules/<CODE>/extracted_pages/.

````text
You are performing structured OCR on a clinical guideline page.

Extract ALL visible information from the image.

Rules:

1. Transcribe all text exactly as written.
2. Preserve the logical reading order.
3. If the page contains flowcharts or decision diagrams:
   - Identify each box or node.
   - Transcribe the text inside each box.
   - Describe connections between boxes using arrows.
   - Explicitly label decision paths such as YES / NO.

4. If there are tables:
   - Convert them into a clear text table format.

5. If there are bullet lists:
   - Preserve the list structure.

6. Do NOT summarize or interpret.
7. Do NOT skip any text.

Output should be a structured transcription that preserves the
layout and relationships between elements.

Focus especially on preserving decision flow and connections.
````

### 2. Page OCR (OpenAI variant)

- **Model:** gpt-5.3-chat-latest (image_url, detail=high)
- **Used in:** `notebooks/01_graph_construction/1b_extract_page_text_ocr.ipynb`
- **File:** `prompts/01_graph_extraction/page_ocr_openai.txt`
- **Notes:** Alternative OCR path with the same rules.

````text
You are performing structured OCR on a clinical guideline page.
Extract ALL visible information from the image.

Rules:
1. Transcribe all text exactly as written.
2. Preserve the logical reading order.
3. If the page contains flowcharts or decision diagrams:
   - Identify each box or node.
   - Transcribe the text inside each box.
   - Describe connections between boxes using arrows (e.g., [Box A] -> [Box B]).
   - Explicitly label decision paths such as YES / NO.
4. If there are tables:
   - Convert them into a clear text table format or Markdown.
5. If there are bullet lists:
   - Preserve the list structure.
6. Do NOT summarize or interpret.
7. Do NOT skip any text.

Output should be a structured transcription that preserves the layout and relationships.
````

### 3. Text to decision-graph JSON (early draft)

- **Model:** Gemini (model set in notebook)
- **Used in:** `notebooks/01_graph_construction/1c_text_to_graph_json.ipynb`
- **File:** `prompts/01_graph_extraction/text_to_graph_json_draft.txt`
- **Notes:** WARNING: this draft asks for `Question` nodes and `NEXT_YES` edges. The final graphs in data/graphs use `assessment/management/diagnosis/referral/exit` nodes and `condition` edges, so the prompt that produced the final graphs (and mhgap_clinical_logic.md) is not in the notebooks. Add it here.

````text
Convert the following mhGAP Depression section into a structured decision graph.

STRICT RULES:
- Output only valid JSON.
- Do NOT include explanations or markdown code blocks (no ```json).
- Do NOT summarize.
- Do NOT include paragraphs.
- Extract only decision logic.

OUTPUT FORMAT SCHEMA:
{
  "module": { "id": "DEP", "name": "Depression" },
  "nodes": [
    { "id": "DEP_Q1", "type": "Question", "text": "...", "phase": "assessment", "symptom_tag": "...", "is_core": true }
  ],
  "relationships": [
    { "from": "DEP_Q1", "to": "DEP_Q2", "type": "NEXT_YES" }
  ],
  "diagnosis": [
    { "id": "DEP_MODERATE", "criteria": { "min_core": 2, "min_total": 5, "duration_days": 14 } }
  ],
  "safety_triggers": [
    { "id": "DEP_SUICIDE", "condition": "suicidal_ideation == true", "risk": "high" }
  ],
  "management": [
    { "id": "DEP_MODERATE_PLAN", "applies_to": "DEP_MODERATE", "interventions": ["behavioral_activation", "ssri"] }
  ]
}

Now convert the following text:
---
{all_text_content}
---
````

### 4. Text to final graph JSON + clinical logic MD

- **Model:** unknown
- **Used in:** `not in notebooks`
- **File:** `prompts/01_graph_extraction/text_to_graph_json_final.MISSING.txt`
- **Notes:** Placeholder. Needed for the paper reproducibility claim.

````text
TODO: paste the prompt that produced the final data/graphs/<CODE>/mhgap_decision_graph.json files.
TODO: paste the prompt that produced data/graphs/<CODE>/mhgap_clinical_logic.md (used by S3).
````

## 2. Case generation

### 5. Reference-path generator: developer message

- **Model:** gpt-5.5-pro (OpenAI Responses API, max_output_tokens=20000, json_schema)
- **Used in:** `02_cases/2a_generate_reference_paths.ipynb`
- **File:** `prompts/02_case_generation/reference_path_generator_developer.txt`
- **Notes:** User message = JSON {"task": ..., "payload": ...} where payload is the single-hop or multi-hop object below.

````text
You convert mental-health decision graph JSON into the requested output JSON. Return one valid JSON object matching the provided schema. Do not include markdown. The top-level object must contain only cases. Do not include warnings, metadata, or decision_trace. Do not invent graph nodes or relationships. If graph data is incomplete or no supported new case exists, return {"cases": []}.
````

### 6. Reference-path generator: output JSON schema

- **Model:** gpt-5.5-pro
- **Used in:** `02_cases/2a_generate_reference_paths.ipynb`
- **File:** `prompts/02_case_generation/reference_path_output_schema.json`
- **Notes:** Passed as text.format json_schema (strict=False).

````json
{
  "type": "object",
  "additionalProperties": false,
  "required": [
    "cases"
  ],
  "properties": {
    "cases": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": true,
        "required": [
          "case_id",
          "category",
          "source_module",
          "referred_module",
          "final_module",
          "diagnosis_reached",
          "diagnosis_node_id",
          "exit_node_id",
          "node_sequence"
        ],
        "properties": {
          "case_id": {
            "type": "string"
          },
          "category": {
            "type": "string",
            "enum": [
              "single_hop_positive",
              "single_hop_negative",
              "multi_hop_positive",
              "multi_hop_negative"
            ]
          },
          "source_module": {
            "type": "string"
          },
          "referred_module": {
            "anyOf": [
              {
                "type": "string"
              },
              {
                "type": "null"
              }
            ]
          },
          "final_module": {
            "type": "string"
          },
          "diagnosis_reached": {
            "type": "boolean"
          },
          "diagnosis_node_id": {
            "anyOf": [
              {
                "type": "string"
              },
              {
                "type": "null"
              }
            ]
          },
          "exit_node_id": {
            "anyOf": [
              {
                "type": "string"
              },
              {
                "type": "null"
              }
            ]
          },
          "node_sequence": {
            "type": "array",
            "items": {
              "type": "object",
              "additionalProperties": true
            }
          }
        }
      }
    }
  }
}
````

### 7. Reference-path generator: single-hop instructions

- **Model:** gpt-5.5-pro
- **Used in:** `02_cases/2a_generate_reference_paths.ipynb`
- **File:** `prompts/02_case_generation/reference_path_single_hop_instructions.txt`
- **Notes:** Sent inside payload with flow_type="single_hop", requested_category, max_cases_to_return=1, existing_cases_to_avoid, required_case_schema, graph.

````text
- Use only the provided module graph.
- Generate at most one case for this request.
- If requested_category is set, generate only that category.
- If no supported new case exists for requested_category, return exactly {"cases": []}.
- Start from the node where is_starting is true.
- Classify the case as single_hop_positive or single_hop_negative.
- Positive means the path reaches a diagnosis confirming the module syndrome.
- Negative means the path exits or rules out the module syndrome without positive diagnosis.
- Avoid duplicating any path listed in existing_cases_to_avoid.
- Preserve node objects from graph.nodes. Do not invent or rewrite node text.
- Inline the flow in node_sequence: for each node except the last, add condition_met equal to the relationship.condition used to reach the next node in the sequence.
- condition_met must match an edge in graph.relationships with from=this_node.id and to=next_node.id.
- Do not return relationship_sequence.
- Do not include decision_trace, warnings, or metadata.
- Do not invent missing nodes, missing edges, or unsupported paths.
- Do not create unrealistic data to satisfy a requested count.
````

### 8. Reference-path generator: multi-hop instructions

- **Model:** gpt-5.5-pro
- **Used in:** `02_cases/2a_generate_reference_paths.ipynb`
- **File:** `prompts/02_case_generation/reference_path_multi_hop_instructions.txt`
- **Notes:** Sent inside payload with flow_type="multi_hop", source_graph and target_graph.

````text
- Use exactly two graphs: source_graph and target_graph.
- Generate at most one case for this request.
- If requested_category is set, generate only that category.
- If no supported new case exists for requested_category, return exactly {"cases": []}.
- Find referral nodes in source_graph whose target_module matches target_graph.module.id.
- A multi-hop case starts at the source starting node, reaches one supported referral, then continues from the target graph starting node.
- Allow only one referral hop total.
- If a second referral is needed or encountered, skip that unsupported case.
- Classify the case as multi_hop_positive or multi_hop_negative.
- Positive means the target graph path reaches a diagnosis confirming the referred module syndrome.
- Negative means the target graph path exits or rules out the referred module syndrome without positive diagnosis.
- Avoid duplicating any path listed in existing_cases_to_avoid.
- Preserve node objects from the provided graph nodes. Do not invent or rewrite node text.
- Inline the flow in node_sequence: for each node except the last, add condition_met equal to the relationship.condition used to reach the next node in the sequence (within the same graph).
- When the sequence crosses from the source graph to the target graph (the referral hop), omit condition_met on the referral node.
- Do not return relationship_sequence.
- Do not include decision_trace, warnings, or metadata.
- Do not invent missing nodes, missing edges, or unsupported paths.
- Do not create unrealistic data to satisfy a requested count.
````

### 9. Back-story generator: developer message

- **Model:** gpt-5.5 (OpenAI Responses API)
- **Used in:** `02_cases/2b_generate_virtual_patient_backstories.ipynb`
- **File:** `prompts/02_case_generation/backstory_developer.txt`
- **Notes:** User message = JSON {task, requirements, node_sequence, conditions, output_contract}.

````text
You generate a virtual patient backstory (hidden context) for clinical decision paths. Return only the story text. Do not add headers, bullet points, or JSON.
````

### 10. Back-story generator: task and requirements

- **Model:** gpt-5.5
- **Used in:** `02_cases/2b_generate_virtual_patient_backstories.ipynb`
- **File:** `prompts/02_case_generation/backstory_task_and_requirements.txt`
- **Notes:** conditions = YES/NO edges taken on the reference path; output_contract = {"format": "text_only", "field": "user_story"}.

````text
Task: Generate a rich, concise short virtual patient backstory with a unique persona.

Requirements:
- The persona must be Bangladeshi (name, setting, and life context should fit Bangladesh).
- Create a unique persona for each case; do not reuse the same name, age, occupation, or location across cases.
- The backstory must implicitly answer every YES/NO condition in the provided path or node_sequence.
- Both YES and NO conditions must be represented in the story.
- For NO conditions, include realistic evidence that the symptom, behavior, risk factor, or event is absent; do not simply omit it.
- The story should contain enough information for an assessor to infer the correct answer without guessing.
- Do not list answers explicitly as a checklist; weave them into the narrative.
- Stay consistent with the path sequence and clinical context.
- Keep the story realistic and medically coherent.
````

## 3. Virtual patient (answer normalization)

### 11. S1 virtual patient

- **Model:** gpt-4.1-mini (code default via OPENAI_YESNO_MODEL; not recorded in run logs), temperature=0, max_output_tokens=25
- **Used in:** `notebooks/03_experiments/S1_symbolic_navigator.ipynb`
- **File:** `prompts/03_virtual_patient/S1_virtual_patient.txt`
- **Notes:** Developer message: "Output must be one token: YES, NO, or NO_ANSWER.". The YES/NO/NO_ANSWER output is the normalized condition that selects the graph edge; there is no separate normalizer call.

````text
You are simulating a virtual patient during a clinical assessment.
Answer the clinician's question using ONLY the patient story below.

PATIENT STORY:
{self.user_story}

CLINICIAN QUESTION:
{question}

RULES:
- Return exactly one of: YES, NO, NO_ANSWER.
- Use NO_ANSWER only if the story truly does not contain enough info.
````

### 12. S2 / S3 virtual patient

- **Model:** gpt-4o-mini, temperature=0, max_output_tokens=25
- **Used in:** `notebooks/03_experiments/S2_llm_navigator_graph_json.ipynb, S3_llm_navigator_raw_text.ipynb`
- **File:** `prompts/03_virtual_patient/S2_S3_virtual_patient.txt`
- **Notes:** Same developer message as S1 (prompts/03_virtual_patient/developer.txt). Identical prompt in S2 and S3. Note: model differs from S1.

````text
You are a virtual patient.
Answer the clinician question using ONLY the story.
Return exactly one of: YES, NO, NO_ANSWER.
Use NO_ANSWER only if the story truly does not contain enough info.

PATIENT STORY:
{user_story}

QUESTION:
{question_text}
````

## 4. Navigators

### 13. S2 navigator (LLM + graph JSON)

- **Model:** gpt-4o, gpt-4.1, gpt-4o-mini (OpenAI Responses API); gemini-2.5-flash, gemini-2.5-pro, gemini-3.5-flash (google-genai); temperature=0
- **Used in:** `notebooks/03_experiments/S2_llm_navigator_graph_json.ipynb`
- **File:** `prompts/04_navigators/S2_graph_json_rules.txt`
- **Notes:** OpenAI developer message: "Return only a JSON object with key next_node_id." (Gemini gets only the user payload). User payload = JSON {graph, current_node_id, previous_steps, rules}.

````text
- Choose the next node_id to ask from graph.nodes.
- Try to follow graph.relationships using the most recent YES/NO/NEXT answer.
- Return only a JSON object with a single key next_node_id.
- Do not invent nodes that are not in graph.nodes.
````

### 14. S3 navigator (LLM + clinical-logic text)

- **Model:** gpt-4o, gpt-4.1, gpt-4o-mini (OpenAI Responses API); gemini-2.5-flash, gemini-2.5-pro, gemini-3.5-flash (google-genai); temperature=0
- **Used in:** `notebooks/03_experiments/S3_llm_navigator_raw_text.ipynb`
- **File:** `prompts/04_navigators/S3_raw_text_rules.txt`
- **Notes:** Same developer message as S2. User payload = JSON {mhgap_clinical_logic_md, nodes, current_node_id, previous_steps, rules}. The text given is data/graphs/<CODE>/mhgap_clinical_logic.md, not the original guideline pages.

````text
- Choose the next node_id to ask from nodes only.
- Use the clinical logic markdown to decide the next step based on previous YES/NO/NEXT answers.
- Return only a JSON object with a single key next_node_id.
- Do not invent node ids that are not present in nodes.
````
