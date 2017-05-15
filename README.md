# Kiwi

Kiwi is a WSGI application to host Wininet cache as a web server.  Using Kiwi, you can make a local copy of complicated websites (e.g. corporate intranet sites).

## Requirements

### To run Kiwi:

```bash
$ pip install flask gunicorn
```

You can use any of WSGI servers instead of gunicorn.

### To run tests:

```
$ pip install pytest pytest-flask
```

## Install & Run

```
$ git clone https://github.com/msmania/kiwi.git
$ cd kiwi
$ gunicorn --reload --workers 10 -b [::]:8000 kiwi.wsgi
```

## How to add Wininet cache

1. Copy Wininet files into kiwi/contents/<your_favorite_name>/.  Wininet cache can be found in %localappdata%\Microsoft\Windows\INetCache\Low\IE (ProtectedMode) and %localappdata%\Microsoft\Windows\INetCache\IE (Non-ProtectedMode).

2. Define a new dispatcher function under the kiwi/sites directory.  You can use kiwi/sites/hello.py as a reference.

3. Add a url rule in kiwi/\_\_init\_\_.py to associate a url path with your dispatcher function.
