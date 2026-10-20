# Tool recovery under fixed budgets: replication materials

This repository accompanies the 20 October 2026 revised manuscript on conditional read/write ceilings, commitment stage, operation contracts and feedback presentation in tool-failure recovery. It contains analysis data, frozen protocols, statistical and plotting code, and selected retained-state witnesses. The manuscript itself is not distributed here.

Release: **v1.0.0**. Cite the release together with its full Git commit SHA; see `CITATION.md`.

## Quick start

Use Python 3.12 and a fresh virtual environment:

```sh
python -m venv .venv
# Activate .venv using the command appropriate to your shell.
python -m pip install -r requirements-lock.txt
python reproduce.py --check
python reproduce.py --statistics
python reproduce.py --figures
python reproduce.py --witnesses
```

The four flags can be combined. Statistical checks retain the original 20,000 bootstrap draws and can take several minutes. No model account, API key, model download, GPU, or paid call is needed. Verification subprocesses have Python socket creation disabled. Dependency installation is the only network step.

`--check` verifies every bundle part, the complete manifest, each decoded material, and the claim mapping. On first use the public packaging key decodes the materials into `.materials/`. This directory and `outputs/` are excluded from Git. Scripts run on disposable copies; frozen decoded inputs are checked again afterwards. Reports and the 21 required figure PDFs are saved in `outputs/`.

The materials are encrypted using the AppWorld-compatible bundle format to preserve the upstream redistribution condition for protected benchmark-derived content. The decoding key is intentionally public and supplied in `bundle_codec.py`; it is an anti-scraping packaging measure, not a private access approval process. The bundle is split into numbered files for normal GitHub downloads. Keep every part. Do not republish decoded protected materials as plaintext.

## What can be reproduced

| Evidence | Released inputs and verification |
| --- | --- |
| S7-S10/C2 historical evidence | Retained result, protocol and inclusion/exclusion exports where present. These are explicitly frozen exports, not a claim that every early raw trajectory or original native environment can be replayed here. |
| S11 | Paired object vectors; 16 primary and 64 additional point estimates and 80 frozen interval pairs. Native states are not rescored for all S11 episodes. |
| S12 | 1,728 compact outcomes; all 40 comparisons with the original sign-flip tests and Holm40 correction, plus descriptive interactions. |
| S13 | 2,688 compact trajectories; all five frozen primary records including bootstrap intervals and Holm5, descriptive cells and 2,016 rule conditions. |
| S14 | 1,568 compact scores; both primary comparisons with Holm2; all 36 resource cells; selected cart business-state and event replay. |
| S15 | All 3,024 formal trajectory summaries and 48 reused worlds; all four original interactions, bootstrap intervals, Holm4, and 189 condition-by-operation cells. |
| Selected native witnesses | The earlier 238-witness package, S13's preselected 672 trajectories, and S14's 28 matched cart trajectories. These are retained-state reconstructions, not live executions of the complete benchmark. |
| Figures | Frozen numerical inputs and code for the 11 main and 10 supplementary figures, with frame/legend checks retained. |

S14 and S15 reuse worlds. Repeats, conditions, checkpoints and model endpoints do not create independent objects. All supported and unsupported comparisons remain in their original families. S15's four corrected p-values remain 1; this package does not introduce a new hypothesis family or new model observations.

## Contents

- `reproduce.py`, `scripts/`: public offline entry points.
- `materials/`, `BUNDLE.json`: encrypted materials and part checksums.
- `MATERIALS_MANIFEST.json`: file inventory, sizes and SHA-256 digests.
- Inside the decoded materials: `legacy/` contains S10-S13 materials; `current/` contains current plot inputs, S14/S15 data and resource tables; `historical/` retains earlier outputs; `protocols/` contains frozen design documents; `witness_r2/` contains earlier selected witnesses.
- `CLAIMS.json` inside the bundle maps all 25 manuscript claims to actual files; `FIGURE_MAP.json` maps the 21 figures. The original claim map is retained for provenance.
- `EXPORT_PROVENANCE.json` records original file locations relative to the research project, hashes and adaptations. Historical document dates are provenance, not public preregistration.
- `DATA_DICTIONARY.md`, `THIRD_PARTY.md`, `LICENSES/`: definitions and reuse conditions.

The release excludes paper PDFs/TeX, internal review reports, account credentials, transport headers, private billing ledgers and complete benchmark databases. Existing redacted simulation authentication is documented in the witness provenance. A compact score or selected witness must not be described as a complete raw provider-response deposit.

## Full environment replication

Obtain τ-bench revision `59a200c6d575d595120f1cb70fea53cef0632f6b` from [sierra-research/tau-bench](https://github.com/sierra-research/tau-bench) and AppWorld `0.1.3.post1` through [AppWorld](https://appworld.dev/), under their respective terms. Frozen protocol and source excerpts document recovery interventions, quotas, prompts and scoring. This release's executable guarantee is offline verification; it is not a turnkey collector or a promise that historical remote model services remain unchanged.

Original software is MIT licensed; original analytical data and documentation are CC BY 4.0. These grants cover only the authors' contributions. Third-party content retains its own licenses and redistribution conditions. See `THIRD_PARTY.md`.
