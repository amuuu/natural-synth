# Fake Peripheral Node


## Run

For the first time, run these commands in this directory to initialize the venv:
```
$ python3 -m venv venv
$ source venv/bin/activate
(venv)$ pip3 install -r requirements.txt
```

After that, everytime you want to run the code inside Raspberry Pi, run these:
```
$ source venv/bin/activate
(venv)$ export FLASK_APP=src
(venv)$ export FLASK_DEBUG=1
(venv)$ flask run # or flask run --host 0.0.0.0 --port 5002
```