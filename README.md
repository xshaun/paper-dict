# paper-dict
> This subject is to help students who are freshers of reading academic papers to consult unknown words and improve their English skills and reading paper skills.
> convert PDF to text, then split them into words, and consult online-directory through spiders(python script), finally build a vocabulary list and generate a pdf file.

---

1. How to use
  * [Traditional](#traditional)
    1. [Download paper-dict.py](#step1-download-paper-dictpy)
    2. [Install dependency packages](#step2-install-dependency-packages)
    3. [Make it executable](#step3-make-it-executable)
    4. [Enjoy](#step4-enjoy)
  * [Docker](#docker)
    1. [Download paper-dict.py](#step1-download-paper-dictpy-1)
    2. [Build Docker Image](#step2-build-docker-image)
    3. [Create a container](#step3-create-a-container)
    4. [Enjoy](#step4-enjoy-1)
2. [Features](#features)

## How to use

### Traditional

#### STEP1. Download paper-dict.py

git or downloader(wget, curl ...)
```Shell
$ git clone https://github.com/xshaun/paper-dict.git
# or
$ wget https://github.com/xshaun/paper-dict/archive/master.zip
# or
$ curl -sSL https://github.com/xshaun/paper-dict/archive/master.tar.gz | tar -xzv
```

#### STEP2. Install dependency packages

on ubuntu(debian):
```Shell
$ sudo apt-get install python3 python3-pip python3-reportlab libxml2-dev libxslt-dev libzip-dev
$ pip3 install --timeout=100 -r requirements.txt
```

#### STEP3. Make it executable

on ubuntu(other linux distribution):
```Shell
$ sudo chmod +x paper-dict.py
$ sudo chmod +x paper-dict-folder.sh
```

#### STEP4. Enjoy

local or remote pdf-file:
```Shell
$ paper-dict.py -i ./<relative path>/target.pdf -o <output.pdf> [-n ingore_words.txt]
# or
$ paper-dict.py -i <URL path>/target.pdf -o <output.pdf> [-n ingore_words.txt]
# or
$ paper-dict-folder <relative path>
```

### Docker

#### STEP1. Download paper-dict.py

the same as above method

#### STEP2. Build Docker Image
>Run the command at directory which Dockerfile located at, And notice the last point in this command.   
>Or You can run it with `-f` option.

```Shell
$ docker build -t paper-dict-img .
# or
$ docker build -t paper-dict-img -f <PATH/Dockerfile>
```

#### STEP3. Create a container

```Shell
$ docker run -it --name paper-dict-con paper-dict-img /bin/bash
# or
$ docker run -it -v <host path>:/<container path>/pdf --name paper-dict-con paper-dict-img /bin/bash
# or
$ docker run -it -v ~/:/pdf --name paper-dict-con paper-dict-img /bin/bash
```

#### STEP4. Enjoy

local or remote pdf-file:
```Shell
root@019d28813cae:/# paper-dict -i ./<relative path>/target.pdf -o <output.pdf> [-n ingore_words.txt]
# or
root@019d28813cae:/# paper-dict -i <URL path>/target.pdf -o <output.pdf> [-n ingore_words.txt]
# or
root@019d28813cae:/# paper-dict-folder <relative path>
```

## Features
- [x] support to convert local pdf-file and remote pdf-file.
- [x] support to consult online-bing dictionary.
- [x] support to filter words through ignore.txt.
- [x] support to multiple threads to speed up queries.
- [x] support progress-bar.
