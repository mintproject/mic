mkdir outputs
touch outputs/out.csv
cat $1 
for i in $(cat $2); 
do 
	echo "writing: $3 + $i"
	echo `expr $3 + $i` >> outputs/out.csv; 
done
