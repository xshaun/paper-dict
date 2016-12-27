# pdf2words
convert PDF to text , then split them into words , and consult words through python-spider

## How to use ?
**STEP1. Install python and relative libraries**

on ubuntu:

    sudo apt-get install python3.4 python3-pip
    pip install pdfminer urllib pyquery

**STEP2. Download pdf2words.py**

git or downloader(wget, curl ...)

    git clone https://github.com/xshaun/pdf2words.git
    or
    wget https://github.com/xshaun/pdf2words/archive/master.zip

**STEP3. Make it executable**

on ubuntu(other linux distribution):

    sudo chmod +x pdf2words.py

**STEP4. Enjoy**

local file:

    pdf2words.py -i ./\<relative path>/target.pdf

remote file:

    pdf2words.py -i \<URL path>/target.pdf

## Future Features ?
- support to filter words through ignore.txt.
- support to multiple threads to speed up queries.
- support more spiders to consult more dictionaries.
