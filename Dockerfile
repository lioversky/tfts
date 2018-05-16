FROM phusion/baseimage

ENV HOME /root
#CMD ["/sbin/my_init"]

RUN curl https://bootstrap.pypa.io/get-pip.py| python3
RUN pip3 install tensorflow \
    && pip3 install influxdb \
    && pip3 install numpy \
    && pip3 install scipy \
    && pip3 install matplotlib \
    && pip3 install python-etcd \
    && pip3 install pyyaml \
    && pip3 install apscheduler

ADD . /usr/python/


RUN rm -rf /etc/service/sshd /etc/my_init.d/00_regen_ssh_host_keys.sh
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

CMD ["python3 /opt/python/main.py"]