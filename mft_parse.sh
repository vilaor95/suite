#!/bin/bash

cat $1 | grep -v 'Corrupt' | grep -v 'NoParent'     | awk -F, '{print $8","$9","$10","$11","$12","$13","$14","$15","$16","$    54}' | sed 's/"//g'
