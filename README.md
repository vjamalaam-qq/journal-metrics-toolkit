# Journal Metrics Toolkit

A small, transparent toolkit for understanding how the most-used journal metrics are
calculated. Built as a companion to the free explainers at
[Research Metrics Guide](https://researchmetricsguide.online).

- **Learn the formulas** behind Journal Impact Factor, CiteScore, quartiles, and more.
- **Run the numbers yourself** on sample or your own citation data.
- **Look up real journals** with our free tools:
  - [Impact Factor Lookup](https://researchmetricsguide.online/tools/impact-factor-lookup/)
  - [Impact Factor vs CiteScore explainer](https://researchmetricsguide.online/impact-factor-vs-citescore/)
  - [How to avoid predatory journals](https://researchmetricsguide.online/how-to-avoid-predatory-journals/)
  - [PRISMA 2020 checklist](https://researchmetricsguide.online/prisma-2020-checklist/)

## Contents

| File | What it is |
|---|---|
| `journal_metrics.py` | Clean, documented implementations of JIF-style, 5-year IF, CiteScore-style, h5-style, and quartile calculations |
| `journal_metrics_definitions.csv` | Machine-readable definitions: provider, citation window, formula, and best use of 9 major metrics |

## Quick start

```bash
python3 journal_metrics.py
```

Or import the functions in your own analysis:

```python
from journal_metrics import journal_impact_factor

citations = {2024: 120}          # citations received in 2024
citable_items = {2022: 40, 2023: 50}  # citable items published per year

print(journal_impact_factor(citations, citable_items, year=2024))
# -> 1.333...
```

## Important notes

- These functions compute the **published formulas** for teaching purposes. Official
  values come only from the providers: JIF from Clarivate's Journal Citation Reports
  (Web of Science data), CiteScore from Elsevier's Scopus, SJR from SCImago.
- SJR and SNIP use proprietary weighting — they are described in
  `journal_metrics_definitions.csv` but cannot be replicated exactly here.
- Metrics are **journal-level**, not article-level. A journal's Impact Factor says
  nothing definitive about any single paper in it.
- Always compare metrics **within a subject category** — citation cultures differ
  wildly between fields. Quartiles (Q1–Q4) exist precisely for this reason.

## License

MIT — use freely, attribution appreciated.
