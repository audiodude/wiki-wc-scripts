import sys

import pymongo

MONGO_URI = None
if len(sys.argv) > 1:
  MONGO_URI = sys.argv[1]
if MONGO_URI:
  client = pymongo.MongoClient(MONGO_URI)
  db = client.get_default_database()
else:
  client = pymongo.MongoClient()
  db = client.wiki_wc_dev

def main():
  for stdin_line in sys.stdin:
    input_file_name = stdin_line.strip()
    with open(input_file_name) as f:
      for line in f:
        parts = line.strip().split('\t')
        if len(parts) != 2:
          print('Found line with not exactly two parts:\n%s' % line)
        token, count = parts[0], int(parts[1])
        db.tokens.insert({'_id': token, 'count': count})

if __name__ == '__main__':
  main()
