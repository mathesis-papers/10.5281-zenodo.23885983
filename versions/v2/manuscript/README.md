# Orthogonal absolute-product minimum and minimizers

Main source: `note.tex`. The bibliography is embedded; no external figures or
BibTeX database are required. The PDF is `note.pdf`.

## Build

Use Tectonic **0.17.0**:

```sh
tectonic --untrusted note.tex
```

Alternatively use a standard LaTeX installation with `amsmath`, `amssymb`,
`amsthm`, `geometry`, `lmodern`, `microtype` and `hyperref`:

```sh
pdflatex -interaction=nonstopmode -halt-on-error note.tex
pdflatex -interaction=nonstopmode -halt-on-error note.tex
```

No BibTeX step is necessary because the bibliography is embedded. No shell
escape is used.

## Exact controls

Python 3.10 or later, standard library only:

```sh
python3 check.py
```

The program enumerates every nonsingular 2-by-2 integer matrix with entries
between -2 and 2; compares nilpotency of the absolute-product minus the identity
against independent row/column permutability to triangular form; checks seeded
3-by-3 and 4-by-4 examples; constructs rational attaining examples in dimensions
1 through 8; and checks signed-permutation invariance and the two printed
examples. It prints a JSON summary and exits nonzero on a failed assertion.
These finite checks cover the enumerated cases. The universal results have
the written proofs given in the note.

## Scientific coverage

Theorem 1 reuses the triangularization argument in
`D5/S1/Eigenstructure/OrthogonalAbsoluteProductMinimum.lean`, theorem `result`,
at revision `fd1633144086085a16f35c8171e2f4b6186a6fbb` of
`the-omega-institute/trureturing`. The file's SHA256 is
`270bbcf32fb14c35505b668729c4d2a459c960107f1f95dd61d96e7b505e2a33`.
The source theorem supplies the universal bound and actual attainment for every
positive dimension and nonsingular real matrix. The trace argument, complete
minimizer characterization, special-orthogonal refinement, examples and
companion balancing corollary have ordinary proofs in the note.

The companion question 515547 is answered by direct application of Yamabe and
Yujobo's 1950 sphere theorem. The original
paper's scanned byline has both authors, although its repository catalogue
omits the second. Bibliographic details and exact locators are in the note.

Creators: Haobo Ma (ChronoAI Pte Ltd, Singapore), then Wenlin Zhang (National
University of Singapore; ChronoAI Pte Ltd, Singapore). Original note exposition
and metadata: CC BY 4.0 (`cc-by-4.0`). User3's MathOverflow questions are cited
and paraphrased with their distinct CC BY-SA 4.0 attribution. No historical
priority claim is made.
