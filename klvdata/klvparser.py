#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# The MIT License (MIT)
#
# Copyright (c) 2016 Matthew Pare (paretech@gmail.com)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from io import BytesIO
from io import IOBase
from klvdata.common import bytes_to_int


class KLVParser(object):
    """Return key, value pairs parsed from an SMPTE ST 336 source."""

    def __init__(self, source, key_length):
        if isinstance(source, IOBase):
            self.source = source
        else:
            self.source = BytesIO(source)

        self.key_length = key_length

    def __iter__(self):
        return self

    def __next__(self):
        key = self.__read(self.key_length)

        byte_length = bytes_to_int(self.__read(1))

        if byte_length < 128:
            # BER Short Form
            length = byte_length
        else:
            # BER Long Form
            length = bytes_to_int(self.__read(byte_length - 128))
        value = self.__read(length)

        return key, value

    def __read(self, size):
        if size == 0:
            return b""

        assert size > 0

        if size > 2 ** 32:
            return b""

        data = self.source.read(size)

        if data:
            return data
        else:
            raise StopIteration
