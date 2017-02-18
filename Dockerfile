# our base image
FROM nbgallery/jupyter-alpine
MAINTAINER Kevin Kuhls <kekuhls@cisco.com>

# Install python and pip

RUN apk add --update python2-dev py2-pip openssl-dev libffi-dev musl-dev libxml2-dev libxslt-dev openssh gcc git\
    && pip install --upgrade pip \
    && pip install ansible requests jupyter xlrd lxml ncclient netaddr xmltodict jtextfsm netmiko\
    && mkdir -p ~/.ssh \
    && printf "StrictHostKeyChecking no\nHostKeyAlgorithms +ssh-dss\n" \\
        >> ~/.ssh/config \
    && chmod -R 600 ~/.ssh \
    && touch ~/.ssh/known_hosts \
    && git clone https://797e663cadd721fbdcf2cd0f9b23c5f05fb3e7a3@github.com/CiscoDevNet/ydk-py.git /home/docker/ydk-py \
    && cd /home/docker/ydk-py/core/ \
    && python setup.py sdist \
    && pip install dist/ydk*.gz \
    && cd /home/docker/ydk-py/ietf \
    && python setup.py sdist \
    && pip install dist/ydk*.gz \
    && rm -rf /home/docker/ydk-py/cisco-ios-xr/ \
    && sed -i '86,89 s/^/#/' /usr/lib/python2.7/site-packages/ydk/services/meta_service.py \
    && apk del --update gcc \
    && rm -rf /var/cache/apk/*

COPY devnet2449.ipynb /home/docker/

# Expose port 58888 
# from the container to the host
EXPOSE 58888/tcp

# https://github.com/ipython/ipython/issues/7062
ENTRYPOINT []
CMD ["/bin/sh", "-c", "/usr/bin/jupyter-notebook --port=58888 --no-browser --NotebookApp.token=''"]

WORKDIR /home/docker

# Notes, sed cmd is to comment out lines 86-89 until bug fix in
# /usr/lib/python2.7/site-packages/ydk/services/meta_service.py 

# to run use cmd
# docker run -it -p58888:58888 --rm -v$(pwd):/home/docker/ kuhlskev/ansible_ydk_jupyter