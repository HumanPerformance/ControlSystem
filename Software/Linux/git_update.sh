#!/bin/bash

# Define Username and Password
GIT_USERNAME="pd3dLab"
GIT_PASSWORD="pd3dLabatIST"

# store the current dir
CUR_DIR=$(pwd)

# Let the person running the script know what's going on.
echo -e "\n\033[1mPulling in latest changes for all repositories...\033[0m\n"

# Find all git repositories and update it to the master latest revision
for i in $(find . -name ".git" | cut -c 3-); do
	echo -e "";
    echo -e "\033[33m"+$i+"\033[0m";
    
    # Extract name of repo
    # Find everything between those delimeters
    j=$(echo $i | grep -o -P '(?<=/).*(?=/.git)');
    
    # Check whether or not we extracted the name of the directory
    if [[ $j = *"/"* ]]; then
        while [[ $j = *"/"* ]]; do
                j=$(echo $j | grep -o -P '(?<=/).*(?=)'); 
        done
    fi

    #echo $j;

    # We have to go to the .git parent directory to call the pull command
    cd "$i";
    cd ..;

    # finally pull
#    git pull origin master;
    git pull https://"$GIT_USERNAME":"$GIT_PASSWORD"@github.com/pd3d/"$j";

    # lets get back to the CUR_DIR
    cd $CUR_DIR
done

echo -e "\n\033[32mComplete!\033[0m\n"
