# Erdős Problem 151 — finite graph experiments

Preserved local research programs from the September 14 Erdős-problem hunt, recovered on **7 October 2026**. The investigation concerns the clique-transversal inequality `tau(G) <= n-H(n)`; the code treats maximal cliques with at least two vertices. This repository contains finite checks and search programs, not a general proof.

## Verified in this recovery

```sh
python3 -m pip install -r requirements.txt
python3 -B src/p151_atlas.py
```

The graph-atlas replay checked every graph of orders 3 through 7: **4, 11, 34, 156 and 1,044** graphs, respectively, and found zero counterexamples in the program's stated convention. The exact fresh output is in [verification/atlas-2026-10-07.txt](verification/atlas-2026-10-07.txt).

The inherited hunt README claims checks through 12 vertices. The associated `p151_exh.py` only enumerates graphs with its prescribed degree and independence filters and depends on `./nauty/geng`. The corresponding complete historical logs and nauty binary were not recovered, so this upload does **not** describe the through-12 claim as freshly verified or independent evidence.

## Programs

- `src/p151_atlas.py`: exhaustive NetworkX graph-atlas diagnostic.
- `src/p151_exh.py`: filtered nauty search; run from `src/` with a separately installed `nauty/geng` at the expected path.
- `src/p151_sa.py` and `src/p151_sa2.py`: simulated annealing searches, not exhaustive proofs.
- `src/p151.py`: Ramsey-extremal-complement experiments.

All programs are preserved in their recovered form. Their finite table of Ramsey numbers limits supported orders; they are not general-purpose arbitrary-order verifiers. [Provenance](PROVENANCE.md) records the source and distinction between preserved claims and fresh evidence. No new license is granted. Problem source: [Thomas Bloom's page](https://www.erdosproblems.com/151). [All recovered Erdős work](https://github.com/cubres/erdos-research-index).
