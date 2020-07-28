FROM {{ language.image }}

{% if "generic" in language.label  -%}
#If you put an executable in the bin directory, uncomment the next file
#ADD bin/* /usr/bin/
{% endif -%}
COPY entrypoint.sh /set_umask.sh
RUN chmod +x /set_umask.sh
ENTRYPOINT ["/set_umask.sh"]
