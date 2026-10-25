# Source input manifests

source_manifest.json pins original source code and 75 session metadata files.
outcome_manifest.json declares the archive's outcome files.

For the current report, only the 20 eligible primary sessions' three outcome
files were downloaded, plus 83 source/metadata files: 143 files in total,
6,325,873 bytes, with original Git blob hashes verified. The remaining 55
sessions' 165 outcome files were not downloaded or analyzed.

The data/upstream/ directory is a local read-only source cache. Do not include
it in the public package: the upstream repository has no explicit license file.
Reproduction downloads the pinned originals from their original GitHub host.
