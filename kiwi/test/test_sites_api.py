import pytest
import os

from kiwi.sites import search_contents_dir

def test_search_contents_dir():
  verify_fullpath = lambda result, filename: \
    os.path.basename(result) == filename

  # any item matches
  result = search_contents_dir('contents/hello', '/')
  assert(type(result) == str)
  result = search_contents_dir('contents/hello', '')
  assert(type(result) == str)

  # 404
  result = search_contents_dir('contents/hello', 'no-slash')
  assert(result == None)
  result = search_contents_dir('contents/hello', '/fakeroot')
  assert(result == None)

  # hello.htm: hello.html > hello.json > hello-world.htm
  result = search_contents_dir('contents/hello', '/hello.htm')
  assert(verify_fullpath(result, 'hello[1].html'))
  # hell.json: hello.json > hello.html > hello-world.htm
  result = search_contents_dir('contents/hello', '/hell.json')
  assert(verify_fullpath(result, 'hello.json'))
  # ni-hao-ma.jpeg: ni-hao-ma.jpg > ni-hao-ma
  result = search_contents_dir('contents/hello', '/ni-hao-ma.jpeg')
  assert(verify_fullpath(result, 'ni-hao-ma.jpg'))
  # case-insensitive extenstion
  result = search_contents_dir('contents/hello', '/ni-hao-ma.jPeG')
  assert(verify_fullpath(result, 'ni-hao-ma.jpg'))
