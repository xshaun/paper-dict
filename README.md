# pdf2words
convert PDF to text , then split them into words , and consult words through python-spider

## How to use ?
**STEP1. Install python and relative libraries**

on ubuntu:
```bash
$ sudo apt-get install python3 python3-pip libxml2-dev libxslt-dev libzip-dev 
$ pip3 install pdfminer3k pyquery urllib3
```

**STEP2. Download pdf2words.py**

git or downloader(wget, curl ...)
```bash
$ git clone https://github.com/xshaun/pdf2words.git
# or
$ wget https://github.com/xshaun/pdf2words/archive/master.zip
# or
$ curl -sSL https://github.com/xshaun/pdf2words/archive/master.tar.gz | tar -xzv
```

**STEP3. Make it executable**

on ubuntu(other linux distribution):
```bash
$ sudo chmod +x pdf2words.py
```

**STEP4. Enjoy**

local file:
```bash
$ pdf2words.py -i ./<relative path>/target.pdf
```
remote file:
```bash
$ pdf2words.py -i <URL path>/target.pdf
```

## Future Features ?
- support to filter words through ignore.txt.
- support to multiple threads to speed up queries.
- support more spiders to consult more dictionaries.
- support local or cache dictionary.
