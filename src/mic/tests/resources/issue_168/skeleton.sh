rm -rf */.git
rm -rf mic/data
rm ./.reprozip-trace/trace.sqlite3
for i in $(find . -type f ! -path "*mic/mic.yaml*" ! -path "*.reprozip-trace/config.yml*" ! -name skeleton.sh ); do
    echo $i
    echo /dev/null > $i
done
