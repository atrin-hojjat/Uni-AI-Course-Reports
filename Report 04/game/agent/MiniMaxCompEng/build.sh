#!/bin/sh

# gcc -std=c++17 -c $1.cpp
# gcc --shared -std=c++17 -Wall -Wextra -Wshadow -O2 -o $1 $1.o

echo "This method is depracated"
echo "Please use the following command instead"
echo
echo "python setup.py build"
echo

exit -1


g++ -std=c++17 --shared -Wall -Wextra -Wshadow -fPIC -o $1 $1.cpp
