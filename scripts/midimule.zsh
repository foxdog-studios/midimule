#!/usr/bin/env zsh

setopt ERR_EXIT
setopt LOCAL_OPTIONS
setopt NO_UNSET
setopt PIPE_FAIL

repo=${${(%):-%x}:A:h:h}

unsetopt ERR_EXIT NO_UNSET
source $repo/local/venv2/bin/activate
setopt ERR_EXIT NO_UNSET

export PYTHONPATH=${PYTHONPATH:+$PYTHONPATH:}$repo/src
exec python -m midimule $@
