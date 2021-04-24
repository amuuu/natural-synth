# Server

To run the server, first run these commands in this directory to initialize the venv:
```
$ python3 -m venv venv
$ source venv/bin/activate
(venv)$ pip3 install -r requirements.txt
```

After that, everytime you want to run the server in debug mode, run these:
```
$ source venv/bin/activate
(venv)$ export FLASK_APP=project
(venv)$ export FLASK_DEBUG=1
(venv)$ flask run
```