#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Image Processing Service
A wrapper around GM commands for now
"""
import requests
import stackhut
from stackhut.stackhut import *  # user code imports

class YouTubeDLService:
    def __init__(self, task_id, bucket):
        self.task_id = task_id
        self.bucket = bucket

    def _run_command(self, cmd_list):
        # run command
        resp = call_strings(cmd_list, '')

        # find the downloaded file
        # look for line like this :: [download] Destination: Machinedrum_-_Center_Your_Love_Original_Mix-zp5jpAYeYI4.m4a
        prefix = "[download] Destination: "
        out_file = None
        for l in resp['stdout'].splitlines():
            if l.startswith(prefix):
                out_file = l.split(prefix)[1]
                break

        # save back to S3
        out_url = upload_file(out_file, self.task_id, self.bucket)
        return out_url

    def getAudio(self, in_url):
        return self._run_command(['youtube-dl', '-v', '-f', '140',
                                  '--add-metadata', '--restrict-filename', in_url])


if __name__ == "__main__":
    stack = Stack()
    stack.add_handler("YouTubeDL", YouTubeDLService(stack.task_id, stack.bucket))
    stack.run()
