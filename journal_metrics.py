"""Journal Metrics Toolkit — transparent implementations of standard journal metrics.

These functions implement the *published formulas* for teaching and exploratory
use. Official metric values are published only by their providers
(Clarivate JCR, Elsevier Scopus, SCImago, Google Scholar).

Conventions
-----------
- ``citations``: dict mapping a *citing* year -> number of citations received
  in that year.
- ``items``: dict mapping a *publication* year -> number of citable items (or
  documents) published in that year.
"""

from __future__ import annotations


def journal_impact_factor(citations: dict[int, int],
                         citable_items: dict[int, int],
                         year: int) -> float:
    """Journal Impact Factor (JIF) for ``year``.

    JIF(Y) = citations received in year Y to citable items published in
    Y-1 and Y-2, divided by the number of citable items published in Y-1, Y-2.

    Official source: Clarivate Journal Citation Reports (Web of Science data).
    """
    window = (year - 2, year - 1)
    cites = citations.get(year, 0)
    denom = sum(citable_items.get(y, 0) for y in window)
    if denom == 0:
        raise ValueError("No citable items in the 2-year window.")
    return cites / denom


def five_year_impact_factor(citations: dict[int, int],
                            citable_items: dict[int, int],
                            year: int) -> float:
    """5-year Journal Impact Factor: same idea as JIF over a 5-year window."""
    window = range(year - 5, year)
    cites = citations.get(year, 0)
    denom = sum(citable_items.get(y, 0) for y in window)
    if denom == 0:
        raise ValueError("No citable items in the 5-year window.")
    return cites / denom


def citescore(citations: dict[int, int],
              documents: dict[int, int],
              year: int) -> float:
    """CiteScore-style metric for ``year``.

    CiteScore(Y) = citations received in year Y to documents published in
    Y-1, Y-2, Y-3, divided by the number of documents published in Y-1..Y-3.

    Official source: Elsevier Scopus. Note CiteScore counts more document
    types than JIF's "citable items".
    """
    window = (year - 3, year - 2, year - 1)
    cites = citations.get(year, 0)
    denom = sum(documents.get(y, 0) for y in window)
    if denom == 0:
        raise ValueError("No documents in the 3-year window.")
    return cites / denom


def h5_index(citation_counts: list[int]) -> int:
    """h5-style index: largest h such that h articles have >= h citations.

    Pass citation counts for articles published in the last 5 complete years.
    (Google Scholar's h5-index; h5-median is the median of those h counts.)
    """
    ranked = sorted(citation_counts, reverse=True)
    h = 0
    for i, c in enumerate(ranked, start=1):
        if c >= i:
            h = i
        else:
            break
    return h


def quartile(rank: int, total_journals: int) -> str:
    """Quartile (Q1 best .. Q4) for a 1-based ``rank`` out of ``total_journals``.

    Journals are ranked within ONE subject category, then split into four
    roughly equal groups. A journal can sit in different quartiles in
    different categories.
    """
    if not 1 <= rank <= total_journals:
        raise ValueError("rank must be between 1 and total_journals")
    # Boundaries: Q1 = top 25%, Q2 = 25-50%, Q3 = 50-75%, Q4 = bottom 25%.
    cut = total_journals / 4
    if rank <= cut:
        return "Q1"
    if rank <= 2 * cut:
        return "Q2"
    if rank <= 3 * cut:
        return "Q3"
    return "Q4"


def interpret(metric_name: str, value: float) -> str:
    """One-line plain-language interpretation of a metric value."""
    guides = {
        "JIF": "average citations per recent article; compare only within a field",
        "CiteScore": "Scopus-based average citations per document over 4 years",
        "SJR": "prestige-weighted influence (higher = more prestigious citers)",
        "SNIP": "field-normalized impact; accounts for differing citation cultures",
        "h5-index": "recent 5-year influence of the journal's articles",
    }
    what = guides.get(metric_name, "journal-level citation metric")
    return f"{metric_name} = {value:.3f} ({what})."


if __name__ == "__main__":
    # --- Worked example with sample data ---
    cites = {2024: 120}                       # citations received in 2024
    items = {2022: 40, 2023: 50, 2021: 45}    # citable items per year

    jif = journal_impact_factor(cites, items, 2024)
    cs = citescore(cites, items, 2024)
    print(interpret("JIF", jif))        # 120 / (40 + 50) = 1.333
    print(interpret("CiteScore", cs))   # 120 / (45 + 40 + 50) = 0.889
    print("Quartile for rank 12 of 200:", quartile(12, 200))   # Q1
    print("Quartile for rank 150 of 200:", quartile(150, 200)) # Q3
    print("h5-index of sample:", h5_index([30, 22, 15, 9, 9, 4, 2, 1]))
