#!/usr/bin/env zsh

setopt ERR_EXIT
setopt NO_UNSET

repo=$(realpath "$(dirname "$(realpath -- $0)")/..")
find $repo/midimule -name '*.pyc' -delete
rm --force --recursive $repo/local

