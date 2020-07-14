FROM mintproject/generic:latest

RUN pip install reprozip mic
COPY entrypoint.sh /set_umask.sh
RUN chmod +x /set_umask.sh
ENTRYPOINT ["/set_umask.sh"]