#!/bin/bash

# text colors
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

function is_wsl() {
    if [[ $(uname -r) =~ .*microsoft-standard.* ]]; then
        return 0 # WSL, return true
    else
        return 1 # Not WSL, return false
    fi
}

function is_command_installed() {
    if command "$@" >/dev/null 2>&1; then
        return 0 # command succeeded, return true
    else
        return 1 # command failed, return false
    fi
}

function is_package_installed() {
    if dpkg -s "$@" >/dev/null 2>&1; then
        return 0

    else
        return 1
    fi
}

# https://stackoverflow.com/questions/47234947/spinner-animation-and-echo-command
function spinner() {
    local PROC="$1"
    local delay="0.1"
    tput civis # hide cursor
    while [ -d "/proc/$PROC" ]; do
        printf '\033[s\033[u[ / ] %s\033[u' "$str"
        sleep "$delay"
        printf '\033[s\033[u[ — ] %s\033[u' "$str"
        sleep "$delay"
        printf '\033[s\033[u[ \ ] %s\033[u' "$str"
        sleep "$delay"
        printf '\033[s\033[u[ | ] %s\033[u' "$str"
        sleep "$delay"
    done
    printf '\033[s\033[u%*s\033[u\033[0m' $((${#str} + 6)) " " # return to normal
    tput cnorm                                                 # restore cursor
    return 0
}

function install_fish() {
    if is_command_installed fish --version; then
        echo -e "Fish already installed, skipping."
        return 0
    else
        echo "Installing Fish..."

        function _install_fish() {
            sudo apt-add-repository -y ppa:fish-shell/release-3
            sudo apt update && sudo apt -y install fish
        }

        _install_fish >/dev/null 2>&1 # Suppress command output

        if is_command_installed fish --version; then
            echo -e "${GREEN}Fish installed!${NC}"
            return 0
        else
            echo -e "${RED}Fish installation failed, command not found${NC}"
            return 1
        fi
    fi
}

function install_homebrew() {
    if is_command_installed brew --version; then
        echo -e "Homebrew already installed, skipping."
        return 0
    else
        echo "Installing Homebrew..."
        function _install_homebrew() {
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
            # shellcheck disable=SC2016
            echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"' >> "$HOME/.profile"
            # shellcheck source=/dev/null
            source "$HOME/.profile"
        }

        _install_homebrew >/dev/null 2>&1 # Suppress command output

        if is_command_installed brew --version; then
            echo -e "${GREEN}Homebrew installed!${NC}"
            return 0
        else
            echo -e "${RED}Homebrew installation failed, command not found${NC}"
            return 1
        fi
    fi
}

# install oh-my-posh
function install_omp() {
    if is_command_installed oh-my-posh --version; then
        echo -e "oh-my-posh already installed, skipping."
        return 0
    elif ! is_command_installed brew --version; then
        echo -e "Homebrew install not found, unable to continue oh-my-posh install."
        return 1
    else
        echo "Installing oh-my-posh..."
        function _install_omp() {
            brew install jandedobbeleer/oh-my-posh/oh-my-posh
        }

        _install_omp >/dev/null 2>&1 # Suppress command output

        if is_command_installed oh-my-posh --version; then
            echo -e "${GREEN}oh-my-posh installed!${NC}"
            return 0
        else
            echo -e "${RED}oh-my-posh installation failed, command not found${NC}"
            return 1
        fi
    fi
}

# configure fish shell
# shellcheck disable=SC2016
fish_config_data='
if status --is-login
    set -gx PATH /usr/local/bin $PATH
end

# setup homebrew, see https://github.com/orgs/Homebrew/discussions/4412#discussioncomment-8651316
if test -d /home/linuxbrew/.linuxbrew # Linux
    set -gx HOMEBREW_PREFIX "/home/linuxbrew/.linuxbrew"
    set -gx HOMEBREW_CELLAR "$HOMEBREW_PREFIX/Cellar"
    set -gx HOMEBREW_REPOSITORY "$HOMEBREW_PREFIX/Homebrew"
else if test -d /opt/homebrew # MacOS
    set -gx HOMEBREW_PREFIX "/opt/homebrew"
    set -gx HOMEBREW_CELLAR "$HOMEBREW_PREFIX/Cellar"
    set -gx HOMEBREW_REPOSITORY "$HOMEBREW_PREFIX/homebrew"
end

fish_add_path -gP "$HOMEBREW_PREFIX/bin" "$HOMEBREW_PREFIX/sbin";
! set -q MANPATH; and set MANPATH ''; set -gx MANPATH "$HOMEBREW_PREFIX/share/man" $MANPATH;
! set -q INFOPATH; and set INFOPATH ''; set -gx INFOPATH "$HOMEBREW_PREFIX/share/info" $INFOPATH;

# configure omp, only run if executable exists, see https://fishshell.com/docs/current/cmds/test.html
if test -e /home/linuxbrew/.linuxbrew/bin/oh-my-posh
    oh-my-posh init fish --config $(brew --prefix oh-my-posh)/themes/negligible.omp.json | source
end
'

install_fish_config() {
    echo "Setting up fish shell configuration..."

    local fish_config_dir="$HOME/.config/fish"
    local fish_config_file="$fish_config_dir/config.fish"

    # create fish config file if it does not exist
    if [ ! -d "$fish_config_dir" ]; then
        mkdir -p "$fish_config_dir"
    fi
    if [ ! -f "$fish_config_file" ]; then
        touch "$fish_config_file"
    fi

    # write config data to file
    if ! echo "$fish_config_data" > ~/.config/fish/config.fish; then
        echo -e "${RED}Failed to write fish configuration${NC}"
        return 1
    fi

    echo -e "${GREEN}Fish shell configuration installed successfully${NC}"
    return 0
}


# Define the install functions to run
install_functions=(
    "install_fish"
    "install_homebrew"
    "install_omp"
    "install_fish_config"
)

# Run the commands in a loop with a spinner
for cmd in "${install_functions[@]}"; do
    $cmd &
    spinner $!
done
