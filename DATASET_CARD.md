# Dataset Card: Roman Urdu E-Commerce Review Sentiment

## Summary

This project studies sentiment and language characteristics in Roman Urdu e-commerce reviews, including possible Urdu/English code-switching. It combines an existing dataset with project-specific annotation and evaluation work.

## Upstream data

- **Project:** RU-BiSLTM / RUECD (Roman Urdu E-Commerce Dataset)
- **Creator attribution:** `bilalbaloch1`
- **Upstream repository:** https://github.com/bilalbaloch1/RU-BiSLTM
- **Upstream README description:** 26,824 Roman Urdu reviews with sentiment labels Positive (1), Negative (0), and Neutral (2).
- **Exact downloaded source:** Record the precise Hugging Face repository ID, filename, revision/commit, download date, and checksum here. The path noted during development was described as `ru-BislTM/msin/ruecd.csv`, but it must be verified against the actual downloaded artifact before release.

## Project-derived data

Document the actual counts and transformations for each artifact before publishing:

| Artifact | Count | Notes |
|---|---:|---|
| Upstream source | Verify | Do not assume the upstream total equals the local downloaded row count. |
| Candidate pool | 32,689 unique candidates (project note) | Candidate pool across several sources; not necessarily final data. |
| Qwen-annotated rows | Verify | Record annotation prompt/version, model tag/digest, date, and review policy. |
| Training split | Verify | Record deduplication and split procedure. |
| Validation split | Verify | Keep separate from the final test set. |
| Held-out test split | 2,503 examples (project note) | Confirm current file and split integrity before release. |
| Synthetic Roman Urdu comparison sample | 100 rows (project note) | Mark clearly as synthetic; do not mix with naturally collected user reviews without disclosure. |

## Labels and schema

Include the exact released schema, allowed values, label definitions, and missing-value policy. For evidence spans, state whether each span must be an exact substring of the supplied review. If a schema version was used, include it and link to the relevant annotation instructions.

## Annotation process

The project used local Qwen inference to assist annotation and fine-tuned LAYA for downstream task evaluation. Record exact model versions/digests and prompt revisions. Model-generated labels are not ground truth by default; document human review, adjudication, and quality-control procedures. Keep separate counts for machine-generated labels, manually checked labels, and unresolved cases.

## Known limitations and biases

- Roman Urdu has non-standardized spelling and transliteration.
- Dataset sources may overrepresent certain marketplaces, product categories, regions, or types of users.
- Sentiment and relevance judgments can be subjective.
- Synthetic examples do not represent the natural distribution of actual customers.
- Data leakage can inflate results if duplicates or near-duplicates cross splits.

## License and redistribution

**Do not publish raw data until the exact upstream license and any applicable platform terms have been verified.** A public repository or downloadable file is not, by itself, a redistribution license. If rights are unclear, publish metadata, provenance, code, evaluation procedures, and instructions for users to obtain the original data from its source. Also review model/checkpoint licensing independently.

## Privacy and safety

Inspect review text for names, phone numbers, addresses, order identifiers, and other personal information. Remove or appropriately redact personal information before release, while preserving the validity of evaluation claims. Keep a record of the redaction policy.

## Recommended validation checklist

- [ ] Verify exact source URL, repository ID, revision, download date, and SHA-256 checksum.
- [ ] Verify the license and terms for upstream and project-derived data.
- [ ] Recompute counts after deduplication and cleaning.
- [ ] Confirm train/validation/test disjointness by normalized text and stable source IDs.
- [ ] Confirm no held-out test data was used for prompt or model selection.
- [ ] Audit annotation schema validity and evidence-span substring matches.
- [ ] Separate synthetic and naturally collected examples.
- [ ] Check privacy and personal information.
- [ ] Publish a data statement and limitations.
