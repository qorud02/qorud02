# Kyunghan Bae · 배경한

I run F&B brands at [UNICUP COMPANY](https://www.unicupcompany.com), plan projects with companies and public institutions, and build AI tools for day-to-day business work. I provide AI training for small businesses and organizations. I also build Python tools for data validation, CLI testing, and CI evidence, and contribute reproducible fixes to open-source projects.

F&B 브랜드를 운영하며 기업·기관 협업 프로젝트를 기획하고, 업무에 쓰는 AI 도구와 활용 교육을 제공합니다. 데이터 오류와 테스트 결과를 직접 확인할 수 있는 도구도 만듭니다. 한국어·영어로 질문과 제안을 받습니다.

Contact: [ceo@unicupcompany.com](mailto:ceo@unicupcompany.com)

[Career & public work / 경력과 활동](https://profile.unicupcompany.com/) · [AI training for organizations / 기관·기업 AI 교육](https://education.unicupcompany.com/)

## Research and scholarly work / 연구·학술 활동

[ORCID: 0009-0009-7311-4651](https://orcid.org/0009-0009-7311-4651)

**게재 승인 · Accepted article**  
*Operational domain histories and later restaurant inspection citations in New York City* — [NHI Hospitality International Journal](https://journal.poltekpar-nhi.ac.id/index.php/nhij), October 2026.

My research combines foodservice operations with open data, statistical simulation, and reproducible software. Research repositories include source traces, executable analyses, and numerical results.

| Research project | What the repository contains |
| --- | --- |
| [Bootstrap confidence-interval replication](https://github.com/qorud02/bootstrap-ci-replication) · [Preprint](https://doi.org/10.5281/zenodo.23298767) | Seven interval methods, small-sample coverage experiments, and checks against Hesterberg's numerical targets. |
| [Shared-ingredient cafe replenishment](https://github.com/qorud02/cafe-replenishment-simulation) · [Preprint](https://doi.org/10.5281/zenodo.23298824) | Generated-demand experiments comparing three replenishment policies across 54 settings, with separate calibration and evaluation runs. |
| [Robert's truncated-normal algorithms](https://github.com/qorud02/robert1995-truncated-normal-replication) | Independent calculations of 27 printed acceptance probabilities, an algorithm-switching boundary, and Monte Carlo checks. |

**학술 심사 · Peer review** — Completed one manuscript review for NHI Hospitality International Journal, October 2026.

**저서 · Book** — *AI 프랜차이즈 혁명: 기술을 통해 경영을 바꾸다* (퍼플, 2025). [ISBN 9788924174588](https://www.kobic.net/book/bookInfo/view.do?isbn=9788924174588)

## Developer tools

| Tool | Use it when | Run and install |
| --- | --- | --- |
| [JSON Repr Probe](https://github.com/qorud02/json-repr-probe) | Your CLI should return the same JSON result despite key order, whitespace, line endings, or Unicode escapes. Select a result subtree with `--compare-pointer /data` to leave changing metadata out of comparison. | [Examples](https://github.com/qorud02/json-repr-probe/tree/main/examples) · [Wheel 0.2.0](https://github.com/qorud02/json-repr-probe/releases/tag/v0.2.0) · [Container](https://github.com/qorud02/json-repr-probe/pkgs/container/json-repr-probe) |
| [JUnit Evidence Gate](https://github.com/qorud02/junit-evidence-gate) | A green CI report must contain actual testcase records and meet execution and skip limits. Emit GitHub error annotations with `--format github`. | [Examples](https://github.com/qorud02/junit-evidence-gate/tree/main/examples) · [Wheel 0.2.1](https://github.com/qorud02/junit-evidence-gate/releases/tag/v0.2.1) · [Container](https://github.com/qorud02/junit-evidence-gate/pkgs/container/junit-evidence-gate) |
| [Public Data Sentinel](https://github.com/qorud02/public-data-sentinel) | CSV, TSV, or JSON data must satisfy explicit rules before entering a report. Preserve text identifiers such as `00123` and display field names literally in Markdown. | [Examples](https://github.com/qorud02/public-data-sentinel/tree/main/examples) · [Wheel 0.2.1](https://github.com/qorud02/public-data-sentinel/releases/tag/v0.2.1) · [Container](https://github.com/qorud02/public-data-sentinel/pkgs/container/public-data-sentinel) |

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

[Store and delivery comparison](https://github.com/qorud02/fnb-margin-kit/blob/main/docs/store-versus-delivery.md) · [Wheel 0.1.0](https://github.com/qorud02/fnb-margin-kit/releases/tag/v0.1.0) · [Container](https://github.com/qorud02/fnb-margin-kit/pkgs/container/fnb-margin-kit) · [Calculation basis](https://github.com/qorud02/fnb-margin-kit#calculation-basis) · [Tests](https://github.com/qorud02/fnb-margin-kit/actions/workflows/ci.yml)

## Merged upstream fixes

- [mediation #81](https://github.com/kosukeimai/mediation/pull/81): return two-sided analytic TSLS p-values.
- [USGS dataretrieval-python #431](https://github.com/DOI-USGS/dataretrieval-python/pull/431): reject missing nearest-observation timestamps; included in [v1.4.0](https://github.com/DOI-USGS/dataretrieval-python/releases/tag/v1.4.0).
- [scikit-hep-testdata #240](https://github.com/scikit-hep/scikit-hep-testdata/pull/240): isolate the cache failure test from network access and shared state.
- [HDX Python API #114](https://github.com/OCHA-DAP/hdx-python-api/pull/114): correct resource-generation date examples to use explicit keyword arguments.
- [kiwipiepy #236](https://github.com/bab2min/kiwipiepy/pull/236): support empty Kiwi format strings.
- ForestCI [#128](https://github.com/scikit-learn-contrib/forest-confidence-interval/pull/128), [#130](https://github.com/scikit-learn-contrib/forest-confidence-interval/pull/130), [#132](https://github.com/scikit-learn-contrib/forest-confidence-interval/pull/132): correct bias correction, single-sample variance, and calibration with supplied sampling counts.
- [ForestCI #134](https://github.com/scikit-learn-contrib/forest-confidence-interval/pull/134): release unselected class-probability arrays before stacking.

## Contribute

Start with a runnable example or a reproducible bug. The contributor guides explain the tests and review process:

[JSON Repr Probe](https://github.com/qorud02/json-repr-probe/blob/main/CONTRIBUTING.md) · [JUnit Evidence Gate](https://github.com/qorud02/junit-evidence-gate/blob/main/CONTRIBUTING.md) · [Public Data Sentinel](https://github.com/qorud02/public-data-sentinel/blob/main/CONTRIBUTING.md) · [F&B Menu Margin Kit](https://github.com/qorud02/fnb-margin-kit/blob/main/CONTRIBUTING.md)
