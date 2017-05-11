import pdb
from wsgiref import simple_server
from kiwi import create_app

if __name__ == '__main__':
  app = create_app()
  httpd = simple_server.make_server('0.0.0.0', 8000, app)
  pdb.run('httpd.serve_forever()')
