#! /usr/bin/env python3

import argparse
import os
import platform
import string

MAKEFILE = """\
CXX=${cxx}
CXX_LANG=-std=c++17 -I. -march=native -fdiagnostics-color=auto -fno-exceptions -fno-rtti ${warnings}
CXX_MODE=${mode}
CXX_LIBS=-lgtest -lgmock -lglog -lgflags -pthread
CXX_TOOL=$$(CXX) $$(CXX_LANG) $$(CXX_MODE)

.PHONY: run

bin: $$(NAME).cc log.h
\t$$(CXX_TOOL) $$< -o $$(NAME) $$(CXX_LIBS)

run: bin
\t./$$(NAME) < $$(NAME).in
"""


def write_template(t, vars, name, overwrite=False):
    if os.path.exists(name) and not overwrite:
        return
    with open(name, "wt") as f:
        s = string.Template(t).substitute(**vars)
        f.write(s)


ap = argparse.ArgumentParser(
        description="Generate make files for codecon problems")
ap.add_argument("--clang",
        action="store_true",
        help="override to use clang")
ap.add_argument("-o", "--opt",
        action="store_true",
        help="turn on optimization")
args = ap.parse_args()

vars = {}
warnings = ["all", "shadow",
        "conversion",
        "no-sign-conversion",
        "no-unused-function",
        "no-sign-compare",
        "no-char-subscripts"]
if platform.system() == "Darwin" or args.clang:
    vars["cxx"] = "clang++"
    warnings.append("literal-range")
else:
    vars["cxx"] = "g++"
vars["warnings"] = " ".join(["-W" + w for w in warnings])

if args.opt:
    vars["mode"] = "-O3 -ffast-math -flto -DNDEBUG"
else:
    vars["mode"] = "-O0 -g -fsanitize=address -fno-omit-frame-pointer"

write_template(MAKEFILE, vars, "Makefile", overwrite=True)
