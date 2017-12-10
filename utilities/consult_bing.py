#!/usr/bin/python3
# -*- coding: utf-8 -*-

from pyquery import PyQuery as pyq
import threading
import time

# Global variables
success_words = set()
success_words_info = list()
failure_words = set()
ignore_words = set()
searching_words = set()
threadLock_sw = threading.Lock()
threadLock_swi = threading.Lock()
threadLock_fw = threading.Lock()


class WordThread (threading.Thread):

    def __init__(self, threadID, name, word):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.word = word

    def run(self):
        #print ("start thread:" + self.name)
        search_bing(self.word)
        #print ("end thread: " + self.name)
        print("\rPercent: %.2f %% [not 100%% is ok, ignoring transformation ]" % (
            len(success_words | failure_words) / len(searching_words) * 100), end="")


def search_bing(word):
    global success_words
    global success_words_info
    global failure_words
    global ignore_words
    global searching_words
    global threadLock_sw
    global threadLock_swi
    global threadLock_fw

    # HTML response
    for i in range(5):
        try:
            doc = pyq(url=r'http://cn.bing.com/dict/search?q=' + word)
            break
        except:    # capture all exceptions
            time.sleep(3)
            continue

    # DOM node of effective content
    cts = doc('.content>.rs_area>.lf_area>.qdef')
    if not cts:
        threadLock_fw.acquire()
        failure_words.add(word)
        threadLock_fw.release()
        return

    # DOM node of searching word
    keyword = cts.find('.hd_area>#headword>h1>strong').text()
    if keyword in (success_words | ignore_words):
        return

    # DOM node of word's pronunciation
    pronunciation = cts.find('.hd_area>.hd_tf_lh>.hd_p1_1').text()

    # DOM node of word's explanation
    explanation = []
    for e in cts.find('ul').children():
        e_pos = pyq(e).children('span.pos').text()
        e_def = pyq(e).children('span.def').text()
        explanation.append('[' + e_pos + ']' + e_def)

    threadLock_sw.acquire()
    success_words.add(keyword)
    threadLock_sw.release()

    threadLock_swi.acquire()
    success_words_info.append(
        [x for x in [keyword, pronunciation, explanation] if x])
    threadLock_swi.release()

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


def consult_bing(words_list, ignore_words_set=set()):
    global success_words
    global success_words_info
    global failure_words
    global ignore_words
    global searching_words

    searching_words |= set(words_list) - ignore_words_set
    ignore_words |= ignore_words_set

    threads = []
    for index, item in enumerate(searching_words):
        thread = WordThread(index, 'searching ' + item, item)
        thread.start()
        threads.append(thread)

    for t in threads:
        t.join()

    result = {
        'success_words': list(success_words),
        'failure_words': list(failure_words),
        'success_words_info': success_words_info,
    }
    result['success_words'].sort()
    result['failure_words'].sort()
    result['success_words_info'].sort()

    return (result)


def show_bing(result):
    print('\n=================================>>>')
    print('success_words:', len(
        result['success_words']), result['success_words'])
    print('failure_words:', len(
        result['failure_words']), result['failure_words'])
    print('success_words_info:', len(result['success_words_info']))
    for record in result['success_words_info']:
        print('---------------')
        for item in record:
            if isinstance(item, list):
                for l_item in item:
                    print(l_item)
            else:
                print(item)
    print('<<<=================================')


# TEST
if __name__ == "__main__":
    words_list = ['abc', 'above-mentioned', 'activex', 'actua', 'add', 'an', 'and', 'apart', 'applications', 'are', 'as', 'at', 'automatic', 'ava', 'be', 'before', "beginner's",
                  'beginner-leve', 'better', 'big', 'broad', 'browsers', 'building', 'bulk', 'by', 'byte-code', 'ca', 'can', 'checking', 'with', 'within', 'write', 'www', 'you', 'your']
    result = consult_bing(words_list)
    show_bing(result)
