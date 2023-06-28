# -*- coding: utf-8 -*-

"""
"""

from __future__ import absolute_import
import hashlib
import os
from Queue import Queue


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


def save_files_attrs(i, q):
  """
  :param i:
  :param q:
  :return:
  """

  while True:
    path = q.get()

    file_basename = os.path.basename(path)
    file_attrs[file_basename] = save_file_attrs(path)

    q.task_done()


def save_file_attrs(path):
  file_info = os.lstat(path)

  return {
    'mode' : file_info.st_mode,
    'uid' : file_info.st_uid,
    'gid' : file_info.st_gid,
    # 'ctime' : file_info.st_ctime,
    'mtime' : file_info.st_mtime,
    'atime' : file_info.st_atime,
    'checksum' : md5_file(path) if os.path.isfile(path) else None
  }


def restore_files_attrs(i, q):
  """
  :param i:
  :param q:
  :return:
  """

  while True:
    data = q.get()

    path = data['path']
    attrs = data['attrs']

    restore_file_attrs(path, attrs)

    q.task_done()


def restore_file_attrs(path, attrs):
  if os.path.exists(path):
    mode = attrs['mode']
    uid = attrs['uid']
    gid = attrs['gid']
    # ctime = attrs['ctime']
    mtime = attrs['mtime']
    atime = attrs['atime']
    # checksum = attrs['checksum']

    os.chown(path, uid, gid)
    os.chmod(path, mode)

    if os.path.isfile(path):
      os.utime(path, (atime, mtime))
