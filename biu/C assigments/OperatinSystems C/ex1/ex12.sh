#aviv shisman 206558157
#!/bin/bash

#entering the path in argument 1
cd $1

#printing all the directory's in the current directory (that we got in argument 1)
for d in */ ; do
	#removing the path from the name
	a="$d"
	b=$(basename $a)
	echo "$b" is directory
done

#printing all the files
for file in "$PWD"/*; do
	#if its a directory don't print it(skip the condition)
	if [ ! -d "$file" ]; then
		#removing the path from the name
		a="$file"
		b=$(basename $a)
		echo "$b" is file
	fi
done

 
