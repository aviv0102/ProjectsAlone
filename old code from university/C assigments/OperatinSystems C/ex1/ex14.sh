#aviv shisman 206558157
#!/bin/bash




#check number of args
if [ "$#" -ne 2 ]; then
    echo "Illegal number of parameters"

fi

    #awk '{print $1}' "$2"
    
#reading from the file...
sum=0
while IFS='' read -r line || [[ -n "$line" ]]; do
 	#get the first two words of each line
	word1=$(echo "$line" | cut -d" " -f1)
	word2=$(echo "$line" | cut -d" " -f2)
	word=$word1$" "$word2
	#checking if its the matching person-> if it is print this line and add to sum
	if [ "$word" == "$1" ]; then
		echo "$line"
		amount=$(echo "$line" | cut -d" " -f3)
		sum=$[$sum+$amount]
	fi
    	
    
done < "$2"
#print total balance
echo Total balance: $sum 
