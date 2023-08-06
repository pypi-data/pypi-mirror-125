# -*- coding=utf-8 -*-
r"""
MIT License

Copyright (c) 2021 PlayerG9

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""
import os
import pathlib
import difflib


__author__ = "PlayerG9"
__copyright__ = "Copyright 2021, PlayerG9"
__credits__ = ["PlayerG9"]
__license__ = "MIT"
__version_info__ = (0,1,0)
__version__ = '.'.join(str(_) for _ in __version_info__)
__maintainer__ = "PlayerG9"
__email__ = None
__status__ = "Prototype"  # Prototype, Development, Production


class BadPath(Exception):
    def __init__(self, text: str, orig: BaseException):
        super().__init__(text)
        self.original = orig


def findpath(path: str, ratio: float = 0.7) -> str:
    path = pathlib.Path(path)
    current = pathlib.Path(path.root)
    try:
        for part in path.parts:
            if path.drive and part.startswith(path.drive):  # prevent error that occurs with abs-path
                continue
            filenames = os.listdir(current)
            sequs = [(fn, difflib.SequenceMatcher(None, part, fn)) for fn in filenames]
            sequs.sort(key=lambda e: e[1].ratio(), reverse=True)
            better, sequ = sequs[0]
            if sequ.ratio() < ratio:
                raise ValueError('to less ratio')
            current /= better
        return os.path.abspath(current)
    except Exception as error:
        raise BadPath(f'{error.__class__} {error}', error)
