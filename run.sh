#!/bin/bash -x

PYTHON_PATH=/usr/bin/python3
PYTHON_ENV=.virtualenv
PYTHON_SCRIPT=doSomething.py

if [ ! -d "$PYTHON_ENV" ]; then
	echo "Directorio no encontrado"
	"$PYTHON_PATH" -m venv "$PYTHON_ENV"
fi

source $PYTHON_ENV/bin/activate

PYTHON_PATH="$PYTHON_ENV/bin/python3"
"$PYTHON_PATH" -m pip install --upgrade pip
"$PYTHON_PATH" -m pip install -r requirements.txt

# RUN
"$PYTHON_PATH" "$PYTHON_SCRIPT"
