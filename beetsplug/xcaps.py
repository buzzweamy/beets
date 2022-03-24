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

SPECIAL_QUOTES_PATTERN = r'[“″”]'
IMPROPER_CAPITALIZATION = r'(?<![\'\$\*])\b[a-z]+\b'
TRACK_FIELDS = ['title', 'artist', 'artist_credit', 'artist_sort']
ALBUM_FIELDS = ['artist', 'album']

def fix_case(m):
    as_list = list(m.string)
    temp = as_list[m.start():m.end()]
    temp[0] = temp[0].upper()
    fixed = "".join(temp)
    return fixed

def check_case_for_album(info):
    for field in ALBUM_FIELDS:
        info[field] = re.sub(IMPROPER_CAPITALIZATION, fix_case, info[field])

def check_case_for_track(track):
    for field in TRACK_FIELDS:
        track[field] = re.sub(IMPROPER_CAPITALIZATION, fix_case, track[field])

def replace_special_chars(str):
    str = re.sub(r'’', '\'', str)
    str = re.sub(SPECIAL_QUOTES_PATTERN, '"', str)
    return str

def replace_special_chars_for_album(info):
    for field in ALBUM_FIELDS:
        info[field] = replace_special_chars(info[field])

def replace_special_chars_for_track(track):
    for field in TRACK_FIELDS:
        track[field] = replace_special_chars(track[field])


class XCapsPlugin(BeetsPlugin):
    def __init__(self):
        super().__init__()
        self.config.add({
            'auto': True,
        })

        if self.config['auto']:
            self.register_listener("albuminfo_received", self.fix_titles)
        
    def fix_titles(self, info):
        replace_special_chars_for_album(info)
        check_case_for_album(info)
        for track in info.tracks:
            replace_special_chars_for_track(track)
            check_case_for_track(track)
