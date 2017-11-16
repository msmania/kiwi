import os
import pdb
from wsgiref import simple_server
from eventlet import wsgi, listen, wrap_ssl
from kiwi import create_app

useSSL = 'USESSL' in os.environ
SSLCert='/path/to/certificate'
SSLPrivateKey='/path/to/privatekey'
PORT = 8000
PORT_SSL = 8001

if __name__ == '__main__':
  app = create_app()
  httpd = simple_server.make_server('', PORT, app) if not useSSL else\
          wsgi.server(wrap_ssl(listen(('', PORT_SSL)),
                               certfile=SSLCert,
                               keyfile=SSLPrivateKey,
                               server_side=True),
                      app)
  pdb.run('httpd.serve_forever()')
