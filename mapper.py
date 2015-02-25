#!/usr/bin/env python
import sys

def main(separator='\t'):
  for line in sys.stdin:
    words = line.split()
    for word in words:
      sys.stdout.write(u'%s%s%d\n' % (word, separator, 1))

if __name__ == "__main__":
    main()
