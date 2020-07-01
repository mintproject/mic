#!/bin/bash
BASEDIR=$PWD
set +x
. .colors.sh
set -e
if [ ! -f outputs/b.txt ]; then
    echo -e "$(c R)[error] The model has not generated the output outputs/b.txt"
    exit 1
else
    echo -e "$(c G )[success] The model has generated the output outputs/b.txt"
    mv outputs/b.txt ${OUTPUTS1}
fi
if [ ! -f outputs/c.txt ]; then
    echo -e "$(c R)[error] The model has not generated the output outputs/c.txt"
    exit 1
else
    echo -e "$(c G )[success] The model has generated the output outputs/c.txt"
    mv outputs/c.txt ${OUTPUTS2}
fi
if [ ! -f outputs/a.txt ]; then
    echo -e "$(c R)[error] The model has not generated the output outputs/a.txt"
    exit 1
else
    echo -e "$(c G )[success] The model has generated the output outputs/a.txt"
    mv outputs/a.txt ${OUTPUTS3}
fi
