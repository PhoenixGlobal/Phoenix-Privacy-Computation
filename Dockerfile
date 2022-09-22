FROM phoenixglobal/ubuntu

ADD . /home/Phoenix-Privacy-Computation

RUN apt install unzip

RUN pip3 --no-cache-dir install -r /home/Phoenix-Privacy-Computation/requirements.txt --user -i https://mirrors.aliyun.com/pypi/simple/

RUN cd /home && unzip Rosetta.zip && cd Rosetta && ./rosetta.sh install