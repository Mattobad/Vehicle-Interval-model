PY=python -m py_compile
.PHONY:
    test
test:
    python -m pytest

local_test:
    python run.py

dev:
    cd zappa_app
    zappa deploy dev
    