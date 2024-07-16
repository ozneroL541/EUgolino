#!/bin/bash
#
#   file name: script.sh
#   author: Lorenzo Radice
#

# Main file to execute
main="./main.py"
# Logs directory
log_dir="logs/"
# Output Logs File
outlog="output.log"
# Error Logs File
errlog="error.log"
# Time Logs File
timelog="time.log"


#tree

echo "--------------------"
# Make destination directory
mkdir -p $log_dir
# Run the main.py script
echo "((time ($main 1>> $log_dir$outlog 2>> $log_dir$errlog)) &>> $log_dir$timelog) &"
((time ($main 1>> $log_dir$outlog 2>> $log_dir$errlog)) &>> $log_dir$timelog) &
# End
echo "--------------------"
#tree
