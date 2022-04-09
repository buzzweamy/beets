# This file is part of beets.
# Copyright 2016, Blemjhoo Tezoulbr <baobab@heresiarch.info>.
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

"""Moves patterns in path formats (suitable for moving articles)."""


import re
from beets.plugins import BeetsPlugin

class CleanAlbumPathPlugin(BeetsPlugin):

    def __init__(self):
        super().__init__()
        self.config.add({
            'auto': True,
        })

        self.template_funcs['clean_album_path'] = self.the_template_func

    def the_template_func(self, text):
        if text:
            sanitized = re.sub(r'[\\\/\:\"\|\?\>\<\*]', ' ', text).rstrip()
            sanitized = re.sub(r'\.$', '', sanitized)
            return sanitized
        else:
            return ''
