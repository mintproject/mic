mkdir outputs
touch outputs/out.csv
for i in $(cat in.txt); 
do 
	echo "writing: $1 + $i"
	echo `expr $1 + $i` >> outputs/out.csv; 
done
