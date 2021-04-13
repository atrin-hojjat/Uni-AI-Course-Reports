#!/bin/sh

gcc -c $1.c
gcc --shared -o $1 $1.o

