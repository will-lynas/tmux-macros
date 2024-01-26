#!/usr/bin/env python3.11
from subprocess import check_output

INSTALL_DIR = "~/dotfiles/tmux-macros"

class MyException(Exception):
    ...

def run_command(command: str) -> str:
    return check_output(command, shell=True).strip().decode("utf-8")

def get_tmux_option(option: str, default: str) -> str:
    result = run_command(f"tmux show-option -gqv {option}")
    return result or default

if __name__ == "__main__":
    keybind = get_tmux_option("@tm-keybind", "e")
    inner_command = f"{INSTALL_DIR}/pane_main.py #{{pane_id}}"
    command = f"tmux display-popup -w80% -h80% -E \"{inner_command}\""
    run_command(f"tmux bind {keybind} run-shell '{command}'")
