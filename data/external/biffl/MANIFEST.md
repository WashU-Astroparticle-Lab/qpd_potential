# Biffl et al. (2023) -- capture-recoil background for reactor CEvNS

**Retrieved:** 2026-07-23. **`WebFetch` and LLM summarizers were NOT used as a data source.**

The extracted text `2212.14148v2.txt` is the frozen source of record and IS committed. The source
PDF is gitignored (1.6 MB binary), reproducible via the command below and verified by SHA-256.

## Retrieval command (reproducible)

```bash
curl -sS -m 120 -o 2212.14148v2.pdf "https://arxiv.org/pdf/2212.14148"
python3 -c "import pypdf; open('2212.14148v2.txt','w').write('\n'.join((p.extract_text() or '') for p in pypdf.PdfReader('2212.14148v2.pdf').pages))"
shasum -a 256 2212.14148v2.pdf 2212.14148v2.txt
```

## Integrity

| file | sha256 | committed |
|---|---|---|
| `2212.14148v2.pdf` | `5eee50ee15ddc1d45470fb93b887c8259383860f011b268dbc946c16b916639c` | no (gitignored) |
| `2212.14148v2.txt` | `087d9171023ee55b6fdba32b59462b27234ffe10c9f7e99448507f18ac35a888` | yes |

## Source

A. J. Biffl, A. Gevorgian, K. Harris, A. N. Villano, *Neutron capture-induced nuclear recoils as
background for CEvNS measurements at reactors*, **Phys. Rev. D 107, 092011 (2023)**,
arXiv:2212.14148v2, DOI 10.1103/PhysRevD.107.092011. University of Colorado Denver.

## What it establishes for this project

- The published treatment of exactly our (n,gamma) capture recoil background for reactor CEvNS in
  Ge. Computes the recoil spectrum with `nrCascadeSim` (see `data/external/nrcascadesim/`).
- Authorship confirmation: **Biffl, Gevorgian, Harris & Villano** (corrects a "Zhang et al."
  mis-attribution of this arXiv ID in `GPD/literature/PITFALLS.md`).
- Ge is the favourable target ("larger CEvNS cross section and lower capture rates at low energy").
- Quenching largely cancels in the capture-vs-CEvNS comparison ("the shift is largely the same for
  both capture and neutrino induced recoils").
- The thermal flux is measurable in situ from the 71Ge EC line rate -- the same line this project
  already carries as an RoI background.
