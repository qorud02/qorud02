# Kyunghan Bae

Contact: [ceo@unicupcompany.com](mailto:ceo@unicupcompany.com)

UNICUP에서 F&B 운영을 맡으며, Python으로 데이터 검사·계산·오류 재현 도구를 만듭니다. 공개 프로젝트에는 재현 예제와 회귀 테스트를 갖춘 수정으로 기여합니다.

I work in F&B operations at [UNICUP](https://www.unicupcompany.com). I build Python tools for menu costs and data checks, and contribute reproducible fixes to open-source projects.

## Selected projects

### [JUnit Evidence Gate](https://github.com/qorud02/junit-evidence-gate)

**JUnit 보고서의 테스트 수·중복·건너뜀을 검사하는 Python CLI.** Checks testcase records before a CI report is accepted: empty execution, contradictory totals, duplicate identities and skip budgets.

- Counts nested suites once and applies a minimum execution count and optional skip limits
- Rejects unsafe XML and displays report names literally in JSON or Markdown
- [Seven runnable fixtures](https://github.com/qorud02/junit-evidence-gate/tree/main/examples) · [62 tests, installation and CLI checks on Windows & Linux](https://github.com/qorud02/junit-evidence-gate/actions/runs/37130700719)

~~~sh
git clone https://github.com/qorud02/junit-evidence-gate.git
cd junit-evidence-gate
python -m junit_evidence_gate examples/contradictory.xml --format markdown
~~~

### [JSON Repr Probe](https://github.com/qorud02/json-repr-probe)

**같은 JSON 값의 표현을 바꿔 CLI의 결과 차이를 찾는 테스트 도구.** Detects bugs caused by object key order, whitespace, line endings and Unicode escapes.

- Reports the first changed field as a JSON Pointer and compares numbers with decimal precision
- Runs a stable baseline twice, then applies deterministic presentations to your command
- [Passing example](https://github.com/qorud02/json-repr-probe/blob/main/examples/passing-report.json) · [Bug example](https://github.com/qorud02/json-repr-probe/blob/main/examples/failing-report.json) · [Windows & Linux tests](https://github.com/qorud02/json-repr-probe/actions/workflows/tests.yml)

~~~sh
git clone https://github.com/qorud02/json-repr-probe.git
cd json-repr-probe
python -m json_repr_probe --input examples/input.json -- python -m examples.stable_cli
~~~

### [F&B Menu Margin Kit](https://github.com/qorud02/fnb-margin-kit)

**메뉴 원가와 판매 구성을 공헌이익으로 연결하는 Python CLI.** Ranks menu contribution after ingredients, packaging, and platform fees using Decimal arithmetic.

- Handles Korean CSV exports, VAT, negative margins, and optional fixed-cost scenarios
- A synthetic four-menu example totals **190 units and 512,000.00 contribution before fixed costs**
- [Sample CSV](https://github.com/qorud02/fnb-margin-kit/blob/main/examples/menu.csv) · [Calculation basis & quick start](https://github.com/qorud02/fnb-margin-kit#calculation-basis) · [Tests: Python 3.10 / 3.12 / 3.14](https://github.com/qorud02/fnb-margin-kit/actions/workflows/ci.yml)

### [Public Data Sentinel](https://github.com/qorud02/public-data-sentinel)

**분석·보고서에 넣기 전 CSV·JSON의 오류를 찾는 Python CLI.** Validates files against an explicit contract and reports the failing record and field.

- Checks required values, numeric bounds, dates, and duplicate keys; preserves identifiers such as `00123`
- A synthetic invalid-data example finds **5 issues in 3 records**
- [Passing JSON report](https://github.com/qorud02/public-data-sentinel/blob/main/examples/valid-report.json) · [Failing Markdown report](https://github.com/qorud02/public-data-sentinel/blob/main/examples/invalid-report.md) · [Windows & Linux tests](https://github.com/qorud02/public-data-sentinel/actions/workflows/tests.yml)

All four tools require Python 3.10+ and have no runtime dependencies. Installation and examples are in each repository.

## Merged upstream fixes

Five fixes accepted into three external projects:

- [USGS dataretrieval-python #431](https://github.com/DOI-USGS/dataretrieval-python/pull/431) — reject missing nearest-observation timestamps
- [kiwipiepy #236](https://github.com/bab2min/kiwipiepy/pull/236) — support empty Kiwi format strings
- ForestCI [#128](https://github.com/scikit-learn-contrib/forest-confidence-interval/pull/128), [#130](https://github.com/scikit-learn-contrib/forest-confidence-interval/pull/130), [#132](https://github.com/scikit-learn-contrib/forest-confidence-interval/pull/132) — correct bias correction, single-sample variance, and calibration with supplied sampling counts

## Contribute

- JUnit Evidence Gate: [Contributor guide](https://github.com/qorud02/junit-evidence-gate/blob/main/CONTRIBUTING.md)
- JSON Repr Probe: [Contributor guide](https://github.com/qorud02/json-repr-probe/blob/main/CONTRIBUTING.md)
- Public Data Sentinel: [TSV input support #2](https://github.com/qorud02/public-data-sentinel/issues/2) · [Contributor guide](https://github.com/qorud02/public-data-sentinel/blob/main/CONTRIBUTING.md)
- F&B Menu Margin Kit: [매장·배달 비교 예제 #2](https://github.com/qorud02/fnb-margin-kit/issues/2) · [Contributor guide](https://github.com/qorud02/fnb-margin-kit/blob/main/CONTRIBUTING.md)

질문과 제안은 한국어·영어 모두 가능합니다. Discuss the scope in the issue, then send a small draft PR with reproducible examples and tests.
