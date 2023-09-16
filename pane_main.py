#!/usr/bin/env python3.10
from subprocess import CalledProcessError
import json
import os
import sys

from main import get_tmux_option, MyException, INSTALL_DIR, run_command

def get_macros() -> dict[str, str]:
    # A space-separated list of json files to load macros from
    files = get_tmux_option("@tm-macro-files", f"{INSTALL_DIR}/example_macros.json").split(" ")
    out = {}
    for file in files:
        try:
            with open(os.path.expanduser(file)) as f:
                data = f.read()
            out |= json.loads(data.strip())
        except FileNotFoundError:
            pass
    out = {k: v for k, v in out.items() if "\n" not in k} # This would mess up fzf
    return out

def choose_macro(macros: dict[str, str]) -> str:
    options = "\n".join(macros.keys())
    try:
        choice = run_command(f"echo '{options}' | fzf --preview='{INSTALL_DIR}/show_macro.py {{}}'")
    except CalledProcessError as err:
        raise MyException from err
    return macros[choice]

if __name__ == "__main__":
    try:
        pane = sys.argv[1] # The pane to send the result to
        macros = get_macros()
        val = choose_macro(macros)
        run_command(f"tmux send-keys -t {pane} -l '{val}'")
    except MyException:
        pass
