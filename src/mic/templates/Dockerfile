FROM {{ language.image }}

{% if "generic" in language.label  -%}
#If you put an executable in the bin directory, uncomment the next file
#ADD bin/* /usr/bin/
{% endif -%}

COPY entrypoint.sh /set_umask.sh

{% if os -%}
{% if os == "windows"-%}
RUN echo "Converting line endings"
RUN sed -i 's/\r//' set_umask.sh
{% endif -%}
{% endif -%}

ADD https://data.mint.isi.edu/files/install.sh /bin/mic_install.sh

RUN chmod +x /set_umask.sh
ENTRYPOINT ["/set_umask.sh"]

