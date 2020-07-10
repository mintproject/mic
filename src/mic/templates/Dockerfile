FROM {{ language.image }}

ARG UNAME=mic
ARG UID=1000
ARG GID=1000
RUN groupadd -g $GID -o $UNAME
RUN useradd -m -u $UID -g $GID -o -s /bin/bash $UNAME
USER $UNAME

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
RUN pip install reprozip mic --no-warn-script-location
ENV PATH="/home/mic/.local/bin:${PATH}"
ENTRYPOINT []