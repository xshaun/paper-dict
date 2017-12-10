#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pdf2text as pt
import os
import re
import sys


def text2words(text_string):
    # rectify words having a break.
    temp, number = re.compile(r'-\s{1}').subn('', text_string.lower())

    # convert chinese characters into english characters.
    temp, number = re.compile(r'’').subn('\'', temp)

    # eliminate characters not consisting in words.
    temp, number = re.compile(r'[^a-zA-Z0-9\'-]').subn(' ', temp)

    # convert [blank,\t,\r,\n,\f,\v] into blank.
    temp, number = re.compile(r'\s+').subn(' ', temp)

    # process words individually and remove redundancy by set.
    rset = set()
    for word in temp.split(' '):
        # eliminate special chatacters at either end
        word = word.strip('-').strip('\'')

        # eliminate pure number/single-character/words-over-20-characters
        if not re.compile(r'(^[0-9-]*$)|^.{1}$|^.{20,}$').match(word):
            rset.add(word)

    result = list(rset)
    result.sort()
    return (result)

# TEST
if __name__ == "__main__":
    try:
        # Local File
        pdf_file = open(os.path.abspath(
            './tests/test_python_overview.pdf'), 'rb')
        pdf_text = pt.pdf2text(pdf_file)
        words = text2words(pdf_text)
        print(words)
        pdf_file.close()
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise
