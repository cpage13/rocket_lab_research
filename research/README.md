# Research Wiki

The `research/` directory is a research-wiki style source base for the Rocket
Lab orbital AI-inference data-center project. It contains source notes,
reasoning, synthesis, peer review, historical debates, and open questions. It
does not contain the canonical generated model output or the current static
conclusion; those live under `data_center/`.

## Navigation

- `SOURCE_INDEX.md` is the source-of-truth claim ledger for public claims and
  release-critical assumptions.
- `RESEARCH_TRACKER.md` records file status, source-audit notes, stale material,
  and open questions.
- `LIBRARY.md` organizes references and explains what each research file is for.
- Topic folders contain the evidence and reasoning behind the claim ledger.
- This same wiki now also holds the communications workstream research (waves 1
  through 4), with its own `COMM-*` claim IDs in `SOURCE_INDEX.md`. Comms source
  docs live under `economics/`, `direct_communication/`, `laser_comms/`,
  `competitors/`, and `rocket_lab/neutron/`; the syntheses are
  `synthesis/comms_baseline_synthesis.md` and
  `synthesis/comms_framework_synthesis.md`; the thesis is
  `vision/comms_thesis.md`.

Model inputs should link back to source IDs, source documents, or research docs
when possible. If a value is only a scenario choice, the model and public docs
should say that plainly rather than treating the value as sourced fact.
