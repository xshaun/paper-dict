#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from urllib.request import urlopen
from pyquery import PyQuery as pyq
from io import StringIO
import re, os, sys, getopt

def pdf2text(pdf_file):
  rsrcmgr = PDFResourceManager()
  retstr = StringIO()
  laparams = LAParams()
  device = TextConverter(rsrcmgr, retstr, laparams=laparams)

  process_pdf(rsrcmgr, device, pdf_file)
  device.close()

  content = retstr.getvalue()
  retstr.close()
  return (content)

def text2words(text_string):
  # modify broken words.
  temp, number = re.compile(r'-\s{1}').subn('', text_string) 

  # convert chinese characters into english characters.
  temp, number = re.compile(r'’').subn('\'', temp)

  # eliminate characters which do not consist in words.
  temp, number = re.compile(r'[^a-zA-Z0-9\'-]').subn(' ', temp)

  # convert [blank,\t,\r,\n,\f,\v] into blank.
  temp, number = re.compile(r'\s+').subn(' ', temp)
  
  # process words individually and eliminate duplicates using set.
  rset = set()
  for word in temp.split(' '):
    # eliminate special chatacters located at either end
    word = word.strip('-').strip('\'')
    # eliminate pure number/single character/words over 20 characters
    if not re.compile(r'(^[0-9-]*$)|^.{1}$|^.{20,}$').match(word):
      rset.add(word.lower())
  
  result = list(rset)
  result.sort()
  return (result)

# structure of return value
# [
#   [keyword1, pronunciation1, explanation1],
#   [keyword2, explanation2],
#   [keyword3, pronunciation3],
#   ...
# ]
def consult_bing(words_list):
  result = []
  rset = set()
    
  for word in words_list:
    # response
    while True:
      try:
        doc = pyq(url=r'http://cn.bing.com/dict/search?q=' + word)
        break
      except:
        time.sleep(2)
        continue

    # DOM node of main content
    cts = doc('.content>.rs_area>.lf_area>.qdef')
    if not cts: continue

    # DOM node of searching word
    keyword = cts.find('.hd_area>#headword>h1>strong').text()
    if keyword in rset: continue
   
    # DOM node of word's pronunciation
    pronunciation = cts.find('.hd_area>.hd_tf_lh>.hd_p1_1').text()
    
    # DOM node of word's explanation
    explanation = []
    for e in cts.find('ul').children():
      e_pos = pyq(e).children('span.pos').text()
      e_def = pyq(e).children('span.def').text()
      explanation.append('[' + e_pos + ']' + e_def)

    rset.add(keyword)
    word_info = [ x for x in [keyword, pronunciation, explanation] if x ]
    #print (word_info)
    result.append(word_info)

  result.sort()
  return (result)

def main(argv):
  # argv
  input_pdf_file = ''
  try:
    opts, args = getopt.getopt(argv,"hi:",["ifile="])
  except getopt.GetoptError:
    print ('pdf2words.py -i <input_pdf_file>')
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
       print ('pdf2words.py -i <input_pdf_file>')
       sys.exit()
    elif opt in ("-i", "--ifile"):
       input_pdf_file = arg
  
  # if input is valid
  try:
    pdf_file = urlopen(input_pdf_file)
  except:
    try:
      location = 'file://' + os.path.abspath(input_pdf_file)
      pdf_file = urlopen(location)
    except:
      print (' invalid argv \'input_pdf_file\' ')
      sys.exit()

  # process
  text_string = pdf2text(pdf_file)
  words_list = text2words(text_string)
  #print (words_list)
  result = consult_bing(words_list)
  
  # show
  print ('sum: ', len(result))
  for record in result:
    for item in record:
      print (item)
    print ('---------------')

if __name__ == "__main__":
  main(sys.argv[1:])
