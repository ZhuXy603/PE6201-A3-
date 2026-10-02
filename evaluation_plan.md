# Evaluation and Top-k Comparison

## Current case set

The 10 questions in `run_project.py` use the corrected, source-attributed corpus in `data/Part2_notebook.ipynb`: five typical, three edge and two adversarial/unsupported probes. Each case records required facts, relevant corpus indices, refusal expectation and claims that must not appear. The authoritative sources and date checked are listed in `sources.md`.

Corpus indices are zero-based. In generated context, passages have a retrieval rank and a separate corpus ID; do not treat rank as source identity.

| ID | Case | Required check | Corpus index | Refuse? |
|---|---|---|---:|---|
| typical_1 | M3 Max unified memory | Up to 128GB; 96GB is not the maximum | 1 | No |
| typical_2 | iPhone 15 Pro Max playback | Up to 29h playback; 25h streamed | 0 | No |
| typical_3 | Watch Ultra 2 diving | EN13319 recreational diving to 40m; not below 40m | 2 | No |
| typical_4 | Singapore online return window | Eligible purchases generally up to 14 calendar days; qualify exceptions | 4 | No |
| typical_5 | Trade-in device timing | Received within 14 days after estimate; condition matches | 5 | No |
| edge_1 | Pencil 2 with M4 iPad Pro | Incompatible; Pencil Pro and USB-C are compatible | 3 | No |
| edge_2 | Education-store MacBook limit | One per year in Singapore | 6 | No |
| edge_3 | Blanket $750 signature threshold | No universal threshold stated; direct to order/checkout | 7 | Yes |
| adversarial_1 | Invented five-year warranty | Reject claim; note one-year limited warranty and qualifiers | 8 | Yes |
| adversarial_2 | AppleCare+ exact price | Refuse/qualify because this corpus has no price | 9 | Yes |

## Scoring protocol

The same ten questions are run with top-k=1 and top-k=2. A retrieval hit means the required source record is present. A strict answer pass requires the required facts, correct qualifiers and no forbidden claim. For unsupported cases, refusal is scored separately: it passes when the answer explicitly says the notes do not establish the requested claim. `evaluation_results.csv` records both strict answer and refusal judgments. The runner logs retrieved IDs/ranks, text, latency and provider token counts; it does not implement semantic grading.

## Revised-prompt run (2 October 2026)

The first corrected-corpus run is retained at `results/top_k_comparison_first_scored_run.csv`. It scored 7/10 strict answers at both settings. After tightening the prompt, the user ran the same 10 cases again using local semantic embeddings and OpenRouter. The current run is preserved at `results/top_k_comparison_final_prompt_run.csv`; the working output is `results/top_k_comparison.csv`. All 10 required source records were retrieved at both settings.

Manual strict answer checks pass 8/10 at k=1 and 9/10 at k=2. Correct refusals pass 3/3 at each setting. The k=1 Watch response gives the 40m recreational limit but omits the warning against diving below 40m; k=2 includes the warning. Both settings correctly refuse the unsupported five-year warranty, but omit the source-supported one-year limited-warranty correction, so that case fails strict completeness while passing refusal. All other strict checks pass, including the order-specific next step for the unsupported signature threshold.

| Setting | Retrieval hits | Strict answer checks | Correct refusals | Median generation latency | Avg prompt tokens | Avg completion tokens |
|---|---:|---:|---:|---:|---:|---:|
| top-k=1 | 10/10 | 8/10 (80%) | 3/3 (100%) | 1,261 ms | 339 | 36 |
| top-k=2 | 10/10 | 9/10 (90%) | 3/3 (100%) | 1,157 ms | 456 | 39 |

On this small set, k=2 adds one strict pass, including the missing dive-safety warning, while average prompt tokens rise by about 34% (339 to 456). The median API-call latency was 104 ms lower for k=2 in this particular run; this single run does not establish that k=2 is generally faster. Latency is generation-call latency, not end-to-end time. Token counts are cost proxies, not dollar estimates. With only ten self-authored cases and one run per setting, these figures are prototype evidence, not a broad reliability benchmark.

The stated ≥80% strict-answer target was met at both settings in this run (k=1 exactly at threshold; k=2 above it). The rubric gap on the warranty probe remains visible rather than being counted as a strict pass. Retrieval hit rate is not evidence of factual correctness by itself.


## Run provenance, cost and citation audit

The run log dates the revised-prompt run to 2 October 2026. The runner's default model is `qwen/qwen-2.5-7b-instruct`; however, the historical output does not store the effective model or `PE6201_MODEL` override, so the default is an assumption, not a verified fact. The run used 7,947 prompt and 748 completion tokens over 20 requests. At the OpenRouter listed rate of $0.10/M input and $0.20/M output tokens, the estimated total is $0.0009443 if the default model was used. Actual billing was not recorded and should be checked in OpenRouter activity. Pricing reference (checked 2 October 2026): [OpenRouter Qwen2.5 7B Instruct pricing](https://openrouter.ai/qwen/qwen-2.5-7b-instruct). Details are in `results/run_metadata.json`.

I checked the Evidence references in all 20 answers. All 20 cite an ID present in that row's retrieved context and all 20 point to the case's expected source note. However, 0/20 conform to the requested exact format of a separate final line `Evidence: [id]`: most append unbracketed `Evidence: id` to answer prose, and three append bracketed IDs to prose. The `evidence_format_pass` check requires the Evidence reference on its own final line, in the exact form `Evidence: [id]` (or `[id, id]` for multiple sources); an inline `Evidence: [id]` does not pass. The model identifies the right source but fails the output-format instruction. `evidence_ids_in_retrieved_context` checks only that each cited ID appears among that row’s retrieved IDs; it does not require citing every retrieved ID. This check establishes ID alignment and note relevance, not independent entailment of every sentence; those need human source comparison. The merged row-level review is in `evaluation_results.csv`; the focused check is in `results/evidence_audit.csv`.

The `adversarial_1` answers are short (11 completion tokens each) and end with a complete Evidence reference, so there is no visible sign of truncation. The runner did not save the API `finish_reason`, so provider-side truncation cannot be ruled out conclusively. The rubric omission is therefore recorded as an observed model omission, with this logging limitation disclosed. The prompt was deliberately strengthened in response to observed failures (safety ceilings, corrections, and order-specific next steps); this creates a risk of tuning to the same ten self-authored cases. Results should not be read as evidence of general performance.

A small literal L1 checker (`audit_outputs.py`) writes `results/l1_heuristic_audit.csv` with required-term omissions and exact forbidden-string matches. It is a review aid only: paraphrases and negation can create false positives or false negatives, so its flags do not change manual scores.
