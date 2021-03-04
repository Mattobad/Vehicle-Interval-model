PY=python -m py_compile
.PHONY:
    test
test:
    python -m pytest

dev:
    pip install virtualenv
    virtualenv ml-app
    source ml-app/bin/activate
    pwd
    ls
    pip install -r requirements.txt zappa
    cd zappa_app
    zappa update dev
    