# Kyunghan Bae

UNICUP에서 F&B 운영을 하며, 반복되는 데이터 확인과 메뉴 원가 계산을 Python 도구로 만듭니다. 공개 프로젝트에는 오류 재현과 회귀 테스트로 기여합니다.

I work in F&B operations at [UNICUP](https://www.unicupcompany.com). I build Python tools for data checks and menu costs, and contribute reproducible fixes to open-source projects.

## Public Data Sentinel

[Public Data Sentinel](https://github.com/qorud02/public-data-sentinel) checks CSV and JSON against an explicit contract. It preserves text identifiers such as `00123` and reports the record and field that failed. Python 3.10+; no runtime dependencies.

필수 값, 숫자 범위, 날짜, 중복 키를 검사합니다. [예제 결과](https://github.com/qorud02/public-data-sentinel/blob/main/examples/valid-report.json)와 [Windows·Linux 검사](https://github.com/qorud02/public-data-sentinel/actions/workflows/tests.yml)를 확인할 수 있습니다.

```sh
git clone https://github.com/qorud02/public-data-sentinel.git
cd public-data-sentinel
python -m pip install -e .
data-sentinel examples/valid.csv --contract examples/contract.json
```

The example checks three records and returns exit code 0.

**첫 기여 / First contribution:** [TSV input support #2](https://github.com/qorud02/public-data-sentinel/issues/2). Read the [Korean/English contributor guide](https://github.com/qorud02/public-data-sentinel/blob/main/CONTRIBUTING.md), discuss your scope in the issue, and send a small draft PR with tests. 질문과 제안은 한국어·영어 모두 가능합니다.

## F&B Menu Margin Kit

[F&B Menu Margin Kit](https://github.com/qorud02/fnb-margin-kit) calculates menu contribution using Decimal arithmetic. 메뉴별 원가·판매 수량으로 공헌이익을 계산합니다. [매장·배달 비교 예제 #2](https://github.com/qorud02/fnb-margin-kit/issues/2)에 참여할 수 있습니다.

## Merged fixes

- [USGS dataretrieval-python #431](https://github.com/DOI-USGS/dataretrieval-python/pull/431) — reject missing nearest-observation timestamps.
- [kiwipiepy #236](https://github.com/bab2min/kiwipiepy/pull/236) — support empty Kiwi format strings.
- ForestCI [#128](https://github.com/scikit-learn-contrib/forest-confidence-interval/pull/128), [#130](https://github.com/scikit-learn-contrib/forest-confidence-interval/pull/130), [#132](https://github.com/scikit-learn-contrib/forest-confidence-interval/pull/132) — correct bias correction, single-sample variance, and calibration with supplied sampling counts.
