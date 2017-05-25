import os
import mimetypes

class CustomMap:
  def __init__(self, hint=None,
                     path=None,
                     mimetype=None,
                     status=None,
                     location=None):
    self.hint = hint
    self.path = path
    self.type = mimetype
    self.status = status
    self.location = location

  def has_path(self):
    return type(self.path) == str

  def has_type(self):
    return type(self.type) == str

  def has_location(self):
    return type(self.location) == str

  def get_status_code(self):
    return self.status if type(self.status) == int else 200

class ContentMatcher:
  class FileScorer:
    def __init__(self, target_url_path):
      (root, ext) = os.path.splitext(target_url_path)
      self.ext = ext.lower()
      self.filename = os.path.basename(root)

    @staticmethod
    def are_in_same_group(items, group):
      for item in items:
        if item not in group:
          return False
      return True

    extension_groups = [
      ['.html', '.htm'],
      ['.jpeg', '.jpg'],
    ]

    def calculate(self, dirpath, filename):
      (filename, ext) = os.path.splitext(filename)
      ext = ext.lower()
      match_filename = (self.filename == filename.split('[')[0])
      match_ext = (self.ext == ext)
      if not match_ext:
        for group in ContentMatcher.FileScorer.extension_groups:
          if self.are_in_same_group((self.ext, ext), group):
            match_ext = True
            break
      score = 0
      if match_filename and match_ext:
        score = 100
      elif match_filename:
        score = 50
      elif filename.startswith(self.filename):
        score = 20 if match_ext else 10
      return score

  def __init__(self, target_url_path):
    self.scorer = ContentMatcher.FileScorer(target_url_path)
    self.score = 0
    self.candidate = None

  def put_candidate(self, root, filename):
    new_score = self.scorer.calculate(root, filename)
    if new_score > self.score:
      self.score = new_score
      self.candidate = os.path.join(root, filename)

def search_contents_dir(contents_root, target_url_path):
  current_match = ContentMatcher(target_url_path)
  for root, dirs, files in os.walk(contents_root):
    for filename in files:
      current_match.put_candidate(root, filename)
  return current_match.candidate

def search_custom_mapping(mapping, path):
  for m in mapping:
    if m.hint in path:
      return m
  return None

def respond_with_file(contents_root, mapping, path, full_path, logger):
  content_file = None

  # Check custom mapping first
  mapped_item = search_custom_mapping(mapping, full_path)
  if mapped_item == None or not mapped_item.has_path():
    # No match in custom mapping or no path is suggested in the mapping
    # --> search the content directory
    content_file = search_contents_dir(contents_root, path)
    if mapped_item == None:
      mapped_item = CustomMap(status=(404 if content_file == None else 200))
  elif type(mapped_item.path) == str:
    # Custom mapping has a path relative to the content root
    content_file = os.path.join(contents_root, mapped_item.path)

  # Read a file
  body = ''
  if type(content_file) == str and os.path.isfile(content_file):
    logger.info('> ' + full_path);
    logger.info('< ' + content_file);
    with open(content_file, 'rb') as infile:
      body = infile.read()
  else:
    logger.info('! ' + full_path)

  # Build a response
  status_code = mapped_item.get_status_code()
  if status_code != 200:
    body = '<html><body>%idayo</body></html>' % status_code

  headers = {}
  headers['Server'] = 'KiwiServer'
  if mapped_item.has_type():
    headers['Content-Type'] = mapped_item.type
  else:
    (guessed_type, _) = mimetypes.guess_type(path)
    headers['Content-Type'] = guessed_type if guessed_type != None \
                                           else 'text/html'
  if mapped_item.has_location():
    headers['Location'] = mapped_item.location

  return (body, status_code, headers)
