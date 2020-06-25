#!/bin/bash
BASEDIR=$PWD
set +x
. .colors.sh
set -e
if [ ! -f result.txt ]; then
    echo -e "$(c R)[error] The model has not generated the output result.txt"
    exit 1
else
    echo -e "$(c G )[success] The model has generated the output result.txt"
    mv result.txt ${OUTPUTS1}
fi
