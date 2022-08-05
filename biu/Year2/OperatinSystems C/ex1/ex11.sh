#aviv shisman 206558157
#!/bin/bash

#entering the path in argument 1
cd $1

#setting var to 0 and counting the number of txt files in the dir
set x=0
for i in *.txt; do
    [ -f "$i" ] || break
    x=$[$x+1]
done

#printing
echo Number of files in the directory that end with .txt is $x
