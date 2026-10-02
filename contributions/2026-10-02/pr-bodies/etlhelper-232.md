# Proposed PR: Add a runnable branching pipeline recipe

Status: tested and published to [qorud02/etlhelper:docs-branching-pipeline-recipe](https://github.com/qorud02/etlhelper/tree/docs-branching-pipeline-recipe). No upstream PR was created: both REST/connector and GraphQL attempts returned HTTP 403.

The recipe book currently has no example of sending one extraction into multiple output tables. Add a runnable SQLite bird-check pipeline based on the proposal in #232: the transform yields paired output rows, and the pipeline collects and loads each branch for the current chunk.

One branch includes every bird's size check; the other includes swimming birds. `None` marks an omitted branch row. The first sample chunk has no swimming output, and later chunks still populate that branch. The page explains empty input, bounded chunk processing, separate destination connections, and the default per-load commits. No ETL engine code changes are needed.

Validation on Python 3.12.14:

- `python -m pytest --noconftest test/test_branching_pipeline_recipe.py -q`: 6 passed, covering three chunk sizes, an entirely empty branch, empty source, and the executable script.
- The standalone script prints four size checks and two swimming-bird records.
- Both Python files pass flake8 with the repository configuration; `git diff --check` passes.
- The Sphinx HTML build succeeds with warnings treated as errors using `-D html_static_path=` to avoid the existing missing `_static` directory warning. The rendered recipe is linked from the recipe book.

`--noconftest` avoids the repository-wide PostgreSQL fixture import; these tests exercise the real ETL functions with in-memory SQLite only. Live database integration tests were not run.

Closes #232.

Prepared with AI assistance; the recipe and its empty-output cases were executed locally.
