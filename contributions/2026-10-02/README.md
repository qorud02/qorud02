# Contribution archive — 2026-10-02

Three tested upstream patches are preserved here. The FinanceDataReader change was submitted as [PR #291](https://github.com/FinanceData/FinanceDataReader/pull/291) through an existing user-owned fork; review and merge are pending. The urllib3 and yargs patches remain prepared locally because GitHub integration permissions prevented creating their required new forks. An attempted external yargs issue comment was also rejected with HTTP 403. Publishing this archive does not submit the remaining patches upstream. No patch is claimed as merged.

| Patch | Change | Status | Upstream base |
| --- | --- | --- | --- |
| [FinanceDataReader #272](patches/fdr-yahoo-duplicate-dates.patch) | Keep the final complete Yahoo quote row per normalized daily date; prevent duplicate-index failures during multi-symbol alignment. | [PR #291 open](https://github.com/FinanceData/FinanceDataReader/pull/291) | `addcbb7e887f0db6176a87d323de5de28357b5f4` |
| [urllib3 #5294](patches/urllib3-5294.patch) | Reject NaN connect/read/total timeouts during construction; add four regression cases and a changelog fragment. | Prepared; not submitted | `796d200d3070ead69ec3a5d848fecf52a2249b59` |
| [yargs dotted config documentation](patches/yargs-strict-dotted-config.patch) | Explain literal dotted configuration keys with `dot-notation: false` in strict mode; document a working example. | Prepared; not submitted | `10f1dda5991fba2cea6a4b4dc6bd90da6e5292b2` |

See [verification notes](verification/README.md) for executed checks and limitations, and [PR descriptions](pr-bodies/) for the submitted FinanceDataReader body and proposed urllib3/yargs bodies. Development and independent review used OpenAI Codex; no human-only review or upstream acceptance is claimed.

## Apply a patch

The files are standard `git format-patch` output suitable for `git am`. Start from the listed upstream base in a clean checkout and create a working branch:

```sh
# In a FinanceDataReader checkout:
git switch -c fix-yahoo-daily-duplicates addcbb7e887f0db6176a87d323de5de28357b5f4
git am /path/to/archive/patches/fdr-yahoo-duplicate-dates.patch

# In an urllib3 checkout:
git switch -c fix-nan-timeout 796d200d3070ead69ec3a5d848fecf52a2249b59
git am /path/to/archive/patches/urllib3-5294.patch

# In a yargs checkout:
git switch -c docs-strict-dotted-config 10f1dda5991fba2cea6a4b4dc6bd90da6e5292b2
git am /path/to/archive/patches/yargs-strict-dotted-config.patch
```

All three patches were independently applied to pristine local clones at these bases, and the resulting trees matched the prepared changes. Later upstream commits may require rebasing or conflict resolution. Check for newer overlapping contributions before submitting the remaining patches.

## Verify the yargs example

After applying the yargs patch, install that checkout's dependencies and build it using its standard project commands. Then run:

```sh
node /path/to/archive/verification/yargs-doc-verification.mjs /path/to/yargs-checkout
```

The verifier accepts the checkout path as its sole argument. It checks strict-mode behavior, JSON configuration, CLI precedence, unknown-option rejection, and the exact documented JavaScript example. It makes no network requests.
