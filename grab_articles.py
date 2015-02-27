#!/usr/bin/env python
import multiprocessing
import re
import sys
import time

import lxml.etree

NS_EXPORT = '{http://www.mediawiki.org/xml/export-0.9/}'

def read_file(filename, line_q):
  with open(filename, encoding='utf-8') as f:
    for line in f:
      line_q.put(line.encode('utf-8'))

def read_xml(line_q, text_q):
  parser = lxml.etree.XMLPullParser(tag='%spage' % NS_EXPORT)
  events = parser.read_events()
  while True:
    parser.feed(line_q.get())
    for _, elem in parser.read_events():
      title = elem.find('%stitle' % NS_EXPORT)
      if not title.text.startswith('Wikipedia:'):
        text = elem.find('%srevision/%stext' % (NS_EXPORT, NS_EXPORT))
        if text.text:
          text_q.put(
            lxml.etree.tostring(text, encoding='utf-8', xml_declaration=False))
      elem.clear()

def write_lines(text_q):
  while True:
    text = text_q.get()
    sys.stdout.buffer.write(text)
    sys.stdout.buffer.flush()
    text_q.task_done()

if __name__ == '__main__':
  filename = sys.stdin.readline().strip()

  line_q = multiprocessing.Queue()
  text_q = multiprocessing.JoinableQueue()

  read_file_p = multiprocessing.Process(
    target=read_file, args=(filename, line_q))
  read_file_p.start()

  read_xml_p = multiprocessing.Process(target=read_xml,
                                       args=(line_q, text_q))
  read_xml_p.daemon = True
  read_xml_p.start()

  write_lines_p = multiprocessing.Process(target=write_lines, args=(text_q,))
  write_lines_p.daemon = True
  write_lines_p.start()

  read_file_p.join()
  text_q.join()
  time.sleep(5)
