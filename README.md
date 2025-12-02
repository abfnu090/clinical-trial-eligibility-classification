# Multi-Model Consensus Classification of Clinical Trial Eligibility Criteria

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A three-phase multi-model LLM consensus pipeline for classifying clinical trial eligibility criteria into EHR predictability tiers, with application to NSCLC PD-1/PD-L1 immunotherapy trials.

## Overview

Clinical trial eligibility criteria have nearly doubled in complexity from 2008-2018, contributing to 19.3% of NCI-affiliated trials failing due to low accrual (Peterson et al., 2023). Only 30% of NSCLC patients meet eligibility for Phase III ICI trials. This project develops a reproducible framework for:

1. **Consolidating** heterogeneous eligibility trait expressions into unified umbrella categories
2. **Classifying** each category by EHR predictability to identify high-value imputation targets
3. **Establishing** a multi-model consensus approach that mitigates individual LLM biases

## Pipeline Architecture

```
ClinicalTrials.gov
       ↓
606 Raw Traits
       ↓
Preprocessing (deduplication, normalization)
       ↓
543 Unique Traits
       ↓
┌─────────────────────────────────────┐
│  Phase 1: Umbrella Proposal         │
│  5 LLMs independently propose       │
│  umbrella categories                │
│  → Intersection (≥3/5) → 92 cats    │
└─────────────────────────────────────┘
       ↓
┌─────────────────────────────────────┐
│  Phase 2: Trait → Umbrella Mapping  │
│  Majority voting across 5 LLMs      │
│  → 92% high-confidence agreement    │
└─────────────────────────────────────┘
       ↓
┌─────────────────────────────────────┐
│  Phase 3: Category Classification   │
│  Majority voting across 5 LLMs      │
│  → 71% high-confidence agreement    │
└─────────────────────────────────────┘
       ↓
Three Predictability Tiers:
• P&N:  251 traits (46%) - Imputation targets
• P-NN: 212 traits (39%) - Easily obtainable
• NP:    79 traits (15%) - Requires specialized testing
```

## Models Used

| Model | Provider | Role |
|-------|----------|------|
| Claude Opus 4.5 | Anthropic | Consensus member |
| GPT-5.1 | OpenAI | Consensus member |
| Gemini 3 Pro | Google | Consensus member |
| DeepSeek V3.2 | DeepSeek | Consensus member |
| Grok 4.1 | xAI | Consensus member |

Extended thinking/reasoning modes enabled for all models. Total pipeline cost: **$1.03**

## Classification Framework

| Category | Definition | Examples |
|----------|------------|----------|
| **Predictable & Necessary (P&N)** | Traits not in structured EHR fields; require inference from notes/imaging | ECOG PS, Brain metastases, Prior systemic therapy |
| **Predictable but Not Necessary (P-NN)** | Traits in structured EHR or easily obtainable via routine testing | Age, Lab values, HIV status |
| **Not Predictable (NP)** | Traits requiring specialized molecular/tissue testing | PD-L1 expression, ALK rearrangement, Tumor tissue |

## Repository Structure

```
├── data/
│   ├── raw_traits.csv              # 606 raw eligibility traits
│   └── preprocessed_traits.csv     # 543 unique traits after cleaning
├── results/
│   ├── phase1/                     # Umbrella proposals per model
│   ├── phase2/                     # Trait mapping results per model
│   ├── phase3/                     # Category classification per model
│   ├── unified_umbrellas.json      # 92 merged umbrella categories
│   ├── phase2_consensus.csv        # Trait→Umbrella consensus
│   ├── phase3_consensus.csv        # Umbrella→Category consensus
│   └── final_classification.csv    # Complete trait-level results
├── scripts/
│   ├── preprocess.py               # Trait preprocessing
│   ├── phase1_umbrella.py          # Phase 1 pipeline
│   ├── phase2_mapping.py           # Phase 2 pipeline
│   ├── phase3_classification.py    # Phase 3 pipeline
│   └── consensus.py                # Majority voting logic
├── figures/
│   └── pipeline_workflow.png       # Workflow diagram
├── requirements.txt
├── LICENSE
└── README.md
```

## Results Summary

### Agreement Statistics

| Phase | Items | Green (≥4/5) | Yellow (3/5) | Red (<3/5) |
|-------|-------|--------------|--------------|------------|
| Phase 2: Trait→Umbrella | 543 | 501 (92.2%) | 34 (6.3%) | 7 (1.3%) |
| Phase 3: Umbrella→Category | 92 | 65 (70.7%) | 26 (28.3%) | 1 (1.1%) |

### Model Voting Patterns (Phase 3)

| Model | P&N | P-NN | NP |
|-------|-----|------|-----|
| Claude Opus 4.5 | 24 (26.1%) | 51 (55.4%) | 17 (18.5%) |
| GPT-5.1 | 56 (60.9%) | 25 (27.2%) | 11 (12.0%) |
| Gemini 3 Pro | 37 (40.2%) | 45 (48.9%) | 10 (10.9%) |
| DeepSeek V3.2 | 30 (32.6%) | 43 (46.7%) | 19 (20.7%) |
| Grok 4.1 | 10 (10.9%) | 66 (71.7%) | 16 (17.4%) |

## Installation

```bash
git clone https://github.com/[username]/clinical-trial-eligibility-classification.git
cd clinical-trial-eligibility-classification
pip install -r requirements.txt
```

## Usage

```python
# Example: Load final classification
import pandas as pd

df = pd.read_csv('results/final_classification.csv')
print(df[df['category'] == 'PREDICTABLE_AND_NECESSARY'].head())
```

## Citation

If you use this work, please cite:

```bibtex
@inproceedings{author2025multimodel,
  title={Multi-Model Consensus Classification of Clinical Trial Eligibility Criteria for EHR-Based Patient Matching},
  author={[Author] and Zhuang, Yan},
  booktitle={AMIA Clinical Informatics Conference},
  year={2025}
}
```

## Key References

1. Peterson JS, et al. Growth in eligibility criteria content and failure to accrue among NCI-affiliated clinical trials. *Cancer Med.* 2023;12(4):4715-4724.
2. Yoo SH, et al. Generalization and representativeness of phase III immune checkpoint blockade trials in NSCLC. *Thoracic Cancer.* 2018;9(12):1617-1622.
3. Yuan C, et al. Criteria2Query: a natural language interface to clinical databases for cohort definition. *J Am Med Inform Assoc.* 2019;26(4):294-305.
4. MacKay E, et al. Multi-LLM voting strategies for structured data extraction. *Br J Anaesth.* 2025.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Contact

- Abdul [Last Name] - Indiana University
- Dr. Yan Zhuang - Indiana University
