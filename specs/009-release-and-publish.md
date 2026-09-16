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

### v0.0.1 was tagged before this spec was started, and produced nothing

The tag exists on GitHub. No release does. Requirement 2 — bootstrap the
container first — was skipped, so `release` died in 31 seconds pulling an image
that had never been published, and nobody noticed because `build` and `lint`
were failing too and had been since they were written.

### Six failures stood between the tag and a release

None were in the book. All were first-contact-with-reality faults in
infrastructure that had been written but never executed, exactly as the Context
section predicted. In the order they surfaced, each hiding the next:

1. **`hunspell-fa` does not exist.** Neither Debian nor Ubuntu packages a
   Persian hunspell dictionary. The Dockerfile's apt step failed on it, so the
   image was never built; lint's `spelling` job installed the same package and
   failed identically, never reaching a file. Requirement 3 expected this step
   to need `project.dic` entries; in fact it had never run at all. The job was
   deleted. `tools/dict/project.dic` is kept — bringing the check back means
   vendoring a dictionary and pointing hunspell at it by path.
2. **No `xz-utils`.** TinyTeX ships as `.tar.xz`; the slim base has no xz, so
   tar's child died and Quarto reported only "Failed to extract".
3. **`find ... -type f` for tlmgr.** Every binary in TinyTeX's bin directory is
   a symlink, so the search matched nothing and the shell ran the empty string:
   `/bin/sh: 1: : Permission denied`, exit 127, immediately after "Installation
   successful".
4. **`tlmgr path add` links nowhere useful.** It reported success and left
   `tlmgr: not found` on the next line. The bin directory is now symlinked once
   to `/opt/texbin`, which `ENV PATH` carries; both `path add` calls are gone.
5. **`tlgpg` is not in TinyTeX's repository.** `tools/texlive-packages.txt` was
   captured from a full TeX Live. tlmgr exits 1 on the one missing name after
   installing all 292 others.
6. **`github.repository_owner` is `Kaaveh`.** metadata-action lowercases it for
   the push, so the image published; `docker run` refuses an uppercase
   repository name, so the smoke render died at exit 125 after a two-minute
   build.

Also: the repository is private, so the GHCR package is too. Both workflows
that pull it need `packages: read` and `credentials:` on the container — an
explicit `permissions:` block grants nothing it does not name.

### What shipped

`v0.0.2`, not `v0.1.0`. PATCH by the README's scheme: no new translation, only
the apparatus around it and the CI beneath it. Four assets — the print PDF, the
phone PDF, the EPUB, and the HTML tarball. `lint`, `build` and `image` are green
on `main`; the relocatability assertion passed.

The spec stays **🟨 In progress**. Requirements 1, 5 and 6 are untouched: the
`_quarto.yml` TBDs still stand, the website is not deployed, and the edit link
has never been clicked from a deployed page.

### Still open before the repository goes public

Release assets on a private repository are downloadable only by people with
access, so the "anyone can download the PDF" story does not hold yet. Making the
repository public also means setting the GHCR package's visibility, or the
`credentials:` above keep it working either way.
