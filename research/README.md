# Research Wiki

The `research/` directory is the research-wiki source base for both of the
repository's applications on Neutron: the Rocket Lab orbital AI-inference data
center and communications (the Iridium model). It contains source notes,
reasoning, synthesis, peer review, historical debates, and open questions. It
does not contain generated model output or the current conclusions; those live
under `data_center/` and `communications/`.

## Navigation

- `SOURCE_INDEX.md` is the source-of-truth claim ledger for public claims and
  release-critical assumptions.
- `RESEARCH_TRACKER.md` records file status, source-audit notes, stale material,
  and open questions.
- `LIBRARY.md` organizes references and explains what each research file is for.
- Topic folders contain the evidence and reasoning behind the claim ledger.
- The communications research ran in nine waves (2026-06-11 to 2026-07-08)
  and the saturation build (its two notes landed here 2026-10-05, the
  saturation note's Section 2 on 2026-10-12), with its own `COMM-*` claim IDs
  in `SOURCE_INDEX.md`. Its documents live under `economics/`,
  `direct_communication/`, `laser_comms/`, `competitors/`, `rocket_lab/` and
  `rocket_lab/neutron/`; its syntheses and lint reports are the
  `synthesis/comms_*` files; its thesis is `vision/comms_thesis.md`, whose
  latest revision (Revision 5) covers waves 5 to 9 and the built models. The two notes behind the Iridium
  model's saturation module are `rocket_lab/flatellite_panel_and_stack.md`
  (the panel and satellites per launch) and
  `direct_communication/iridium_saturation_module.md`.

Model inputs should link back to source IDs, source documents, or research docs
when possible. If a value is only a scenario choice, the model and public docs
should say that plainly rather than treating the value as sourced fact.
