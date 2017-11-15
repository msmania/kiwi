import os
from io import StringIO
from flask import request

def environ_checker():
  env_pairs = []
  for key in request.environ:
    value = request.environ[key]
    if (type(value) == str):
      env_pairs.append((key, value))
    elif (type(value) == bool
          or type(value) == int
          or type(value) == type
          or type(value) == tuple):
      env_pairs.append((key, str(value)))
    else:
      env_pairs.append((key, str(type(value))))

  output = StringIO()
  output.write('PID = ')
  output.write(str(os.getpid()))
  output.write(' UID = ')
  output.write(str(os.getuid()))
  output.write(' GID = ')
  output.write(str(os.getgid()))
  output.write('\n\n')

  for pair in sorted(env_pairs):
    output.write(pair[0])
    output.write(' = ')
    output.write(pair[1])
    output.write('\n')

  return output.getvalue(), \
         200, \
         {'Content-Type': 'text/plain; charset=utf-8'}
