#!/usr/bin/python3
from fabric.api import local
from time import strftime
from datetime import date
import os


def do_pack():
    """ A script that generates archive the contents of web_static folder"""

    filename = strftime("%Y%m%d%H%M%S")
    try:
        local("mkdir -p versions")
        local("tar -czvf versions/web_static_{}.tgz web_static/"
              .format(filename))
        filepath = f"versions/web_static_{filename}.tgz"
        filesize = os.path.getsize(filepath)
        print(f"web_static packed: {filepath} -> {filesize}Bytes")

        return "versions/web_static_{}.tgz".format(filename)

    except Exception as e:
        return None
