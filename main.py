#!/usr/bin/env python3
from subprocess import check_output

INSTALL_DIR = "~/.tmux_macros"

class MyException(Exception):
    ...

def run_command(command: str) -> str:
    return check_output(command, shell=True).strip().decode("utf-8")

def get_tmux_option(option: str, default: str) -> str:
    result = run_command(f"tmux show-option -gqv {option}")
    return result or default

def split_mode() -> str:
    # How to split the tmux window:
    # 'vertical' - top/bottom split
    # 'horizontal' - side-by-side split
    window_mode = get_tmux_option("@tm-window-mode", "vertical")
    mode_map = {"vertical": "v", "horizontal": "h"}
    return mode_map[window_mode]

if __name__ == "__main__":
    keybind = get_tmux_option("@tm-keybind", "e")
    inner_command = f"{INSTALL_DIR}/pane_main.py #{{pane_id}}"
    command = f"tmux split-window -{split_mode()} \"{inner_command}\""
    run_command(f"tmux bind {keybind} run-shell '{command}'")
