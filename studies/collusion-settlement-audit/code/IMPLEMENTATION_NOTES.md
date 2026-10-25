# Protocol implementation notes

## Threshold notation

The parent brief specified strict I>0 for the primary outcome and used >=0.25
and >=0.5 for supplementary thresholds. The locked protocol and reviewer brief
used strict >0.25 and >0.5. The primary definition never changed. To retain the
locked plan transparently, the main supplementary results use the strict >
definitions, and separate boundary checks report >= definitions as well.
This discrepancy was flagged before group-comparison output and the parent's
approval to report both was recorded. The original protocol file is preserved.

## Interpretation and prior work

- The source already stores undefined per-round executed prices as null/NaN.
  We do not claim to repair its missing-value handling.
- The source CI is a highest-buyer-bid index relative to its midpoint benchmark.
  A positive index without trades is an unsettled positive signal, not a
  ground-truth collusion false positive.
- The source's total_welfare_normalized uses a different denominator from our
  gains-from-trade fraction. We do not label the difference as a source error.
- Numeric run suffixes do not establish matched random seeds or initial draws.
- Tests use explicitly synthetic diagnostic fixtures; these are never included
  in the archival research results.
