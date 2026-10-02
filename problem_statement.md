# Apple Product Support Assistant Problem Statement

## Problem and user

A shopper may need to compare product specifications or interpret Apple Online Store Singapore guidance. Product data can be stale, while store terms may vary by region and product. A fluent answer that confuses a model configuration, states a made-up policy threshold or omits a qualifier can mislead a purchase.

The primary persona is Mei, an Apple online shopper in Singapore. She wants a concise, source-backed answer before checkout and a clear statement when the provided evidence does not settle her question. This prototype does not access orders, issue refunds or make individual warranty decisions.

## Proposed system

The prototype retrieves from ten short paraphrased notes based on Apple official sources, then sends selected passages to a language model with a grounding instruction. The notes retain source URLs and dates checked; the source register is `sources.md`. The runner compares top-k=1 and top-k=2. It retrieves whole notes and does not currently chunk them.

## Scope and baseline

The current corpus covers iPhone 15 Pro Max battery, M3 Max unified memory, Apple Watch Ultra 2 dive limits, Apple Pencil compatibility, eligible Apple Singapore returns, Trade In timing, Singapore education-store quantity limits, shipping signatures, Apple warranty and AppleCare+ pricing limitations. Keyword search or a static FAQ is the non-generative baseline. The generative system is useful only if it retrieves correctly, preserves qualifications and refuses unsupported exact claims.

## Evaluation and target

The fixed test set contains five typical questions, three edge cases and two adversarial/unsupported prompts. The target is at least 80% manually reviewed strict answer completeness and 100% correct refusal on unsupported cases. Retrieval hit rate, answer pass rate, refusal rate, latency and tokens should be reported separately. The earlier 7/10 and 9/10 results are invalidated because the classroom corpus included wrong or unsourced claims; the first corrected-corpus run scored 7/10 strict answers (70%), below target. The revised-prompt model comparison has been run and manually scored: strict completeness was 8/10 (80%) at k=1 and 9/10 (90%) at k=2, with 3/3 correct refusals at each setting. The raw outputs and case-level judgments are in `results/top_k_comparison_final_prompt_run.csv` and `evaluation_results.csv`. The final run also exposed a citation-format issue: Evidence IDs point to the expected source notes, but none of the 20 answers put the Evidence reference on its own correctly bracketed line; see `results/evidence_audit.csv`.

## Risks and responsible use

The principal risks are source staleness, retrieval misses, hallucinated policy details and ambiguous citations. The assistant should direct users to the linked official page for current terms and individual decisions. This small prototype is not a validated benchmark or a substitute for Apple Support.
