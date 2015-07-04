#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Media Download Service
A wrapper around youtube-dl commands for now
"""
from sh import youtube_dl
import stackhut  # user code imports

class MediaDownload:
    def get_filename(self, stdout, prefix):
        # find the downloaded file
        out_file = None
        for l in stdout.splitlines():
            if l.startswith(prefix):
                out_file = l.split(prefix)[1]
                break
        print("Output filename is {}".format(out_file))
        return out_file
    
    
    def getVideo(self, in_url):
        stdout = youtube_dl('-v', '--add-metadata', '--restrict-filename', in_url)
        prefix = "[ffmpeg] Merging formats into "
        out_file = self.get_filename(stdout, prefix)[1:-1] # strip quotes in filename
        return stackhut.put_file(out_file)

    def getAudio(self, in_url):
        stdout = youtube_dl('-v', '-x', '--add-metadata', '--restrict-filename', in_url)
        prefix = "[download] Destination: "
        out_file = self.get_filename(stdout, prefix)
        return stackhut.put_file(out_file)


SERVICES = {"Default": MediaDownload()}

