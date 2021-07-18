#!/bin/bash

USAGE="Usage: build {linux|widows|mac}"


if [[ -z "$1" || -n "$2" ]]; then
	echo $USAGE 
	return 1
elif [[ "$1" == "linux" ]]; then
	pip3 install -r requirements.txt &&
	pyinstaller -F --clean --hidden-import "pynput.keyboard._xorg" --hidden-import "pynput.mouse._xorg" vimmouse.py
elif [[ "$1" == "windows" ]]; then
	pip3 install -r requirements.txt &&
	pyinstaller -F --clean --hidden-import "pynput.keyboard._win32" --hidden-import "pynput.mouse._win32" vimmouse.py
elif [[ "$1" == "mac" ]]; then
	pip3 install -r requirements.txt &&
	pyinstaller -F --clean --hidden-import "pynput.keyboard._darwin" --hidden-import "pynput.mouse._darwin" vimmouse.py
else
	echo $USAGE
	return 1
fi

echo "----------------------------------"
echo "Your executable is ready in dist/"
echo "----------------------------------"

return 0
