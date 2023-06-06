#!/bin/bash

directory="/home/master/applications"

#find "$directory" -maxdepth 1 -type d ! -path "$directory" -exec basename {} \; 
cd $directory

echo "Please enter the name you want to name the backup file in the destination folder"
read dest_name

for A in $(ls | awk '{print $NF}') 
do 
	echo $A 
       	cp $directory/$A/local_backups/backup.tgz $directory/$A/public_html/$dest_name
	echo "Backup file copied to public_html"
done
