# Proposed PR: Reject NaN timeout values during construction

Status: prepared locally; not submitted or merged upstream.

A NaN connect, read, or total timeout currently passes `Timeout` validation. For a connect timeout, the invalid value reaches `socket.settimeout()` and raises a later `ValueError`. Reject NaN during construction with an error that names the affected timeout field.

Added regression coverage for all three constructor fields and `Timeout.from_float()`, plus a changelog entry. The four new cases fail against unchanged upstream main and pass with the fix.

Validation on Python 3.12.14:

- Related utility, connection, pool, proxy, and retry unit tests: 1193 passed, 6 skipped.
- Python formatting/lint hooks, lock validation, and zizmor: passed.
- The full suite was attempted but interrupted after two network-route failures and a blocked HTTP/2 probe test. Both network failures also occur on unchanged main. The isolated probe test passes on unchanged main, so a baseline hang has not been established.
- Full mypy reports the same existing `ClassVar[Final[...]]` error in `connection.py:150` on main and this branch. The full lint session cannot install its JavaScript-only Prettier hook with this environment's npm; JavaScript hooks were not completed.

Fixes [#5294](https://github.com/urllib3/urllib3/issues/5294).

AI assistance: OpenAI Codex helped prepare and independently review the patch; the reproducer and validation above were executed locally.
