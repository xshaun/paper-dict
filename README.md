# pdf2words
>convert PDF to text, then split them into words, and consult online-directory through spiders(python script), finally build a vocabulary list.

---

1. How to use
  * [Traditional](#traditional)
    1. [Download pdf2words.py](#step1-download-pdf2wordspy)
    2. [Install dependency packages](#step2-install-dependency-packages)
    3. [Make it executable](#step3-make-it-executable)
    4. [Enjoy](#step4-enjoy)
  * [Docker](#docker)
    1. [Download pdf2words.py](#step1-download-pdf2wordspy-1)
    2. [Build Docker Image](#step2-build-docker-image)
    3. [Create a container](#step3-create-a-container)
    4. [Enjoy](#step4-enjoy-1)
2. [Features](#features)

## How to use

### Traditional

#### STEP1. Download pdf2words.py

git or downloader(wget, curl ...)
```Shell
$ git clone https://github.com/xshaun/pdf2words.git
# or
$ wget https://github.com/xshaun/pdf2words/archive/master.zip
# or
$ curl -sSL https://github.com/xshaun/pdf2words/archive/master.tar.gz | tar -xzv
```

#### STEP2. Install dependency packages

on ubuntu(debian):
```Shell
$ sudo apt-get install python3 python3-pip libxml2-dev libxslt-dev libzip-dev 
$ pip3 install pdfminer3k pyquery urllib3
```

#### STEP3. Make it executable

on ubuntu(other linux distribution):
```Shell
$ sudo chmod +x pdf2words.py
```

#### STEP4. Enjoy

local file:
```Shell
$ pdf2words.py -i ./<relative path>/target.pdf
```
remote file:
```Shell
$ pdf2words.py -i <URL path>/target.pdf
```

### Docker

#### STEP1. Download pdf2words.py

the same as above method

#### STEP2. Build Docker Image
>Run the command at directory which Dockerfile located at, And notice the last point in this command.   
>Or You can run it with `-f` option. 

```Shell
$ docker build -t pdf2words-img .
# or
$ docker build -t pdf2words-img -f <PATH/Dockerfile>
```

#### STEP3. Create a container

```Shell
$ docker run -it --name pdf2words-con pdf2words-img /bin/bash
# or
$ docker run -it -v /<host path>/PDF:/<container path>/pdf --name pdf2words-con pdf2words-img /bin/bash
```

#### STEP4. Enjoy

local file:
```Shell
root@019d28813cae:/# pdf2words -i ./<relative path>/target.pdf
```
remote file:
```Shell
root@019d28813cae:/# pdf2words -i <URL path>/target.pdf
```

## Features
- [x] support to convert local pdf-file and remote pdf-file.
- [x] support to consult online-bing dictionary.
- [x] support to filter words through ignore.txt.
- [x] support to multiple threads to speed up queries.
- [ ] support more spiders to consult more dictionaries.
- [ ] support local or cache dictionary.
- [x] support progress-bar.
