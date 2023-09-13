#!/bin/bash

directory="/home/master/applications"  # The directory to search

#add the rule in the variable htaccess_rule
htaccess_rule="#this is a test
#this the second line
#this is the third line"

# Check the exit status
exit_status=$?

# Loop through the items in the directory
for item in "$directory"/*; do
    
    # Check if it's a directory and not a symlink
    if [ -d "$item" ] && [ ! -L "$item" ]; then 
        
        htaccess_file="${item}/public_html/.htaccess"
        
        #Outputs the application path in which the changes are being made
        echo -e "\033[32mAdding rule to this application:\033[31m$item\033[0m"

        echo -e "\n$htaccess_rule" >> "$htaccess_file"
        if [ $exit_status -eq 0 ]; then
        
        # Print "Success" in green
        echo -e "\033[32mSuccess\033[0m"
        
        else
        
        # Print "Failed" in red
        echo -e "\033[31mFailed\033[0m"
        
        fi
        
        else
        
        #Gives Warning message if the .htaccess file is not there.
        echo "Warning: .htaccess file not found for $item"
        
        fi

done
