# Kyunghan Bae

I build small Python tools for data validation, CLI testing, and CI evidence. I work in F&B operations at [UNICUP](https://www.unicupcompany.com) and contribute reproducible fixes to open-source projects.

데이터 오류와 테스트 결과를 직접 확인할 수 있는 도구를 만듭니다. 한국어·영어로 질문과 제안을 받습니다.

Contact: [ceo@unicupcompany.com](mailto:ceo@unicupcompany.com)

## Developer tools

| Tool | Use it when | Run and install |
| --- | --- | --- |
| [JSON Repr Probe](https://github.com/qorud02/json-repr-probe) | Your CLI should return the same JSON result despite key order, whitespace, line endings, or Unicode escapes. Select a result subtree with `--compare-pointer /data` to leave changing metadata out of comparison. | [Examples](https://github.com/qorud02/json-repr-probe/tree/main/examples) · [Wheel 0.2.0](https://github.com/qorud02/json-repr-probe/releases/tag/v0.2.0) · [Container](https://github.com/qorud02/json-repr-probe/pkgs/container/json-repr-probe) |
| [JUnit Evidence Gate](https://github.com/qorud02/junit-evidence-gate) | A green CI report must contain actual testcase records and meet execution and skip limits. Emit GitHub error annotations with `--format github`. | [Examples](https://github.com/qorud02/junit-evidence-gate/tree/main/examples) · [Wheel 0.2.0](https://github.com/qorud02/junit-evidence-gate/releases/tag/v0.2.0) · [Container](https://github.com/qorud02/junit-evidence-gate/pkgs/container/junit-evidence-gate) |
| [Public Data Sentinel](https://github.com/qorud02/public-data-sentinel) | CSV, TSV, or JSON data must satisfy explicit rules before entering a report. Preserve text identifiers such as `00123` and display field names literally in Markdown. | [Examples](https://github.com/qorud02/public-data-sentinel/tree/main/examples) · [Wheel 0.2.0](https://github.com/qorud02/public-data-sentinel/releases/tag/v0.2.0) · [Container](https://github.com/qorud02/public-data-sentinel/pkgs/container/public-data-sentinel) |

These tools run offline with Python 3.10+ and have no runtime dependencies. Each repository includes installation instructions, runnable examples, and Windows/Linux CI.

### Try a representation bug

~~~sh
git clone https://github.com/qorud02/json-repr-probe.git
cd json-repr-probe
python -m json_repr_probe --input examples/input.json -- python -m examples.stable_cli
~~~

The stable CLI passes. Replace `examples.stable_cli` with `examples.order_sensitive_cli` to reproduce a key-order bug and see the first changed JSON Pointer.

### [F&B Menu Margin Kit](https://github.com/qorud02/fnb-margin-kit)

Calculate menu contribution after ingredients, packaging, and platform fees using Decimal arithmetic. It handles Korean CSV exports, VAT, negative margins, and optional fixed-cost scenarios.

[Sample data](https://github.com/qorud02/fnb-margin-kit/blob/main/examples/menu.csv) · [Calculation basis](https://github.com/qorud02/fnb-margin-kit#calculation-basis) · [Tests](https://github.com/qorud02/fnb-margin-kit/actions/workflows/ci.yml)

## Merged upstream fixes

- [USGS dataretrieval-python #431](https://github.com/DOI-USGS/dataretrieval-python/pull/431): reject missing nearest-observation timestamps.
- [kiwipiepy #236](https://github.com/bab2min/kiwipiepy/pull/236): support empty Kiwi format strings.
- ForestCI [#128](https://github.com/scikit-learn-contrib/forest-confidence-interval/pull/128), [#130](https://github.com/scikit-learn-contrib/forest-confidence-interval/pull/130), [#132](https://github.com/scikit-learn-contrib/forest-confidence-interval/pull/132): correct bias correction, single-sample variance, and calibration with supplied sampling counts.

## Contribute

Start with a runnable example or a reproducible bug. The contributor guides explain the tests and review process:

[JSON Repr Probe](https://github.com/qorud02/json-repr-probe/blob/main/CONTRIBUTING.md) · [JUnit Evidence Gate](https://github.com/qorud02/junit-evidence-gate/blob/main/CONTRIBUTING.md) · [Public Data Sentinel](https://github.com/qorud02/public-data-sentinel/blob/main/CONTRIBUTING.md) · [F&B Menu Margin Kit](https://github.com/qorud02/fnb-margin-kit/blob/main/CONTRIBUTING.md)
