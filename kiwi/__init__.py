import sys
import logging
from flask import Flask, request

from kiwi.sites.hello import App as HelloApp

def create_app():
  app = Flask(__name__, static_folder='../contents')
  app.logger.addHandler(logging.StreamHandler(sys.stdout))
  app.logger.setLevel(logging.INFO)
  app.add_url_rule('/favicon.ico',
                   'favicon',
                   lambda: app.send_static_file('kiwi.ico'))

  # Hello Sample
  app.add_url_rule('/hello/<path:path>',
                   'hello',
                   lambda path: HelloApp(app, request),
                   methods=['GET', 'POST'])
  app.add_url_rule('/hi/<path:path>', 'hello', methods=['GET', 'POST'])

  return app
