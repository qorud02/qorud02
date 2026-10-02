# Proposed PR: docs: explain dotted config keys with strict mode

Status: prepared locally; not submitted or merged upstream.

Options such as `auth.username` can fail strict validation with `Unknown argument: auth`, including when they come from a JSON configuration. Document the working combination of literal dotted config keys and `dot-notation: false`, with an executable example and an explicit explanation that the parsed keys remain flat.

Related to [#2472](https://github.com/yargs/yargs/issues/2472) and [#1811](https://github.com/yargs/yargs/issues/1811). This documents a workaround; it does not change parser behavior.

Validation on Node.js 24.19.0 and yargs 18.2.0:

- Ran the documented JavaScript example and checked its output.
- Verified config objects and JSON files, CLI overrides, and rejection of unknown dotted options. Confirmed both `.strict()` and `.strictOptions()` behavior.
- `npm test -- --grep 'strict|config|parserConfiguration'`: 96 tests passed, with the project's compilation and lint checks.
- `npx prettier --check docs/api.md` and `git diff --check` passed.
- The portable archive verifier was independently run against the prepared checkout and passed.

Prepared and independently verified with OpenAI Codex assistance. Maintainer review is pending.
