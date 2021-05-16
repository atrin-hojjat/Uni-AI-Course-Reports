# Description
This is othello game with minimax engine as computer player. The minimax algorithm also implements alpha-beta pruning, zobrist hashing, and cutoff.
A full report and description can be found on [here](https://github.com/atrin-hojjat/Uni-AI-Course-Reports/blob/main/Report%2004/Report/AUTthesis.pdf)(it's in persian);

# Trying it out
## Requirements
You'll need python(3.8/3.9) and g++/gcc with c++17. Python part also uses rich and numpy.

## Installation process
First, you need to create a python virtual envirnment(jfgi). After activating the virtual envirnment, install the dependency:
```bash
cd Report\ 04/game
python3 -m pip install -r requirements.txt
```
Then you need to build and install c++ minimax module:
```bash
cd agent/MiniMaxCompEngine
python3 setup.py build
python3 setup.py install
```

## Running
In the game directory, run `test01.py`, there you can select the board size and agents for each player.
```bash
python3 test01.py
```
Enjoy!
