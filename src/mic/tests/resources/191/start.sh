files=$(ls files)
mkdir outputs
for i in $files; do
    echo $i > outputs/$i
done
