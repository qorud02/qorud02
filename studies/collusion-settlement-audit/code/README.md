# Settlement-aware evidence audit

Independent analysis code for the 20-session primary comparison in the report.
The original LLM experiments, prompts, raw logs and original metrics are from
Agrawal et al. (2025), *Evaluating LLM Agent Collusion in Double Auctions*,
arXiv:2507.01413, https://doi.org/10.48550/arXiv.2507.01413.

## Reproduce

Use Python 3.12 (tested with 3.12.9). No third-party packages, credentials,
model endpoints or new inference costs are required.

From the project root, containing code/, data/ and results/:

    python code/download.py --phase primary
    python code/analyze.py --scope primary
    python code/test_analyze.py

The downloader requires internet access to public raw.githubusercontent.com.
It pins commit 2bb2a7e22860160d1fddb5d2e5cb460cc6ec6aff and checks the Git
blob SHA-1 and byte length of every downloaded file. It also records SHA-256.
Existing cached files are validated before reuse. The analyzer works offline
once the pinned inputs are present.

## Files

- protocol.json and protocol.sha256: the locked retrospective analysis plan.
- IMPLEMENTATION_NOTES.md: threshold-boundary clarification and interpretation.
- download.py: pinned public-source downloader; no inference requests.
- analyze.py: strict parser, source reproduction, session summaries and tests
  of the primary group contrast.
- test_analyze.py: synthetic integrity fixtures and archived-result checks.
- ../data/source_manifest.json: source code and metadata for all 75 archived
  sessions; metadata are used to establish the 20-session eligible population.
- ../data/outcome_manifest.json: declared outcome files. Only the 20 primary
  sessions were downloaded for this report. The other 55 sessions were not
  analyzed and do not enter any reported statistic.
- ../results/summary_primary.json: group means, differences, bootstrap intervals,
  exact primary permutation test and source-reproduction checks.
- ../results/sessions_primary.csv: one row per independent session.
- ../results/rounds_primary.csv: derived numeric round evidence, not raw messages.
- ../results/source_reproduction_primary.json: all 300 source comparisons.
- ../results/stored_judge_summary_primary.json: optional descriptive summaries
  of already stored source judgments, never ground-truth labels.

## Statistical interpretation

The primary unit is an independent experimental session, ten per condition.
The 600 rounds are not treated as 600 independent treatment replicates.
The primary test enumerates all 184,756 assignments using integer count sums;
ties count as extreme. Bootstrap intervals resample sessions independently
within condition, using fixed seeds and 20,000 replicates.

A positive original index with no trade is an unsettled positive signal.
It is not proof of a false-positive collusion judgment, no harm, or no collusion.
Undefined executed prices remain missing; they are never replaced by zero.
The original source already stores missing executed prices appropriately.
The price benchmark 90 is the source implementation's midpoint reference.

## Scope and distribution

No new LLM experiments were run. All archived logs predate this sprint.
Only the independent analysis, evidence labels, validation and report are new.
No LICENSE/COPYING/NOTICE file was found in the source tree. The report's public
package therefore excludes the original logs/messages and original code.
Use the pinned downloader to retrieve source material from its original host.
Only new code, manifests, attribution and aggregate/derived results are intended
for distribution. The report is reproduced with the primary option above.

## Validation

Sixteen distinct integrity checks were validated across the initial suite and
the source-validation update. These cover strict parsing, missing inputs,
threshold boundaries, no-trade prices, trade-volume/surplus conservation, exact
permutation ties, deterministic bootstrap seeds and pinned input hashes.
An independent implementation reproduced 260 session fields and verified all
143 downloaded files. Detailed test and review logs accompany the report.
