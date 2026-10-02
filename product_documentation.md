# Product Documentation

## Persona
Mei is an Apple online shopper in Singapore comparing products before checkout. She wants a concise answer with a source and a clear refusal when the supplied sources do not establish an answer.

## Input and output
**Input:** a natural-language product or Apple Singapore online-store question.

**Output:** an answer grounded in one or more retrieved source-attributed notes, plus source IDs; or a refusal when the notes do not establish the exact claim. Model outputs are manually checked against the evaluation rubric.

## Architecture
```text
Apple official pages
        │ paraphrase + URL + checked date
        ▼
10 source-attributed notes in notebook
        │ local retrieval (MiniLM; TF-IDF fallback)
        ▼
top-k context with retrieval rank + corpus ID
        │ grounded prompt
        ▼
OpenRouter model ──► answer / refusal + requested evidence IDs
        │
        └── manual case-by-case evaluation
```
The current code retrieves whole records; it does not implement overlapping chunking.

## Targets and measurement status
| Metric | Target | Reached |
|---|---:|---:|
| Strict answer completeness | ≥80% | Revised-prompt run: k=1 8/10 (80%); k=2 9/10 (90%) |
| Refusal on unsupported probes | 100% | 3/3 (100%) at both k settings |
| Retrieval hit rate | Report for k=1 and k=2 | 10/10 for both; small-set limitation |
| Median generation latency | Report for k=1 and k=2 | k=1: 1,261 ms; k=2: 1,157 ms |
| Avg prompt/completion tokens | Report for k=1 and k=2 | k=1: 339/36; k=2: 456/39 |

These are manual judgments on ten self-authored questions and one run per setting, not a broad reliability benchmark. The prompt was tuned after inspecting failures, so performance may overfit this test set. k=1 omitted the 40m safety ceiling warning; both settings omitted the one-year warranty correction in the invented-warranty case. See `evaluation_plan.md`, `evaluation_results.csv` and `results/top_k_comparison_final_prompt_run.csv`.
