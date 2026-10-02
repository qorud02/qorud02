# ETLHelper #232 local contribution

Repository: https://github.com/BritishGeologicalSurvey/etlhelper
Base: 8a2b413585d892443037679acf4559d4e4d2583e
Issue: https://github.com/BritishGeologicalSurvey/etlhelper/issues/232
Suggested title: Add a runnable branching pipeline recipe
PR body: ../pr-bodies/etlhelper-232.md

## Authorization and scope

Issue #232 was opened by collaborator volcan01010 on 2026-08-06. It asks for a branching-pipeline recipe based on the bird quality-check prototype and tests including empty results in one branch. CONTRIBUTING.md explicitly welcomes additional recipes/case studies and improved documentation. No AGENTS.md or AI prohibition was found. All-state issue-number and branching PR searches found no duplicate. Existing docs PR #234 concerns SQL error handling; this patch touches only the recipe area and a new offline test module.

The current engine already supports this feature: iter_chunks applies a transform generator, and load treats empty lists as a no-op. Main contains no branching recipe. This is a requested new runnable example, not an engine bug fix, so we do not claim a pre-fix behavioral regression.

## Implementation

Four intended files:

- docs/recipes.rst: add one toctree entry.
- docs/recipes/branching_pipeline.rst: explain tuple outputs, None for absent branch output, chunk memory bounds, empty branch/input behavior, separate connections and per-load commits.
- docs/code_demos/recipes/branching_pipeline.py: actual runnable birds example using two in-memory SQLite connections; size checks for all birds and a swimming branch that filters non-swimming birds.
- test/test_branching_pipeline_recipe.py: tests execute the actual documentation module against real in-memory SQLite databases using existing ETL functions.

Each returned transform chunk is split into two lists. Empty swim output is handed to etl.load normally rather than skipping the whole source chunk. This avoids zip(*chunk) failure on empty transformed chunks. ORDER BY id makes sample order deterministic. Connections close via contextlib.closing. Both destination branches use the same destination connection in the example; readers can replace each with another connection.

No engine behavior, database helper, SQL error-handling documentation, or repository config changes.

## Validation

- .venv/bin/python -m pytest --noconftest test/test_branching_pipeline_recipe.py -q
  Result: 6 passed in 0.08s. Cases: chunk sizes 1, 2, 5; entirely empty swim branch; empty source; runnable __main__ output. Raw test logs are not included in this archive.

- .venv/bin/flake8 docs/code_demos/recipes/branching_pipeline.py test/test_branching_pipeline_recipe.py
  Passed with repository .flake8 configuration and flake8-annotations installed. These paths follow existing test/docs annotation exemptions.

- .venv/bin/python docs/code_demos/recipes/branching_pipeline.py
  Passed. Output has four size-check rows and two swimming-bird rows. Creates no files and uses no network.

- .venv/bin/sphinx-build -b html -W --keep-going -D html_static_path= docs /path/to/temporary-docs-build
  Passed. The CLI override avoids the existing missing _static warning, as in PR #234; configuration is unchanged. Raw build logs are not included in this archive. Verified generated recipes.html links to recipes/branching_pipeline.html and the new page includes literal source, execution command and empty-branch explanation.

- git diff --check passed. No live PostgreSQL/Oracle/MS SQL integrations were run; they are unrelated to this SQLite-only recipe. The implementation agent made no remote writes; the root agent subsequently published the prepared branch. Upstream PR creation failed with HTTP 403.

Archive note: local workspace paths and raw-log references above were normalized for portability; the validation results and caveats are unchanged.
