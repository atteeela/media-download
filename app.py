#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Image Processing Service
A wrapper around GM commands for now
"""
from __future__ import (unicode_literals, print_function, division, absolute_import)
from future import standard_library
standard_library.install_aliases()
from builtins import *
from sh import youtube_dl
import helper as stackhut # user code imports

class YouTubeDLService:
    def getAudio(self, in_url):
        # run command
        resp = youtube_dl('-v', '-f', '140', '--add-metadata', '--restrict-filename', in_url)

        # find the downloaded file
        # look for line like this :: [download] Destination: Machinedrum_-_Center_Your_Love_Original_Mix-zp5jpAYeYI4.m4a
        prefix = "[download] Destination: "
        out_file = None
        for l in resp.splitlines():
            if l.startswith(prefix):
                out_file = l.split(prefix)[1]
                break

        # save file to S3
        out_url = stackhut.put_file(out_file)
        return out_url


SERVICES = {"Default": YouTubeDLService()}

