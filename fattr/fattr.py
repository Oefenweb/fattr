# -*- coding: utf-8 -*-

"""
"""

from __future__ import absolute_import
from __future__ import print_function

import hashlib
import io
import os
from queue import Queue

import xxhash

worker_queue = Queue()
"""
"""

file_attrs = {}
"""
"""


def md5_file(path, block_size=128 * 512):
    """
    :param path:
    :param block_size:
    :return:
    """

    hasher = hashlib.md5()
    with io.open(path, 'rb') as f_p:
        for chunk in iter(lambda: f_p.read(block_size), b''):
            hasher.update(chunk)

    return hasher.hexdigest()


def xxhash_file(path, block_size=128 * 512):
    """
    :param path:
    :param block_size:
    :return:
    """

    hasher = xxhash.xxh64()
    with io.open(path, 'rb') as f_p:
        for chunk in iter(lambda: f_p.read(block_size), b''):
            hasher.update(chunk)

    return hasher.hexdigest()


def save_files_attrs(i, w_q):
    """
    :param i:
    :param w_q:
    :return:
    """

    del i
    while True:
        path = w_q.get()

        file_basename = os.path.basename(path)
        file_attrs[file_basename] = save_file_attrs(path)

        w_q.task_done()


def save_file_attrs(path):
    """
    :param path:
    :return:
    """

    file_info = os.lstat(path)

    return {
        'mode': file_info.st_mode,
        'uid': file_info.st_uid,
        'gid': file_info.st_gid,
        # 'ctime' : file_info.st_ctime,
        'mtime': file_info.st_mtime,
        'atime': file_info.st_atime,
        'checksum': xxhash_file(path) if os.path.isfile(path) else None
    }


def restore_files_attrs(i, w_q):
    """
    :param i:
    :param w_q:
    :return:
    """

    del i
    while True:
        data = w_q.get()

        path = data['path']
        attrs = data['attrs']

        restore_file_attrs(path, attrs)

        w_q.task_done()


def restore_file_attrs(path, attrs):
    """
    :param path:
    :param attrs:
    :return:
    """

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
