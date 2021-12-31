# This file is part of beets.
# Copyright 2016, Adrian Sampson.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

from beets.plugins import BeetsPlugin
import re

class ReplaceCharPlugin(BeetsPlugin):
    def __init__(self):
        super().__init__()
        self.config.add({
            'auto': True,
        })

        if self.config['auto']:
            self.register_listener("albuminfo_received", self.replace_special_chars)

    def replace_special_chars(self, info):
        for track in info.tracks:
            track.title = re.sub(r'’', '\'', track.title)
            track.title = re.sub(r'″', '"', track.title)