#coding:utf-8
import os
import cStringIO
import gzip
import hashlib
import subprocess

from cactus.utils.helpers import checksum


class FakeTime:
    """
    Monkey-patch gzip.time to avoid changing files every time we deploy them.
    """
    def time(self):
        return 1111111111.111


def compressString(s):
    """Gzip a given string."""

    gzip.time = FakeTime()

    zbuf = cStringIO.StringIO()
    zfile = gzip.GzipFile(mode='wb', compresslevel=9, fileobj=zbuf)
    zfile.write(s)
    zfile.close()
    return zbuf.getvalue()


def fileSize(num):
    for x in ['b', 'kb', 'mb', 'gb', 'tb']:
        if num < 1024.0:
            return "%.0f%s" % (num, x)
        num /= 1024.0


def calculate_file_checksum(path):
    """
    Calculate the MD5 sum for a file (needs to fit in memory)
    """
    # with open(path, 'rb') as f:
    #     return checksum(f.read())
    output = subprocess.check_output(["md5", path])
    md5 = output.split(" = ")[1].strip()
    return md5

def file_changed_hash(path):
    info = os.stat(path)
    hashKey = str(info.st_mtime) + str(info.st_size)
    return checksum(hashKey)