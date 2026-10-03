# Kyunghan Bae · UNICUP / F&B

F&B 운영 현장에서 필요한 도구를 만들고, 공개 프로젝트의 오류를 재현해 작은 수정과 회귀 테스트로 기여합니다.

I work in F&B operations at [UNICUP Company](https://www.unicupcompany.com) and build practical tools for menu costs, business workflows, and public-data checks.

## Tools I build

| Project | What it helps with |
| --- | --- |
| [F&B Menu Margin Kit](https://github.com/qorud02/fnb-margin-kit) | 메뉴 원가·판매 수량으로 공헌이익을 계산합니다. Decimal calculations, Korean CSV examples, tests, and CI. |
| [Public Data Sentinel](https://github.com/qorud02/public-data-sentinel) | CSV·JSON의 누락 값, 날짜, 숫자 범위, 중복 키를 검사합니다. Explicit contracts, readable reports, tests, and CI. |

## First contributions

작은 초안 PR로 참여할 수 있는 작업입니다. Questions and proposals in Korean or English can go in the linked issue.

- **[TSV input support](https://github.com/qorud02/public-data-sentinel/issues/2)** — 공공 데이터 파일의 탭 구분 형식을 지원하고 문자 식별자를 보존합니다.
- **[Store versus delivery example](https://github.com/qorud02/fnb-margin-kit/issues/2)** — 같은 메뉴의 포장비·수수료 차이를 설명하는 검증 가능한 예제를 만듭니다.

## Merged contributions

- **[USGS dataretrieval-python #431](https://github.com/DOI-USGS/dataretrieval-python/pull/431)** — Reject missing nearest-observation timestamps before querying water data. The maintainer reviewed and extended the validation; merged October 1, 2026.
- **[kiwipiepy #236](https://github.com/bab2min/kiwipiepy/pull/236)** — Make empty Kiwi templates format as an empty string instead of raising `StopIteration`. Includes a regression test; merged October 3, 2026.
- **ForestCI [#128](https://github.com/scikit-learn-contrib/forest-confidence-interval/pull/128), [#130](https://github.com/scikit-learn-contrib/forest-confidence-interval/pull/130), [#132](https://github.com/scikit-learn-contrib/forest-confidence-interval/pull/132)** — Correct training-row bias correction, single-sample memory handling, and supplied sampling counts during calibration. 훈련 행 순서·단일 샘플·보정 단계의 오류를 회귀 테스트로 검증했습니다. Maintainer-reviewed and merged October 3, 2026.

## Pending review

- **[FinanceDataReader #291](https://github.com/FinanceData/FinanceDataReader/pull/291)** — Keep the final Yahoo quote for each daily date so duplicate dates do not break multi-symbol requests.
- [Contribution records](https://github.com/qorud02/qorud02/tree/main/contributions/2026-10-02) — patches and verification notes.

## Interests

F&B operations, useful Python tools, Korean text processing, and reliable public data.
