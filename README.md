# Data materials

Analysis data and code for examining how read and write budgets, commitment stage and budget feedback affect large language model agent recovery.

[Download the materials](https://github.com/YuLuo-yy/tool-recovery-artifacts/archive/refs/heads/main.zip)

## Contents

- Analysis inputs and complete statistical comparison records.
- Experimental protocols, sampling records and data definitions.
- Statistical and plotting code for the main and supplementary results.
- Selected native-state records and public tool observations for replay.

The [result index](CLAIMS_V110.json) links findings to their supporting files. The [figure index](FIGURE_MAP.json) identifies the 10 main and 11 supplementary figures. See the [data dictionary](DATA_DICTIONARY.md) for field definitions and [verification results](VALIDATION.json) for the checks performed.

## Reproduction

Use Python 3.12 and a fresh virtual environment:

    python -m venv .venv
    # Activate the virtual environment for your operating system.
    python -m pip install -r requirements-lock.txt
    python reproduce.py --check
    python reproduce.py --statistics
    python reproduce.py --figures
    python reproduce.py --witnesses

The four flags can also be combined. After installing dependencies, the commands run offline without model credentials.

| Command | Output |
| --- | --- |
| --check | File checksums, inventory completeness and links between results and supporting inputs. |
| --statistics | Statistical estimates, descriptive intervals and complete correction families. |
| --figures | The 10 main and 11 supplementary figure PDFs in outputs/figures/main/ and outputs/figures/supplement/. |
| --witnesses | Selected native-state reconstruction and public-observation replay checks. |

Reports are saved in outputs/. Statistical reproduction retains the specified random seeds and 20,000 bootstrap draws.

## Data coverage

| Study panel | Available inputs |
| --- | --- |
| S7–S10/C2 | Result, protocol and inclusion/exclusion exports. Reproduction is limited to the retained exports for these panels. |
| S11 | Paired object vectors, 16 primary and 64 additional estimates, and 80 interval pairs. |
| S12 | 1,728 outcome records and the complete 40-comparison family. |
| S13 | 2,688 trajectory summaries, all five primary comparisons, protocol and sampling records, and selected native-state observations. |
| S14 | 1,568 scores, both primary comparisons, all 36 resource cells and selected cart-state records. |
| S15 | 3,024 trajectory summaries and projected public tool observations, all four primary interactions and 189 operation-condition cells. |

Repeated conditions share objects within the relevant panels. Supported and unsupported comparisons are included in their complete families. Native-state and observation replay use retained records; full benchmark execution requires the upstream environments.

## Access and file integrity

Download the complete repository and keep every numbered file in materials/ together with the additional encrypted bundle in the repository root. The entry point checks all file inventories and checksums, then unpacks the inputs into .materials/ and .updates/. These generated directories and outputs/ are excluded from Git.

Protected AppWorld-derived materials use the upstream-compatible encrypted distribution format. The supplied public packaging key enables local unpacking for inspection and reproduction. Redistribution of protected materials must retain the upstream conditions. See [third-party materials](THIRD_PARTY.md).

For full environment execution, obtain [AppWorld](https://appworld.dev/) and [tau-bench](https://github.com/sierra-research/tau-bench) at the experiment dependencies specified in THIRD_PARTY.md.

## Licence and citation

Original code is MIT licensed. Original analytical data and documentation are CC BY 4.0. Third-party materials retain their respective licences and distribution conditions.

See [citation information](CITATION.md) when referring to these materials.
