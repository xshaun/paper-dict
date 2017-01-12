#!/usr/bin/python3
# -*- coding: utf-8 -*-

from pyquery import PyQuery as pyq
import time

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
def consult_bing(words_list, ignore_words = set()) :
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

def show_bing (result) :
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


# TEST
if __name__ == "__main__" :
    words_list = ['abc', 'above-mentioned', 'activex', 'actua', 'add', 'an', 'and', 'apart', 'applications', 'are', 'as', 'at', 'automatic', 'ava', 'be', 'before', "beginner's", 'beginner-leve', 'better', 'big', 'broad', 'browsers', 'building', 'bulk', 'by', 'byte-code', 'ca', 'can', 'checking', 'with', 'within', 'write', 'www', 'you', 'your']

    result = consult_bing( words_list)
    show_bing(result)
