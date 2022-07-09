#!/bin/sh
target_files=$(find . -name "*.sql")
for file in $target_files
do
    $(sql-formatter --output $file $file)
done
echo format check completed.