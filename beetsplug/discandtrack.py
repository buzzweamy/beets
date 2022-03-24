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

class MyPlugin(BeetsPlugin):
    def __init__(self):
        super(MyPlugin, self).__init__()
        self.template_fields['disc_and_track'] = _tmpl_disc_and_track

def _tmpl_disc_and_track(item):
    """Expand to the disc number and track number if this is a
    multi-disc release. Otherwise, just expands to the track
    number.
    """
    if item.disctotal > 1:
        return u'%02i - %02i' % (item.disc, item.track)
    else:
        return u'%02i' % (item.track)