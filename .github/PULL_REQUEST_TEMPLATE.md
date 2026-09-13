<!--
Translating a chapter you have not claimed? Please stop and read
CONTRIBUTING.md first — it will be declined, and that is a waste of your time.
Typos, orthography, footnote corrections and tooling are all welcome without
asking.
-->

## What this changes

<!-- One or two sentences. If it closes an issue, say "closes #NN". -->

## Type

- [ ] Typo or orthography
- [ ] Factual or footnote correction
- [ ] Chapter translation (claimed in #___)
- [ ] Tooling, build or CI
- [ ] Something else:

## Checks

- [ ] `just check` passes locally
- [ ] Every commit is signed off (`git commit -s`)
- [ ] One sentence per line in anything I touched under `fa/`
- [ ] I have read the rendered PDF from the build comment, not only the diff

<!--
That last one matters more than it looks. Bidi problems, missing ZWNJ and bad
line breaks are obvious when typeset and nearly invisible in Markdown. The
build workflow posts a comment with a PDF link a minute or two after you push.
-->

## Terminology

- [ ] This PR introduces no new rendering of a term
- [ ] It uses a rendering already settled in `glossary.yml`
- [ ] It needs a terminology decision — issue #___

<!--
If a term needs deciding, open a terminology issue rather than settling it
here. Those issues are the project's decision log; a PR that quietly changes a
term erases the reasoning.
-->
