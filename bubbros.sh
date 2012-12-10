#! /bin/sh

# Launcher for "The Bub's Brother"
#
# Copyright (C) 2007 by Siegfried Gevatter <siggi.gevatter@gmail.com>
#
# Released under the GNU General Public License, version 2 or later,
# see "/usr/share/common-licenses/GPL".

if [ -z $exec_file ]
then
	exec_file=/usr/share/bubbros/BubBob.py
fi

if [ ! -f $exec_file ]
then
	echo "Error! File \"$exec_file\" doesn't exist!"
	exit 1
fi

# Move to the directory where the script is
cd ${exec_file%/*}

python $exec_file $*
