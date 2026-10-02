# Contribution archive — 2026-10-02

One upstream PR was submitted, three additional upstream changes are prepared, and a validation fix was published to Public Data Sentinel. This archive preserves the patches, descriptions, and executed checks. PR #291 awaits maintainer review.

| Patch | Change | Status | Upstream base |
| --- | --- | --- | --- |
| [FinanceDataReader #272](patches/fdr-yahoo-duplicate-dates.patch) | Keep the final complete Yahoo quote row per normalized daily date; prevent duplicate-index failures during multi-symbol alignment. | [PR #291 open](https://github.com/FinanceData/FinanceDataReader/pull/291) | `addcbb7e887f0db6176a87d323de5de28357b5f4` |
| [ETLHelper #232](patches/etlhelper-232.patch) | Add a runnable SQLite branching pipeline recipe with empty-branch and empty-input tests. | [Public branch](https://github.com/qorud02/etlhelper/tree/docs-branching-pipeline-recipe); PR not submitted | `8a2b413585d892443037679acf4559d4e4d2583e` |
| [urllib3 #5294](patches/urllib3-5294.patch) | Reject NaN connect/read/total timeouts during construction; add four regression cases and a changelog fragment. | Archived; overlaps external [PR #5295](https://github.com/urllib3/urllib3/pull/5295); do not submit a duplicate | `796d200d3070ead69ec3a5d848fecf52a2249b59` |
| [yargs dotted config documentation](patches/yargs-strict-dotted-config.patch) | Explain literal dotted configuration keys with `dot-notation: false` in strict mode; document a working example. | Prepared; not submitted | `10f1dda5991fba2cea6a4b4dc6bd90da6e5292b2` |

FinanceDataReader #291 is the only submitted new upstream PR. ETLHelper's source PR attempts returned HTTP 403; a [prefilled manual submission link](verification/etlhelper-manual-pr.md) is available. New-fork creation was denied for urllib3 and yargs; neither archived patch was submitted by this session.

Later user OAuth approval completed, but ETLHelper source-PR and yargs-fork retries still returned HTTP 403 because the managed route retained app authentication. Submission permissions remain unresolved. After this archive's original preparation, `mikamikasuki` opened overlapping urllib3 [PR #5295](https://github.com/urllib3/urllib3/pull/5295) at 11:43:49 UTC on 2026-10-02; upstream rules prohibit submitting a duplicate.

[Public Data Sentinel maintenance](verification/public-data-sentinel-maintenance.md) is complete on its default branch: malformed array/object contract types now produce a clean CLI error with exit status 2. All 27 unittest tests passed.

See [verification notes](verification/README.md) for exact checks and limitations, and [PR descriptions](pr-bodies/) for submitted/proposed bodies. OpenAI Codex assisted with development and independent review.

## Apply a patch

The files are standard `git format-patch` output suitable for `git am`. Start from the listed upstream base in a clean checkout and create a working branch:

```sh
# In a FinanceDataReader checkout:
git switch -c fix-yahoo-daily-duplicates addcbb7e887f0db6176a87d323de5de28357b5f4
git am /path/to/archive/patches/fdr-yahoo-duplicate-dates.patch

# In an ETLHelper checkout:
git switch -c docs-branching-pipeline-recipe 8a2b413585d892443037679acf4559d4e4d2583e
git am /path/to/archive/patches/etlhelper-232.patch

# In an urllib3 checkout:
git switch -c fix-nan-timeout 796d200d3070ead69ec3a5d848fecf52a2249b59
git am /path/to/archive/patches/urllib3-5294.patch

# In a yargs checkout:
git switch -c docs-strict-dotted-config 10f1dda5991fba2cea6a4b4dc6bd90da6e5292b2
git am /path/to/archive/patches/yargs-strict-dotted-config.patch
```

All four upstream patches were independently applied to pristine local clones at these bases, and the resulting trees matched the prepared changes. Later upstream commits may require rebasing or conflict resolution. Check for newer overlapping contributions before submitting the remaining patches.

## Verify the yargs example

After applying the yargs patch, install that checkout's dependencies and build it using its standard project commands. Then run:

```sh
node /path/to/archive/verification/yargs-doc-verification.mjs /path/to/yargs-checkout
```

The verifier accepts the checkout path as its sole argument. It checks strict-mode behavior, JSON configuration, CLI precedence, unknown-option rejection, and the exact documented JavaScript example. It makes no network requests.
