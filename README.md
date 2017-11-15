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

If you want to host contents over SSL:

```
$ sudo iptables -t nat -A PREROUTING -p tcp --dport 443 -j REDIRECT --to-ports 8000
$ gunicorn -w10 -b [::]:8000 kiwi.wsgi\
           --keyfile <your privatekey>\
           --certfile <your certificate>
```

## How to integrate Kiwi with Apache

This supposes Kiwi's repo is `/data/src/kiwi` and Apache's htdoc directory is
`/data/htdoc`.  Don't forget to replace them for your environment.

1. Install mod_wsgi.
```
pip install mod_wsgi
```

2. Add for_apache.wsgi into your htdoc directory.  The directories are
hardcoded in `for_apache.wsgi`.  Please update them accordingly.
```
ln -s /data/src/kiwi/kiwi/for_apache.wsgi /data/htdoc/wsgi/kiwi.wsgi
```

3. Modify httpd.conf.  Below is sample configuration to deploy Kiwi under
`/kiwi` in daemon mode.
```
LoadModule wsgi_module modules/mod_wsgi.so
...
Define DOCROOT "/data/htdocs"
...
<IfModule wsgi_module>
  WSGIScriptAlias /kiwi ${DOCROOT}/wsgi/kiwi.wsgi
  WSGIDaemonProcess kiwi\
                    processes=4\
                    threads=10\
                    home=/data/src/kiwi
  <Location "/kiwi">
    WSGIProcessGroup kiwi
  </Location>
</IfModule>
```

## How to add Wininet cache

1. Copy Wininet files into kiwi/contents/<your_favorite_name>/.  Wininet cache can be found in %localappdata%\Microsoft\Windows\INetCache\Low\IE (ProtectedMode) and %localappdata%\Microsoft\Windows\INetCache\IE (Non-ProtectedMode).

2. Define a new dispatcher function under the kiwi/sites directory.  You can use kiwi/sites/hello.py as a reference.

3. Add a url rule in kiwi/\_\_init\_\_.py to associate a url path with your dispatcher function.
