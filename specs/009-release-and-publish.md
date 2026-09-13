# 009 — First Release & Publication

## Context

None of the CI has ever run. The container has never been built, the four
workflows have never executed, and no release has been tagged. This spec is the
first time any of it meets reality — expect it to take longer than it looks.

Publication is two repositories. This one tags a release and attaches the
rendered book; [`Kaaveh/kaavehdev`](https://github.com/Kaaveh/kaavehdev) spec 016
fetches that tarball at its own build time and unpacks it into
`public/translations/linji-lu/`. Cloudflare's build image has no Quarto, which is
why it works this way.

## Goal

The book readable at **kaavehdev.ir/translations/linji-lu/**.

## Dependencies

003–008. Also `kaavehdev` spec 016, which is written and marked 🟨 In progress.

## Requirements

1. **Fill the `_quarto.yml` TBDs first.** Four of them: book title, subtitle,
   author credit, and the four part titles. They are translation decisions, and
   they appear on the cover of the PDF and the front page of the site.
   `LICENSE-CODE` also names a copyright holder that was inferred, not given.

2. **Bootstrap the container.** Run the `image` workflow manually — *Actions →
   image → Run workflow*. `build` and `release` both pull
   `ghcr.io/kaaveh/linji-lu-farsi:latest` and cannot run until it exists. This is
   also the first real test of the Dockerfile; its external references were
   validated by hand but it has never been built.

3. **Open a throwaway pull request** and confirm all four workflows go green:
   `lint`, `build`, `image`, `release` is tag-only. Fix what breaks. The
   `hunspell` step in particular has never run against real Persian prose and
   will likely need entries in `tools/dict/project.dic`.

4. **Tag `v0.1.0`.** Confirm the release carries three assets: the PDF, the EPUB,
   and `linji-lu-farsi-0.1.0-html.tar.gz`. Confirm the relocatability assertion
   in `release.yml` passed.

5. **Then the website.** Implement `kaavehdev` spec 016 and set `bookVersion` to
   `'0.1.0'`. Verify `/translations/linji-lu/` serves, its assets resolve from
   the subpath, and the book's own PDF and EPUB download buttons work.

6. **Check the edit link.** Every book page carries
   «ویرایش این صفحه در گیت‌هاب», pointing back here. Confirm it opens the right
   file in GitHub's web editor from the deployed site — it is the single highest
   value contribution channel and nobody has ever clicked it.

## Acceptance criteria

- [ ] No `TBD` left in `_quarto.yml`; `LICENSE-CODE` names the right holder.
- [ ] `image` workflow green; the container exists in GHCR.
- [ ] `lint` and `build` green on a real pull request.
- [ ] `v0.1.0` tagged; release carries PDF, EPUB and the HTML tarball.
- [ ] `kaavehdev` spec 016 done and its acceptance criteria met.
- [ ] The book loads at kaavehdev.ir/translations/linji-lu/ with working assets,
      search, downloads and edit links.
- [ ] `README.md` and `index.md` links all resolve against the live site.

## Out of scope

Anything after 0.1.0. Versioning from here follows the scheme in `README.md`:
MAJOR for a new edition or retranslation, MINOR for a new chapter or substantive
revision, PATCH for typos and orthography.

## Implementation notes

_(filled in during implementation)_
