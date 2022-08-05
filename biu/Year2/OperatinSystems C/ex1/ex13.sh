#aviv shisman 206558157
#!/bin/bash


flag=0

#check number of args
if [ "$#" -ne 1 ]; then
    echo "Illegal number of parameters"
    flag=1
fi

#check if file exist
if [ ! -f "$1" ] && [ "$flag" -eq "0" ]; then
    echo "error: there is no such file"
    flag=1
fi

#check if dir exists
if [ ! -d "dir_rm_safe" ]&& [ "$flag" -eq "0" ]; then
	mkdir "dir_rm_safe"
fi

#copy & remove
if [ "$flag" -eq "0" ]; then
	cp "$1" "dir_rm_safe"
	rm "$1"
	echo "done!"
fi
