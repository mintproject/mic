#!/bin/bash
BASEDIR=$PWD
set +x
. .colors.sh
set -e
if [ ! -f outputs/out.csv ]; then
    echo -e "$(c R)[error] The model has not generated the output outputs/out.csv"
    exit 1
else
    echo -e "$(c G )[success] The model has generated the output outputs/out.csv"
    mv outputs/out.csv ${OUTPUTS1}
fi
