# Verification record

Checks below were executed locally on 2026-10-02. Passing targeted checks do not establish full cross-platform CI success. FinanceDataReader was submitted as [PR #291](https://github.com/FinanceData/FinanceDataReader/pull/291); urllib3 and yargs remain unsubmitted. No patch is claimed as merged.

## Patch identity and application

| Project | Upstream base | Prepared local commit | Resulting tree |
| --- | --- | --- | --- |
| FinanceDataReader | `addcbb7e887f0db6176a87d323de5de28357b5f4` | `a0012f9f292258f6183d78411dcb8d78b56edfde` | `9b770db49cd9bbcba8fce2ad5d91ffcd15b1d8b6` |
| urllib3 | `796d200d3070ead69ec3a5d848fecf52a2249b59` | `95adb5b644604342df629577db5089403574ca5c` | `546f21c46a3b7cedd41e4fee1aaa0453ad358365` |
| yargs | `10f1dda5991fba2cea6a4b4dc6bd90da6e5292b2` | `6d573405d626a52994d388f67518282643563e55` | `ef28d0b7de1bd4a20b46aeacd5670ce80f6d3b11` |

Each archive patch was applied with `git am` to a temporary pristine clone checked out at its listed base. All three applied successfully; their resulting Git trees exactly matched the prepared local commits. `git diff --check HEAD~1 HEAD` passed in all three temporary clones. The patches preserve the public GitHub noreply author identity from their local commits.

FinanceDataReader's public PR head is `7151b6a5ba93a9edabd237927985d54645cd41f6`, with the same tree as the archived local patch commit. PR #291 was open and unmerged when checked on 2026-10-02.

## FinanceDataReader: duplicate Yahoo daily dates

Runtime: Python 3.12 on Linux; pandas 3.0.6.

- Unchanged upstream source: **4 failed, 1 passed** in the added offline regression module. The multi-symbol regression reproduced pandas `InvalidIndexError`; the unique-date control passed.
- Patched source: `python -m pytest tests/test_yahoo_duplicate_dates.py -q -W error --tb=short`: **5 passed**.
- Tests cover distinct and identical raw timestamps for a duplicated daily date, single-symbol output, multi-symbol alignment, unique-date preservation, and request boundaries including a single-day request.
- `git diff --check` passed.

The fixtures use Yahoo-shaped API responses and differing Nasdaq values reported in [issue #272](https://github.com/FinanceData/FinanceDataReader/issues/272). They are deterministic reproductions, not today's live quotes. Live Yahoo responses checked during the session did not contain duplicate dates. Existing tests that depend on live market services were not run. No full market-service test suite or upstream CI success is claimed.

## urllib3: NaN timeout validation

Runtime: Python 3.12.14 on Linux.

- Regression proof against untouched upstream source: **4 failed, 601 deselected**, all because NaN did not raise `ValueError`.
- Complete `test/test_util.py` on the patch: **599 passed, 6 skipped**.
- Related utility, connection, connection-pool, pool-manager, proxy-manager, and retry unit modules on the final formatted source: **1193 passed, 6 skipped**.
- Independent review run covering NaN, existing invalid inputs, and default resolution: **13 passed, 592 deselected**, with sockets disabled. This run is a subset of the preceding suite, not 13 additional unique tests.
- Independent comparison of 24 sampled inputs found no regression for documented int/float/None inputs. NaN now rejects early; positive infinity, None, and the default sentinel retain their prior behavior. Decimal NaN now raises `ValueError` instead of `decimal.InvalidOperation`; Decimal is outside the documented input types.
- Repository Python/configuration hooks passed: pyupgrade, Black, isort, Flake8, uv-lock, and zizmor. These used the exact repository hooks with only the two JavaScript hooks omitted from a temporary configuration.
- `git diff --check` passed.

Reproduction command for the related unit modules, after preparing a project test environment:

```sh
python -m pytest test/test_util.py test/test_connection.py test/test_connectionpool.py test/test_poolmanager.py test/test_proxymanager.py test/test_retry.py -q --timeout=15 --disable-socket --allow-unix-socket --allow-hosts=localhost,127.0.0.1,::1,127.0.0.0,240.0.0.0
```

Limitations:

- The full `nox -rs test-3.12` run collected 2810 items with 1 skipped and was interrupted during `TestHTTPS_TLSv1_2.test_http2_probe_blocked_per_thread`. Its interrupted summary was **2 failed, 134 passed, 132 skipped, 1 xfailed**. The two failures were `test_https_timeout` and `test_enhanced_timeout`, whose route checks to `240.0.0.0:80` raised `ConnectionRefusedError`. The same two failures were reproduced on pristine upstream main. The probe test passed in isolation on pristine main, so a baseline hang has not been established.
- Full `nox -rs lint` was blocked while installing the JavaScript-only Prettier hook: npm 11.9.0 rejected a local-git placeholder dependency with `EALLOWGIT`. Prettier and ESLint hooks did not complete; the six Python/configuration hooks listed above did pass separately.
- Full `nox -rs mypy` reported one `ClassVar[Final[...]]` qualifier error at `connection.py:150`. The same error was reproduced on pristine main with the same mypy environment. No new reported type error was found.
- No complete multi-platform test matrix or upstream CI result is claimed.

## yargs: strict dotted configuration documentation

Runtime: Node.js v24.19.0; yargs 18.2.0 at the listed upstream base with the documentation patch.

- `npm test -- --grep 'strict|config|parserConfiguration'`: **96 tests passed**, including the project's compilation and lint checks.
- `npx prettier --check docs/api.md`: passed.
- `git diff --check`: passed.
- The documented JavaScript example was executed and printed `test` followed by a newline, as documented.
- Verification covers default dot-notation rejection of nested and dotted config objects, successful flat config parsing with dot-notation disabled, CLI overrides, unknown dotted options, `.strict()`, `.strictOptions()`, and a JSON config file.
- The portable [verification script](yargs-doc-verification.mjs) was independently run from outside the repository, taking its checkout path as an argument. All checks passed on Node.js v24.19.0 and yargs 18.2.0. It reads the actual documentation example from the patched checkout and executes that example.

The yargs patch is documentation only. It explains existing parser behavior and a workaround; it does not fix the parser or establish that either related issue is fully resolved. The full unfiltered project test suite and a cross-platform matrix were not run for this change.

## Scope and disclosure

OpenAI Codex assisted with development, descriptions, and independent review. Commands described as executed were run locally. This record contains no raw authentication output, private credentials, or copied raw logs. STFC work was audited but independently updated remotely during the session and is not included as an authored result in this archive.
