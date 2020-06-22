mkdir outputs
for i in $(cat c.txt); do echo $i > outputs/$i; done
