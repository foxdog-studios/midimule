#!/usr/bin/env zsh

setopt ERR_EXIT
setopt NO_UNSET


# ==============================================================================
# = Configuration                                                              =
# ==============================================================================

repo=$(realpath -- ${0:h}/..)

venv=$repo/local/venv

pacman_packages=(
    git
    python2-virtualenv
    zsh
)


# ==============================================================================
# = Tasks                                                                      =
# ==============================================================================

function install_pacman_packages()
{
    sudo pacman --noconfirm --sync --needed --refresh $pacman_packages
}

function create_virtualenv()
{
    mkdir --parents $venv:h
    virtualenv --python=python2.7 $venv
}

function install_pygame()
{(
    local tmp=$(mktemp -d)
    cd $tmp

    local source_url=http://www.pygame.org/ftp/pygame-1.9.1release.tar.gz
    curl $source_url | tar xz

    local patch_url
    patch_url=https://projects.archlinux.org/svntogit/packages.git/plain/trunk/
    patch_url+=pygame-v4l.patch?h=packages/python-pygame
    curl $patch_url | patch -p0

    unsetopt NO_UNSET
    source $venv/bin/activate
    setopt NO_UNSET

    cd pygame-1.9.1release
    pip install .
    rm --force --recursive $tmp
)}

function install_python_packages()
{
    unsetopt NO_UNSET
    source $venv/bin/activate
    setopt NO_UNSET

    pip install --requirement $repo/requirements.txt
}


# ==============================================================================
# = Command line interface                                                     =
# ==============================================================================

tasks=(
    install_pacman_packages
    create_virtualenv
    install_pygame
    install_python_packages
)

function usage()
{
    cat <<-'EOF'
		Set up a development environment

		Usage:

		    setup.zsh [TASK...]

		Tasks:

		    install_pacman_packages
		    create_virtualenv
		    install_pygame
		    install_python_packages
	EOF
    exit 1
}

for task in $@; do
    if [[ ${tasks[(i)$task]} -gt ${#tasks} ]]; then
        usage
    fi
done

for task in ${@:-$tasks}; do
    print -P -- "%F{green}Task: $task%f"
    $task
done

