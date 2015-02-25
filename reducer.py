#!/usr/bin/env python
from itertools import groupby
from operator import itemgetter
import sys

def yield_stdin(separator):
  for line in sys.stdin:
    yield line.rstrip().split(separator, 1)

def main(separator='\t'):
  for current_word, group in groupby(yield_stdin(separator), itemgetter(0)):
    try:
      total_count = sum(int(count) for current_word, count in group)
      sys.stdout.write(u'%s%s%d\n' % (current_word, separator, total_count))
    except ValueError:
      # count was not a number, so silently discard this item
      pass

if __name__ == "__main__":
    main()
