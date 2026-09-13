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

# Everything CI runs on a pull request.
check: test
    {{python}} tools/normalize.py --check
    {{python}} tools/check_linebreaks.py --check
    {{python}} tools/check_parity.py --check
    {{python}} tools/anchors.py --check
    {{python}} tools/check_glossary.py --check
    {{python}} tools/status_table.py --check

# Unit and end-to-end tests for the checkers.
test:
    {{python}} -m unittest discover -s tools/tests

# Bidi overrides are reported but never rewritten, so this can still leave
# `just check` failing. That is by design -- a human has to look at those.
# Correct what can be corrected automatically.
fix:
    {{python}} tools/normalize.py --fix
    {{python}} tools/check_linebreaks.py --fix

# HTML, PDF and EPUB.
build:
    {{run}}quarto render

pdf:
    {{run}}quarto render --to pdf

epub:
    {{run}}quarto render --to epub

# Live preview with reload. Opens on http://localhost:4200.
serve:
    {{ if local == "1" { "quarto preview --port 4200" } else { "docker run --rm -it -p 4200:4200 -v " + justfile_directory() + ":/book -w /book " + image + " quarto preview --port 4200 --host 0.0.0.0 --no-browser" } }}

# Create or refresh fa/ stubs from source/. Never overwrites existing work.
stubs:
    {{python}} tools/make_stubs.py

# Chapter status table for the README.
status:
    {{python}} tools/status_table.py

status-write:
    {{python}} tools/status_table.py --write

docker-build:
    docker build -t {{image}} .

# Host-side Python environment, for LOCAL=1.
venv:
    python3 -m venv .venv
    .venv/bin/pip install --upgrade pip
    .venv/bin/pip install -r tools/requirements.txt

clean:
    rm -rf _book .quarto
