# Data and Corpus Notes

The current runner reads ten concise, source-attributed notes from `data/Part2_notebook.ipynb`. They are paraphrases of official Apple pages, not a full scrape. Each note includes a source URL and the date checked; the source register is in `sources.md`. Scope is Apple Singapore product/support and store guidance, except the M3 Max product announcement, which is a historical model fact.

The former classroom corpus is preserved as `audit/Part2_classroom_original_invalidated.ipynb` for audit only. Do not use it as evidence or mix its answers into the current score. It contains invented or incorrect claims, including 96GB as the M3 Max maximum (96GB is a real 14-core configuration, but 16-core M3 Max supports up to 128GB), 24 hours for iPhone 15 Pro Max playback, 85m for Apple Watch Ultra 2, fabricated trade-in deadlines/limits, a $750 signature threshold, and made-up return details. See `sources.md` for corrected claims.

The current corpus intentionally omits unsupported exact claims. Where the official page does not establish a threshold, exception or transaction combination, the assistant should say the notes do not say. Sources can change, so re-check dated policies before any real-world use.
