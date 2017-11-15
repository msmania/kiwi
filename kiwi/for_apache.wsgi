import sys
sys.path.append('/data/src/kiwi')

activate_this = '/data/py3/bin/activate_this.py'
with open(activate_this) as file_:
  exec(file_.read(), dict(__file__=activate_this))

from kiwi import create_app
application = create_app()
