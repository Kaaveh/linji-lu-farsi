#!/usr/bin/env sh
# Developer Certificate of Origin sign-off check, for the commit-msg stage.
#
# The project takes DCO rather than a CLA: lower friction, and inbound equals
# outbound. Signing off says you wrote the change or have the right to submit
# it under the project's licences. See CONTRIBUTING.md.

set -eu

message_file="$1"

# Ignore comment lines -- `git commit` puts the whole template in this file.
if grep -v '^#' "$message_file" | grep -qi '^Signed-off-by: .\+ <.\+@.\+>'; then
    exit 0
fi

cat >&2 <<'EOF'
No Signed-off-by line in the commit message.

Sign off with:

    git commit -s

or amend the commit you just wrote:

    git commit --amend -s --no-edit

Signing off certifies that you wrote the change, or have the right to submit
it under the project's licences (CC BY-SA 4.0 for text, MIT for tooling).
See CONTRIBUTING.md.
EOF

exit 1
