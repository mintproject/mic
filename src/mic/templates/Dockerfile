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