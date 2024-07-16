#!/bin/bash
#
#   file name: script.sh
#   author: Lorenzo Radice
#

# Main file to execute
main="./main.py"
# Logs directory
log_dir="logs/"
# Time Logs File
timelog="time.log"

# Make destination directory
mkdir -p $log_dir
# Run the main.py script
echo "((time ($main) &>> $log_dir$timelog) &"
((time $main) &>> $log_dir$timelog) &
