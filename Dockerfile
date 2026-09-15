# The build environment for this book. CI uses this image and so should you,
# so "works on my machine" never becomes an argument.
#
# Everything is pinned: the base image, Quarto, and the exact TeX Live package
# set. The package list in tools/texlive-packages.txt was captured from a
# working build rather than guessed -- regenerate it with
#   tlmgr list --only-installed | sed 's/^i //; s/:.*//' | grep -v '\.' | sort -u
#
# Build:  just docker-build
# Use:    just build          (every recipe runs in here unless LOCAL=1)

# Pinned by digest, not just by tag -- a dated tag can still be re-pushed.
# This is the manifest list, so it resolves on both amd64 and arm64.
FROM debian:bookworm-20250630-slim@sha256:6ac2c08566499cc2415926653cf2ed7c3aedac445675a013cc09469c9e118fdd

# Quarto pins TinyTeX too -- `quarto install tinytex` fetches the version that
# Quarto release was tested against, so this single pin covers both.
ARG QUARTO_VERSION=1.10.18
ARG TARGETARCH=amd64

ENV DEBIAN_FRONTEND=noninteractive \
    PATH=/usr/local/bin:$PATH \
    PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        fontconfig \
        git \
        # tlmgr is a Perl program; TinyTeX will not run without these.
        perl \
        libfontconfig1 \
        python3 \
        python3-pip \
        # hunspell drives the Persian spell check in lint.yml
        hunspell \
        hunspell-fa \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL -o /tmp/quarto.deb \
        "https://github.com/quarto-dev/quarto-cli/releases/download/v${QUARTO_VERSION}/quarto-${QUARTO_VERSION}-linux-${TARGETARCH}.deb" \
    && dpkg -i /tmp/quarto.deb \
    && rm /tmp/quarto.deb \
    && quarto --version

# The binary directory is named after the platform (x86_64-linux, aarch64-linux
# and so on), so it is discovered rather than hardcoded. `tlmgr path add`
# symlinks everything into /usr/local/bin, which is already on PATH, so every
# later step and every `just` recipe finds lualatex without knowing the name.
RUN quarto install tinytex --no-prompt \
    && "$(find /root/.TinyTeX/bin -name tlmgr -type f | head -1)" path add \
    && tlmgr --version \
    && lualatex --version | head -1

# Installed as an explicit list, not on demand. Auto-installation during a
# render would make the image's contents depend on the order CI happened to
# build things in, which is the opposite of reproducible.
COPY tools/texlive-packages.txt /tmp/texlive-packages.txt
RUN tlmgr install $(tr '\n' ' ' < /tmp/texlive-packages.txt) \
    && tlmgr path add \
    && rm /tmp/texlive-packages.txt \
    && luaotfload-tool --update

# Vendored rather than resolved from the system, so a font update on the host
# cannot change the typeset output. Also installed system-wide so fontconfig
# can find them for the HTML preview.
COPY fonts/ /usr/share/fonts/truetype/vazirmatn/
RUN fc-cache -f && fc-list | grep -q Vazirmatn

# The checkers come from PyPI as `linji-tools` -- they are general and live
# outside this repository. tools/anchors.py, the adapter, is mounted with the
# rest of the tree at run time.
COPY tools/requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir --break-system-packages -r /tmp/requirements.txt \
    && rm /tmp/requirements.txt \
    && python3 -c "import linji_tools; print(linji_tools.__version__)"

WORKDIR /book

# Fail the build rather than ship an image that cannot typeset Persian.
RUN printf '%s\n' \
      '\documentclass{book}' \
      '\usepackage[bidi=basic,provide=*]{babel}' \
      '\babelprovide[import,main,maparabic]{persian}' \
      '\babelfont{rm}[Path=/usr/share/fonts/truetype/vazirmatn/,Renderer=Harfbuzz]{Vazirmatn-Regular.ttf}' \
      '\begin{document}' \
      'سلام جهان' \
      '\end{document}' > /tmp/smoke.tex \
    && cd /tmp && lualatex -interaction=nonstopmode smoke.tex >/dev/null \
    && rm -f /tmp/smoke.*

CMD ["/bin/bash"]
