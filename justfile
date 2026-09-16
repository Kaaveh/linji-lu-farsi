# Task runner. Every recipe runs inside the pinned container by default, so
# what you get locally is what CI gets. Override with LOCAL=1 to run on the
# host, which is much faster for the Python checks:
#
#     just check              # in the container
#     LOCAL=1 just check      # on the host, needs `just venv` first
#
# Note for Linux hosts: the container runs as root, so files written by
# `just fix` and `just build` will be root-owned. Use LOCAL=1 for those, or
# chown afterwards. TinyTeX lives in /root, so --user is not an option.

image := "ghcr.io/kaaveh/linji-lu-farsi:latest"
local := env_var_or_default("LOCAL", "0")

# Prefer the project venv on the host; fall back to whatever python3 is around.
py := if path_exists(".venv/bin/python") == "true" { ".venv/bin/python" } else { "python3" }

run := if local == "1" { "" } else {
  "docker run --rm -v " + justfile_directory() + ":/book -w /book " + image + " "
}
python := if local == "1" { py } else { "docker run --rm -v " + justfile_directory() + ":/book -w /book " + image + " python3" }

_default:
    @just --list

# Everything CI runs on a pull request. The checkers come from the installed
# linji-tools package; tools/anchors.py is the adapter that stays here.
check: test
    {{python}} -m linji_tools.normalize --check
    {{python}} -m linji_tools.check_linebreaks --check
    {{python}} -m linji_tools.check_parity --check
    {{python}} tools/anchors.py --check
    {{python}} -m linji_tools.status_table --check

# Two suites, kept apart on purpose. linji_tools/ is general and its tests must
# pass without any of this book's config; tools/tests/ covers the adapter, which
# is nothing but this book's config.
test:
    {{python}} -m unittest discover -s linji_tools/tests
    {{python}} -m unittest discover -s tools/tests

# Bidi overrides are reported but never rewritten, so this can still leave
# `just check` failing. That is by design -- a human has to look at those.
# Correct what can be corrected automatically.
fix:
    {{python}} -m linji_tools.normalize --fix
    {{python}} -m linji_tools.check_linebreaks --fix

# HTML, PDF and EPUB.
build:
    {{run}}quarto render

pdf:
    {{run}}quarto render --to pdf

# The phone edition: a 90x160mm page, so the same 12pt fills the screen.
# Lands in _book-mobile/, never touching the desktop PDF. See _quarto-mobile.yml.
pdf-mobile:
    {{run}}quarto render --profile mobile --to pdf

epub:
    {{run}}quarto render --to epub

# Live preview with reload. Opens on http://localhost:4200.
serve:
    {{ if local == "1" { "quarto preview --port 4200" } else { "docker run --rm -it -p 4200:4200 -v " + justfile_directory() + ":/book -w /book " + image + " quarto preview --port 4200 --host 0.0.0.0 --no-browser" } }}

# Create or refresh fa/ stubs from source/. Never overwrites existing work.
stubs:
    {{python}} -m linji_tools.make_stubs

# Chapter status table for the README.
status:
    {{python}} -m linji_tools.status_table

status-write:
    {{python}} -m linji_tools.status_table --write

docker-build:
    docker build -t {{image}} .

# Host-side Python environment, for LOCAL=1.
venv:
    python3 -m venv .venv
    .venv/bin/pip install --upgrade pip
    .venv/bin/pip install -r tools/requirements.txt

clean:
    rm -rf _book _book-mobile .quarto
