#!/usr/bin/env python3
import sys

from pane_main import get_macros

macros = get_macros()
key = sys.argv[1]
if key:
    print(macros[key])

