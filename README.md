# Kyunghan Bae

UNICUP에서 F&B 운영을 하며, 반복되는 데이터 확인과 메뉴 원가 계산을 Python 도구로 만듭니다. 공개 프로젝트에는 오류 재현과 회귀 테스트로 기여합니다.

I work in F&B operations at [UNICUP](https://www.unicupcompany.com). I build Python tools for menu costs and data checks, and contribute reproducible fixes to open-source projects.

## Selected projects

### [F&B Menu Margin Kit](https://github.com/qorud02/fnb-margin-kit)

**메뉴 원가와 판매 구성을 공헌이익으로 연결하는 Python CLI.** Ranks menu contribution after ingredients, packaging, and platform fees using Decimal arithmetic.

- Handles Korean CSV exports, VAT, negative margins, and optional fixed-cost scenarios
- The four-menu example totals **190 units and 512,000.00 contribution before fixed costs**. These are illustrative inputs, not operating results or net profit
- [Sample CSV](https://github.com/qorud02/fnb-margin-kit/blob/main/examples/menu.csv) · [Calculation basis & quick start](https://github.com/qorud02/fnb-margin-kit#calculation-basis) · [Tests: Python 3.10 / 3.12 / 3.14](https://github.com/qorud02/fnb-margin-kit/actions/workflows/ci.yml)

### [Public Data Sentinel](https://github.com/qorud02/public-data-sentinel)

**분석·보고서에 넣기 전 CSV·JSON의 오류를 찾는 Python CLI.** Validates files against an explicit contract and reports the failing record and field.

- Checks required values, numeric bounds, dates, and duplicate keys; preserves identifiers such as `00123`
- The invalid-data example finds **5 issues in 3 records**. Fixtures are synthetic; passing a contract does not establish factual accuracy
- [Passing JSON report](https://github.com/qorud02/public-data-sentinel/blob/main/examples/valid-report.json) · [Failing Markdown report](https://github.com/qorud02/public-data-sentinel/blob/main/examples/invalid-report.md) · [Windows & Linux tests](https://github.com/qorud02/public-data-sentinel/actions/workflows/tests.yml)

Both tools require Python 3.10+ and have no runtime dependencies. Installation and examples are in each repository.

## Merged upstream fixes

Five fixes accepted into three external projects:

- [USGS dataretrieval-python #431](https://github.com/DOI-USGS/dataretrieval-python/pull/431) — reject missing nearest-observation timestamps
- [kiwipiepy #236](https://github.com/bab2min/kiwipiepy/pull/236) — support empty Kiwi format strings
- ForestCI [#128](https://github.com/scikit-learn-contrib/forest-confidence-interval/pull/128), [#130](https://github.com/scikit-learn-contrib/forest-confidence-interval/pull/130), [#132](https://github.com/scikit-learn-contrib/forest-confidence-interval/pull/132) — correct bias correction, single-sample variance, and calibration with supplied sampling counts

## Contribute

- Public Data Sentinel: [TSV input support #2](https://github.com/qorud02/public-data-sentinel/issues/2) · [Contributor guide](https://github.com/qorud02/public-data-sentinel/blob/main/CONTRIBUTING.md)
- F&B Menu Margin Kit: [매장·배달 비교 예제 #2](https://github.com/qorud02/fnb-margin-kit/issues/2) · [Contributor guide](https://github.com/qorud02/fnb-margin-kit/blob/main/CONTRIBUTING.md)

질문과 제안은 한국어·영어 모두 가능합니다. Discuss the scope in the issue, then send a small draft PR with reproducible examples and tests.
