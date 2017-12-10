# Use debian:jessie as base image.
FROM debian:jessie

# allow replacing httpredir or deb mirror
#
# debian mirror list: 
#   - deb.debian.org
#   - mirrors.163.com
#   - mirrors.sohu.com
#   - ftp.debian.org
#   - ftp.tw.debian.org
#   - ftp.us.debian.org,
#   - debian.csie.ntu.edu.tw
#   
ARG APT_MIRROR=mirrors.163.com
RUN sed -ri "s/(httpredir|deb).debian.org/$APT_MIRROR/g" /etc/apt/sources.list

# Packaged dependencies
RUN apt-get update && apt-get install -y \
        python3 \
        python3-pip \
        curl \
        libxml2-dev \
        libxslt-dev \
        libzip-dev

# Download and Configure paper-dict.py
#
# pip mirror list: 
#   - pypi.python.org   (San Francisco, California US) default
#   - pypi.douban.com   (Beijing, Beijing CN)
#   - pypi.pubyun.com   (Changzhou, Jiangsu CN)
#   - pypi.fcio.net (Oberhausen, Nordrhein-Westfalen DE)
#   
ARG PIP_MIRROR=pypi.fcio.net
RUN curl -sSL https://github.com/xshaun/paper-dict/archive/master.tar.gz | tar -xzv \
    && cd paper-dict-master \
    && pip3 install --timeout=100 -i "https://$PIP_MIRROR/simple" -r requirements.txt \
    && chmod +x paper-dict.py \
    && ln -s paper-dict.py /bin/paper-dict

# Clean up APT when done.
RUN apt-get autoremove \
    && apt-get autoclean \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
