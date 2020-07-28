FROM {{ language.image }}

{% if "python3" in language.label  -%}
ADD requirements.txt /tmp/requirements.txt
RUN pip3 install -U pip
RUN pip3 install -r /tmp/requirements.txt

{% endif -%}

{% if "conda" in language.label  -%}
ADD environment.yml /tmp/environment.yml
RUN conda env update -f /tmp/environment.yml

{% endif -%}

{% if "generic" in language.label  -%}
#If you put an executable in the bin directory, uncomment the next file
#ADD bin/* /usr/bin/
{% endif -%}

COPY entrypoint.sh /set_umask.sh

{% if os -%}
{% if os == "windows"-%}
COPY dos2unix.sh /d2u.sh
RUN chmod +x /d2u.sh
RUN bash -c "./d2u.sh set_umask.sh"
{% endif -%}
{% endif -%}


RUN chmod +x /set_umask.sh
ENTRYPOINT ["/set_umask.sh"]

