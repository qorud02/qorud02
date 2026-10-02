import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { pathToFileURL } from "node:url";

if (process.argv.length !== 3) {
  console.error(
    "Usage: node yargs-doc-verification.mjs /path/to/yargs-checkout",
  );
  process.exit(2);
}

const repo = path.resolve(process.argv[2]);
const entry = path.join(repo, "index.mjs");
assert.ok(fs.existsSync(entry), `Missing yargs entry point: ${entry}`);
const { default: yargs } = await import(pathToFileURL(entry).href);
const version = JSON.parse(
  fs.readFileSync(path.join(repo, "package.json"), "utf8"),
).version;

const nested = { auth: { username: "test", password: "example-password" } };
const dotted = {
  "auth.username": "test",
  "auth.password": "example-password",
};
const createParser = (args) =>
  yargs(args)
    .option("auth.username", { type: "string" })
    .option("auth.password", { type: "string" })
    .exitProcess(false)
    .showHelpOnFail(false);

function parse(parser, args = []) {
  let result;
  parser.parse(args, (error, argv) => {
    result = { error, argv };
  });
  assert.ok(result, "synchronous parse callback must run");
  return result;
}

for (const mode of ["strict", "strictOptions"]) {
  for (const config of [nested, dotted]) {
    const result = parse(createParser([]).config(config)[mode]());
    assert.equal(result.error?.message, "Unknown argument: auth");
  }
  const flatParser = (args) =>
    createParser(args)
      .parserConfiguration({ "dot-notation": false })
      .config(dotted)
      [mode]();
  const result = parse(flatParser([]));
  assert.equal(result.error, null);
  assert.equal(result.argv["auth.username"], "test");
  assert.equal(result.argv["auth.password"], "example-password");
  assert.equal(result.argv.auth, undefined);
  const overrideArgs = ["--auth.username", "override"];
  const override = parse(flatParser(overrideArgs), overrideArgs);
  assert.equal(override.error, null);
  assert.equal(override.argv["auth.username"], "override");
  assert.equal(override.argv["auth.password"], "example-password");
  const unknownArgs = ["--auth.extra", "bad"];
  const unknown = parse(flatParser(unknownArgs), unknownArgs);
  assert.equal(unknown.error?.message, "Unknown argument: auth.extra");
  console.log(
    `${mode}: default dot-notation rejected; flat config accepted; CLI override and unknown-option validation verified`,
  );
}

const dir = fs.mkdtempSync(path.join(os.tmpdir(), "yargs-config-docs-"));
try {
  const filename = path.join(dir, "config.json");
  fs.writeFileSync(filename, JSON.stringify(dotted));
  const args = ["--config", filename];
  const result = parse(
    createParser(args)
      .parserConfiguration({ "dot-notation": false })
      .config()
      .strict(),
    args,
  );
  assert.equal(result.error, null);
  assert.equal(result.argv["auth.username"], "test");
  assert.equal(result.argv["auth.password"], "example-password");
  console.log(
    "JSON config file: literal dotted keys accepted with dot-notation disabled",
  );
} finally {
  fs.rmSync(dir, { recursive: true, force: true });
}

const docs = fs.readFileSync(path.join(repo, "docs/api.md"), "utf8");
const match = docs.match(
  /### Dotted option names with strict mode[\s\S]*?```js\n([\s\S]*?)\n```/,
);
assert.ok(match, "Patched documentation example must be present");
const child = spawnSync(process.execPath, ["--input-type=module"], {
  cwd: repo,
  input: match[1].replace("from 'yargs'", "from './index.mjs'"),
  encoding: "utf8",
});
assert.ifError(child.error);
assert.equal(child.status, 0, child.stderr);
assert.equal(child.stdout, "test\n");
console.log("Exact documented JavaScript example: printed test as documented");
console.log(
  `All documentation verification checks passed on yargs ${version} and ${process.version}`,
);
