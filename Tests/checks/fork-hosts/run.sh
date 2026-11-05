#!/bin/bash
# FORK.md's hard rule, checked: the code and scripts of this fork (shreyashguptas/sill) name no
# repository, website or server but the fork's own GitHub repository, Apple's own servers and this
# Mac. Run it after every upstream merge, before building; CI runs it with every other check.
#   Tests/checks/fork-hosts/run.sh
here="$(cd "$(dirname "$0")" && pwd)"
source "$here/../common.sh"
if [ "${1:-}" = "--mutants" ]; then echo "fork-hosts: no mutants"; exit 0; fi
exec python3 -I "$here/check.py" "$root"
