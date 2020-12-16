#!/bin/bash
echo " => Testing Whale"
python whale/manage.py test whale


if [ $? = 0 ]; then
    # Success: do stuff
    echo "Success."
else
    echo "FAILED."
    exit -1
fi