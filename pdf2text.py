#!/usr/bin/python3
# -*- coding: utf-8 -*-

from io import StringIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from urllib.request import urlopen
import logging 
import os
import sys

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

# TEST
if __name__ == "__main__" :
    try :
        # Remote File
        pdf_file = urlopen('https://www.tutorialspoint.com/python/pdf/python_overview.pdf')
        pdf_text = pdf2text( pdf_file )
        print (pdf_text)
        pdf_file.close()

        # Local File
        pdf_file = open(os.path.abspath('./test/test_python_overview.pdf'), 'rb')
        pdf_text = pdf2text(pdf_file)
        print (pdf_text)
        pdf_file.close()
    except :
        print("Unexpected error:", sys.exc_info()[0])
        raise
