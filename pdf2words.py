#!/usr/bin/python3
# -*- coding: utf-8 -*-

from urllib.request import urlopen
import pdf2text as pt
import text2words as tw
import consult_bing as cb
import getopt
import re
import os
import sys

def main(argv) :
    
    Ga_input_pdf_path = ''
    Ga_ignore_words_file_path = ''

    Gv_input_pdf = ''
    Gv_ignore_words = set()
    Gv_ignore_words_file = ''

    # args
    try :
        opts, args = getopt.getopt(argv, "hi:n:", ["help", "ifile=", "ignore="])
    except getopt.GetoptError as err :
        print (str(err))
        usage(2)
    
    for opt, arg in opts :
        if opt in ('-h', '--help') :
            usage()
        elif opt in ("-i", "--ifile") :
            Ga_input_pdf_path = arg
        elif opt in ("-n","--ignore") :
            Ga_ignore_words_file_path = arg
        else :
            assert False, "unhandled option"

    # validity of input
    try :
        if re.compile(r'[a-zA-z]+://[^\s]*').match(Ga_input_pdf_path) :
            Gv_input_pdf = urlopen(Ga_input_pdf_path)
        else :
            Gv_input_pdf = open(os.path.abspath(Ga_input_pdf_path), 'rb')
    except :
        print ('Error: cannot open input_pdf. exc_info is ', sys.exc_info()[0])
        usage()

    if Ga_ignore_words_file_path :
        try :
            if re.compile(r'[a-zA-z]+://[^\s]*').match(Ga_ignore_words_file_path) :
                Gv_ignore_words_file = urlopen(Ga_ignore_words_file_path)
            else :
                Gv_ignore_words_file = open(os.path.abspath(Ga_ignore_words_file_path))

            Gv_ignore_words = set(Gv_ignore_words_file.read().lower().split())

        except :
            print ('Error: cannot open ignore_words_file. exc_info is ', sys.exc_info()[0])
            usage()     

    # process
    print ('converting pdf to text')
    text_string = pt.pdf2text(Gv_input_pdf)
    print ('spliting text to words_list')
    words_list = tw.text2words(text_string)
    print ('consulting a dictionary')
    result = cb.consult_bing(words_list, Gv_ignore_words)
    cb.show_bing(result)
    
    # close
    # Gv_input_pdf.close()
    # Gv_ignore_words_file.close()

def usage(exitcode = 0) :
    print ('Usage: pdf2words -i <input_pdf_path> [-n ignore_words] [-h]')
    print ('Detail options and arguments: ')
    print (' ' * 4, '-i / --ifile: input_pdf_path; local relative path or url')
    print (' ' * 4, '-n / --ignore : file path of ignore words list')
    print (' ' * 4, '-h / --help : print help info')
    sys.exit(exitcode)

if __name__ == "__main__" :
    main(sys.argv[1:])
