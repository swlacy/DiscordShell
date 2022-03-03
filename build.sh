#!/usr/bin/env bash

input="shell.py"
output="shell"

if [ $# -ne 0 ]; then
    input=$1
fi

pyinstaller --onefile --clean --name $output shell.py
mv dist/$output $output
rm -rf __pycache__ build dist $output.spec

chmod +x $output

printf "\x1b[31m\n[!] Process completed; output: $output\n\x1b[0m\n"
