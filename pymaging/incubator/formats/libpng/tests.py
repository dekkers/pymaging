# Copyright (c) 2012, Jonas Obrist
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the Jonas Obrist nor the
#      names of its contributors may be used to endorse or promote products
#      derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL JONAS OBRIST BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
from pymaging import Image
from pymaging.formats import registry
from pymaging.webcolors import Black, White
from . import LIBPNG
import os
import pymaging
import unittest

TESTDATA = os.path.join(os.path.dirname(pymaging.__file__), '..', 'testdata')


def _get_filepath(fname):
    return os.path.join(TESTDATA, fname)


class PNGTests(unittest.TestCase):
    def setUp(self):
        if LIBPNG not in registry.formats:
            registry.formats = [LIBPNG]
            registry.names = {}
            for extension in LIBPNG.extensions:
                registry.names[extension] = LIBPNG

    def test_indexed(self):
        img = Image.open_from_path(_get_filepath('black-white-indexed.png'))
        self.assertEqual(img.get_color(0, 0), Black)
        self.assertEqual(img.get_color(1, 1), Black)
        self.assertEqual(img.get_color(0, 1), White)
        self.assertEqual(img.get_color(1, 0), White)

    def test_non_indexed(self):
        img = Image.open_from_path(_get_filepath('black-white-non-indexed.png'))
        self.assertEqual(img.get_color(0, 0), Black)
        self.assertEqual(img.get_color(1, 1), Black)
        self.assertEqual(img.get_color(0, 1), White)
        self.assertEqual(img.get_color(1, 0), White)

    def test_non_indexed_interlaced(self):
        img = Image.open_from_path(_get_filepath('black-white-non-indexed-interlaced-adam7.png'))
        self.assertEqual(img.get_color(0, 0), Black)
        self.assertEqual(img.get_color(1, 1), Black)
        self.assertEqual(img.get_color(0, 1), White)
        self.assertEqual(img.get_color(1, 0), White)

    def test_with_transparency(self):
        img = Image.open_from_path(_get_filepath('black-white-with-transparency.png'))
        self.assertEqual(img.get_color(0, 0), Black)
        self.assertEqual(img.get_color(1, 0), White)
        self.assertEqual(img.get_color(1, 1), Black.get_for_brightness(0.5))
        self.assertEqual(img.get_color(0, 1), White.get_for_brightness(0.5))
