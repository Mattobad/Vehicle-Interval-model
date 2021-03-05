PY=python -m py_compile
.PHONY:
    test
test:
    python -m pytest

dev:
    cd ..
    pip install virtualenv
    virtualenv ml-app
    source ml-app/bin/activate
    pwd
    ls
    cd zappa_app
    pip install -r requirements.txt zappa==0.52.0 
    cd zappa_app
    zappa deploy dev
    