#!/bin/sh

command -v virtualenv >/dev/null 2>&1 || { echo "Virtualenv not found. Aborting!
It is recommeded to run this program in a virtualenv, check how to install on your Operating System.
But if you want to install this program and all required packages on your root filesystem comment out this line inside this script and execute it again." >&2; exit 1; }

command -v pip >/dev/null 2>&1 || { echo "PIP not found. Aborting!
I require pip but it's not installed. Check how to install pip on your Operating System and after you install pip, execute this script again." >&2; exit 1; }


#
##
### Configure settings.py
### At the moment configuring only making_software's path at settings.py
##
#

# Get the path to this script, and by consequence, to making_software too.
SCRIPT_PATH="$( cd "$(dirname "$0")" ; pwd -P )"

# Get the parent dir of this script
PARENT_DIR="$(dirname "$SCRIPT_PATH")"
echo $PARENT_DIR

# Contains some values to append on the settings.py
OPENING_STRING="# -*- coding: utf-8 -*- \n\n
# Local configurations \n
# Making Software home folder 
# The folder where you unpack Making Software from Github 
# ie /home/your_name if you follow the tutorial to install
INTELIFORM_PERL_DIR = '$PARENT_DIR'\n 
"
#echo $OPENING_STRING

# Get the path to the django settings.py template file
echo "$SCRIPT_PATH/loopware/loopware/settings.template.py"
SETTINGS_PATH="$SCRIPT_PATH/loopware/loopware/settings.template.py"

# Get the content of the django settings.py template file
SETTINGS_TEMPLATE_FILE=`cat $SETTINGS_PATH`
#echo "$SETTINGS_TEMPLATE_FILE"


# Handle the complete content of the settings file
ULTIMATE_SETTINGS_CONTENT="$OPENING_STRING $SETTINGS_TEMPLATE_FILE"

# Create the settings.py file
touch "$SCRIPT_PATH/loopware/loopware/settings.py"

# Handle the path to the ultimante settings.py file
ULTIMATE_SETTINGS_FILE="$SCRIPT_PATH/loopware/loopware/settings.py"


#http://superuser.com/questions/246837/how-do-i-add-text-to-the-beginning-of-a-file-in-bash
echo "$ULTIMATE_SETTINGS_CONTENT" | cat - $ULTIMATE_SETTINGS_FILE> temp && mv temp "$ULTIMATE_SETTINGS_FILE"



#
##
### Install Ddjango Requirements
##
#

# Need to check wether pip is installed or not
# If not: apt-get install python-pip

# Gets pip path to install Django requirments 
PIP_PATH=`/usr/bin/which pip`
echo $PIP_PATH

# Install Django requirements
$PIP_PATH install -r "$SCRIPT_PATH/loopware/requirements.txt" 
