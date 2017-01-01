#!/usr/bin/python3
# -*- coding: utf-8 -*-

from io import StringIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pyquery import PyQuery as pyq
from urllib.request import urlopen
import getopt
import logging 
import os
import re
import sys
import time

# DETAILS: resolve an issue (get warnings while running)
# 
# Pdfminer3k logs to the Python root logger unfortunately.
# It sets the root logger to level Error. 
#   This will stop PDFMiner warn logging, 
#   since it logs to the root logger, but not your own logging.
#   
# It sets propagation to False.
#   Because after PDFMiner usage, I had duplicate logging entries. 
#   This was caused by the root logger.
logging.propagate = False 
logging.getLogger().setLevel(logging.ERROR)


def pdf2text(pdf_file) :
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)

    process_pdf(rsrcmgr, device, pdf_file)
    device.close()

    content = retstr.getvalue()
    retstr.close()
    return (content)


def text2words(text_string) :
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
    for word in temp.split(' ') :
        # eliminate special chatacters at either end
        word = word.strip('-').strip('\'')

        # eliminate pure number/single-character/words-over-20-characters
        if not re.compile(r'(^[0-9-]*$)|^.{1}$|^.{20,}$').match(word) :
            rset.add(word)

    result = list(rset)
    result.sort()
    return (result)


# structure of return value
# {
#   'success_words' : [ word1, word2, ...],
#   'failure_words' : [ word1, word2, ...],
#   'success_words_info' :
#       [ 
#           [keyword1, pronunciation1, explanation1],
#           [keyword2, explanation2],
#           [keyword3, pronunciation3], 
#           ...
#       ]
# }
def consult_bing(words_list , ignore_words = set()) :
    success_words       = set()
    success_words_info  = []
    searching_words     = set(words_list) - ignore_words
    failure_words       = list(searching_words)

    for word in searching_words :
        # HTML response
        for i in range(5) :
            try : 
                doc = pyq(url=r'http://cn.bing.com/dict/search?q=' + word)
                failure_words.remove(word)
                break
            except :    # capture all exceptions
                time.sleep(2)
                continue
   
        # DOM node of effective content
        cts = doc('.content>.rs_area>.lf_area>.qdef')
        if not cts : continue

        # DOM node of searching word
        keyword = cts.find('.hd_area>#headword>h1>strong').text()
        if keyword in (success_words | ignore_words) : continue

        # DOM node of word's pronunciation
        pronunciation = cts.find('.hd_area>.hd_tf_lh>.hd_p1_1').text()

        # DOM node of word's explanation
        explanation = []
        for e in cts.find('ul').children():
            e_pos = pyq(e).children('span.pos').text()
            e_def = pyq(e).children('span.def').text()
            explanation.append('[' + e_pos + ']' + e_def)
        
        success_words.add(keyword)
        success_words_info.append( [ x for x in [keyword, pronunciation, explanation] if x ] )
    
    result = {
        'success_words' : list(success_words),
        'failure_words' : failure_words,
        'success_words_info' : success_words_info,
    }
    result['success_words'].sort()
    result['failure_words'].sort()
    result['success_words_info'].sort()

    return (result)

def main(argv) :
    # args
    UARGS = {
        'INPUT_PDF_PATH' : '' ,
        'IGNORE_WORDS_FILE_PATH' : '' ,
    }

    try :
        opts, args = getopt.getopt(argv, "hi:", ["help", "ifile=", "ignore="])
    except getopt.GetoptError as err :
        print (str(err))
        usage()
        sys.exit(2)
    for opt, arg in opts :
        if opt in ('-h', '--help') :
            usage()
            sys.exit()
        elif opt in ("-i", "--ifile") :
            UARGS['INPUT_PDF_PATH'] = arg
        elif opt in ("--ignore") :
            UARGS['IGNORE_WORDS_FILE_PATH'] = arg
        else :
            assert False, "unhandled option"

    # validity of input
    pdf_file = ''
    try :
        if re.compile(r'[a-zA-z]+://[^\s]*').match(UARGS['INPUT_PDF_PATH']) :
            pdf_file = urlopen(UARGS['INPUT_PDF_PATH'])
        else :
            pdf_file = open(os.path.abspath(UARGS['INPUT_PDF_PATH']), 'r')
    except :
        print ('Error: Invalid argv \'-i input_pdf_path\' ')
        sys.exit()
    
    ignore_words = set()
    if UARGS['IGNORE_WORDS_FILE_PATH'] :
        try :
            if re.compile(r'[a-zA-z]+://[^\s]*').match(UARGS['IGNORE_WORDS_FILE_PATH']) :
                ignore_words_file = urlopen(UARGS['IGNORE_WORDS_FILE_PATH'])
            else :
                ignore_words_file = open(os.path.abspath(UARGS['IGNORE_WORDS_FILE_PATH']))

            ignore_words = set(ignore_words_file.read().lower().split())

        except :
            print ('Error: Invalid argv \'-i input_pdf_path\' ')
            sys.exit()


    # process
    print ('converting pdf to text')
    text_string = pdf2text(pdf_file)
    print ('spliting text to words_list')
    words_list = text2words(text_string)
    print ('consulting a dictionary')
    result = consult_bing(words_list, ignore_words)
  
  #   'success_words' : [ word1, word2, ...],
#   'failure_words' : [ word1, word2, ...],
#   'success_words_info' :
#   
    # show
    print ('=================================>>>')
    print ('success_words:', len(result['success_words']), result['success_words'])
    print ('failure_words:', len(result['failure_words']), result['failure_words'])
    print ('success_words_info: ')
    for record in result['success_words_info'] :
        print ('---------------')
        for item in record :
            if isinstance(item, list) : 
                for l_item in item : print(l_item)
            else :
                print (item)
    print ('<<<=================================')


def usage() :
    print ('usage: pdf2words -i <input_pdf_path> [options]')
    print ('Options and arguments: ')
    print (' ' * 4, '-i : input_pdf_path; local relative path or url')
    print (' ' * 4, '--ignore : file path of ignore words list')
    pass

if __name__ == "__main__" :
    main(sys.argv[1:])
