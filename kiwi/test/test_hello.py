import pytest

def test_hello_json(client):
  # Normal positive case
  resp = client.get('/hello/hello-world.htm?salt=123&answer=42')
  assert(resp.status_code == 200)
  assert(resp.content_type == 'text/html')
  assert(resp.data == b'hello-world.htm\n')
  assert(resp.headers['Server'] == 'KiwiServer')
  # Secondary path
  resp = client.get('/hi/hello-world.htm?salt=888&answer=42')
  assert(resp.status_code == 200)
  assert(resp.data == b'hello-world.htm\n')
  # POST has the same effect as GET
  resp = client.post('/hi/hello-world.htm?salt=888&answer=42')
  assert(resp.status_code == 200)
  assert(resp.data == b'hello-world.htm\n')

  # Content-Type based on extension in the request
  resp1 = client.get('/hello/hello-world.jpg?')
  assert(resp1.status_code == 200)
  assert(resp1.content_type == 'image/jpeg')
  assert(resp.data == resp1.data)
  resp2 = client.get('/hello/hello-world.js?salt=666&answer=42')
  assert(resp2.status_code == 200)
  assert(resp2.content_type == 'application/javascript')
  assert(resp.data == resp2.data)
  resp3 = client.get('/hello/hello-world.css')
  assert(resp3.status_code == 200)
  assert(resp3.content_type == 'text/css')
  assert(resp.data == resp3.data)

  # Use CustomMap without suggesting the `path`
  resp4 = client.get('/hello/hello-world.css?type=custom')
  assert(resp4.status_code == 200)
  assert(resp4.content_type == 'application/custom')
  assert(resp.data == resp4.data)

  # Invalid filename --> 404
  resp = client.get('/hello/goodbye')
  assert(resp.status_code == 404)
  assert(resp.data == b'<html><body>404dayo</body></html>')

def test_hello_startpage(client):
  resp = client.get('/hello/start')
  assert(resp.status_code == 200)
  with open('contents/hello/1567_14913.html', 'rb') as f:
    actual_data = f.read()
  assert(resp.data == actual_data)

  resp = client.get('/hello/start.htm')
  assert(resp.status_code == 200)

  # Case-sensitivity
  resp = client.get('/hello/Start')
  assert(resp.status_code == 404)

def test_302_redirection(client):
  resp = client.get('/hello/go?to=spain&when=someday')
  assert(resp.status_code == 302)
  assert(resp.headers['Location'] == 'http://www.spain.info/en_US/')
  assert(resp.data == b'<html><body>302dayo</body></html>')
  resp = client.get('/hello/go?to=japan&when=tomorrow')
  assert(resp.status_code == 302)
  assert(resp.headers['Location'] == 'http://www.japan-guide.com/')
  assert(resp.data == b'<html><body>302dayo</body></html>')

def test_CORS_headers(client):
  resp = client.get('/hello/CORS/hello')
  assert(resp.status_code == 200)
  assert(resp.content_type == 'application/json')
  assert(resp.data == b'hello.json\n')
  assert(resp.headers['Access-Control-Allow-Origin'] == '*')

def test_POST(client):
  resp = client.post('/hello/get', data=b'1')
  assert(resp.status_code == 200)
  assert(resp.data == b'{"d":1}\n')
  resp = client.post('/hello/get', data=b'2')
  assert(resp.status_code == 200)
  assert(resp.data == b'{"d":2}\n')
  resp = client.post('/hello/get', data=b'3')
  assert(resp.status_code == 404)

def test_Handler(client):
  resp = client.get('/hello/custom')
  assert(resp.status_code == 200)
  assert(resp.content_type == 'text/plain')
  assert(resp.data == b'/hello/custom?')
  resp = client.get('/hello/custom?q=xxx')
  assert(resp.status_code == 200)
  assert(resp.content_type == 'text/plain')
  assert(resp.data == b'/hello/custom?q=xxx')
