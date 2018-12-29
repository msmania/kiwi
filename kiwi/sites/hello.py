from kiwi.sites import respond_with_file, CustomMap

def App(app, request):
  mapping = [
    CustomMap(hint='/start',
              path='1567_14913.html'),
    CustomMap(hint='/hello-world.css?type=custom',
              mimetype='application/custom'),
    CustomMap(hint='/go?to=spain',
              status=302,
              location='http://www.spain.info/en_US/'),
    CustomMap(hint='/go?to=japan',
              status=302,
              location='http://www.japan-guide.com/'),
    CustomMap(hint='/CORS/hello',
              path='b1f153f3/719e44f9/hello.json',
              mimetype='application/json',
              acao='*'),
    CustomMap(hint='/get',
              mimetype='application/json',
              path='json1',
              examine=lambda x: b'1' in x),
    CustomMap(hint='/get',
              mimetype='application/json',
              path='json2',
              examine=lambda x: b'2' in x),
    CustomMap(hint='/custom',
              mimetype='text/plain',
              handler=lambda req: bytes(req.full_path, encoding='utf-8')),
  ]
  return respond_with_file(contents_root='contents/hello',
                           mapping=mapping,
                           request=request,
                           logger=app.logger)
