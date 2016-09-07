# -*- coding: utf-8 -*-

"""
"""

from __future__ import absolute_import
import hashlib
import os
from Queue import Queue
from threading import Thread


worker_queue = Queue()
"""
"""

file_attrs = {}
"""
"""

def md5_file(path, block_size=128 * 256):
  """
  :param path:
  :param block_size:
  :return:
  """

  md5 = hashlib.md5()
  with open(path, 'rb') as f:
    for chunk in iter(lambda: f.read(block_size), b''):
      md5.update(chunk)

  return md5.hexdigest()


def collect_file_attrs(i, q):
  """
  :param i:
  :param q:
  :return:
  """

  while True:
    path = q.get()

    file_info = os.lstat(path)
    file_attrs[path] = {
      'mode' : file_info.st_mode,
      'uid' : file_info.st_uid,
      'gid' : file_info.st_gid,
      'ctime' : file_info.st_ctime,
      'mtime' : file_info.st_mtime,
      'atime' : file_info.st_atime,
      'md5' : md5_file(path) if os.path.isfile(path) else None
    }

    q.task_done()
