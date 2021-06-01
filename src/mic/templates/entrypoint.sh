#!/bin/bash
umask 0000
bash /bin/mic_install.sh
find . -type f -print0 | xargs -0 dos2unix &> /dev/null
/bin/bash
