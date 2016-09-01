#!/bin/sh

ls -l lock | cut -d' ' -f9-11
for t in $@ ; do
	echo -n "$t: l-standard-"
	LD_LIBRARY_PATH=. ./kccachetest wicked -th $t 100000 | grep time
	if ! [ $? -eq 0 ]; then
		echo "ERROR OCCURED: $?"
	fi
done
echo
