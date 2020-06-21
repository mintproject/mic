#!/bin/bash
BASEDIR=$PWD
set +x
. .colors.sh
. $BASEDIR/io.sh {{ number_inputs }} {{ number_parameters }} {{number_outputs}} "$@"
set -e
{% for i in files -%}
if [ ! -f {{i}} ]; then
    echo -e "$(c R)[error] The model has not generated the output {{i}}"
    exit 1
else
    echo -e "$(c G )[success] The model has generated the output {{i}}"
    mv {{i}} ${OUTPUTS{{ loop.index  }}}
fi
{% endfor -%}
