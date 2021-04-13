#include <cstring>
#include <math.h>
#include <iostream>
#include <unordered_map>
#include <stack>
#include <vector>
#include <random>

using namespace std;

#if defined(_MSC_VER)
    //  Microsoft 
    #define EXPORT __declspec(dllexport)
    #define IMPORT __declspec(dllimport)
#elif defined(__GNUC__)
    //  GCC
    #define EXPORT __attribute__((visibility("default")))
    #define IMPORT
#else
    //  do nothing and hope for the best?
    #define EXPORT
    #define IMPORT
    #pragma warning Unknown dynamic link import/export semantics.
#endif


struct ChangedSegment {
	int is, ie, js, je, idir, jdir;
	unsigned long long int prvHash;
	int prvColor, curColor;
};

struct PreCalcData {
	int value, depth;
	pair<int, int> bestMove;
};

const int MaxN = 20;
const int inf = 1e9 + 7;
const int STATES = 3;
unsigned long long int zobristTable[MaxN][MaxN][STATES];
unordered_map<unsigned long long int, PreCalcData> preCalc[STATES];
stack<ChangedSegment> moves;
mt19937 mt_rand;


unsigned long long randomGenerator() {
	uniform_int_distribution<unsigned long long int> dist(0, UINT64_MAX);

	return dist(mt_rand);
}


void printGrid(const int N, int **grid) {
	cout << endl << endl;
	for(int i = 0; i < N; i++, cout << endl)
		for(int j = 0; j < N; j++)
			cout << grid[i][j];
	cout << endl;
}

void generateZobristValues(int N) {
	for(int i = 0; i < N; i++)
		for(int j = 0; j < N; j++)
			for(int s = 0; s < STATES; s++)
				zobristTable[i][j][s] = randomGenerator();
}

unsigned long long int generateHash(const int N, int **grid) {
	unsigned long long int val = 0;
	for(int i = 0; i < N; i++)
		for(int j = 0; j < N; j++)
			val ^= zobristTable[i][j][grid[i][j]];
	return val;
}

int evaluate(const int N, int **grid, int player) {
	int val = 0;
	for(int i = 0; i < N; i++) 
		for(int j = 0; j < N; j++)
			val += (1 - __builtin_popcount(player ^ grid[i][j]));
	return val;
}

vector<pair<int, int>> getPossibleMoves(const int N, int **grid, int player) {
	vector<pair<int, int>> ret;
	for(int i = 0; i < N; i++) 
		for(int j = 0; j < N; j++) {
			if(grid[i][j] != 0) 
				continue;
			bool ok = false;
			for(int dir = -1; !ok && dir < 2; dir += 2) {
				for(int jp = j + dir; !ok && jp > -1 && jp < N; jp += dir) {
					if(grid[i][jp] == 0) 
						break;
					if(grid[i][jp] == player) {
						ok = abs(jp - j) > 1;
						break;
					}
				}
				for(int ip = i + dir; !ok && ip > -1 && ip < N; ip += dir) {
					if(grid[ip][j] == 0) 
						break;
					if(grid[ip][j] == player) {
						ok = abs(ip - i) > 1;
						break;
					}
				}
			}
			for(int id = -1; !ok && id < 2; id += 2) 
				for(int jd = -1; !ok && jd < 2; jd += 2) 
					for(int k = 1; k < N; k++) {
						if(i + id * k < 0 || i + id * k >= N)
							break;
						if(j + jd * k < 0 || j + jd * k >= N)
							break;

						int ip = i + id * k;
						int jp = j + jd * k;

						if(grid[ip][jp] == 0)
							break;
						if(grid[ip][jp] == player) {
							ok = k > 1;
							break;
						}
					}
			if(ok) 
				ret.push_back({i, j});
		}
	return ret;

}

unsigned long long int makeMove(const int N, int **grid, int player, 
		pair<int, int> selectedMove, unsigned long long int curHash) {
	int i = selectedMove.first, j = selectedMove.second;
	vector<ChangedSegment> changes;

	changes.push_back({i, i + 1, j, j + 1, 0, 1, curHash, 0, player});


	for(int dir = -1; dir < 2; dir += 2) {
		for(int jp = j + dir; jp > -1 && jp < N; jp += dir) {
			if(grid[i][jp] == 0) 
				break;
			if(grid[i][jp] == player) {
				if(abs(jp - j) > 1) {
					ChangedSegment chngd;
					if(jp < j) 
						chngd = {i, i + 1, jp + 1, j, 0, 1, curHash, 3 ^ player, player};
					else
						chngd = {i, i + 1, j + 1, jp, 0, 1, curHash, 3 ^ player, player};
					changes.push_back(chngd);
				}
				break;
			}
		}
		for(int ip = i + dir; ip > -1 && ip < N; ip += dir) {
			if(grid[ip][j] == 0) 
				break;
			if(grid[ip][j] == player) {
				if(abs(ip - i) > 1) {
					ChangedSegment chngd;
					if(i < ip)
						chngd = {i + 1, ip, j, j + 1, 0, 1, curHash, 3 ^ player, player};
					else
						chngd = {ip + 1, i, j, j + 1, 0, 1, curHash, 3 ^ player, player};
					changes.push_back(chngd);
				}
				break;
			}
		}
	}
	for(int id = -1; id < 2; id += 2) 
		for(int jd = -1; jd < 2; jd += 2) 
			for(int k = 1; k < N; k++) {
				if(i + id * k < 0 || i + id * k >= N)
					break;
				if(j + jd * k < 0 || j + jd * k >= N)
					break;

				int ip = i + id * k;
				int jp = j + jd * k;

				if(grid[ip][jp] == 0)
					break;
				if(grid[ip][jp] == player) {
					if(k > 1) {
						ChangedSegment chngd = {i, ip, j, jp, id, jd, curHash, 3 ^ player, player};
						changes.push_back(chngd);
					}
					break;
				}
			}

	unsigned long long int newHash = curHash;
	
	for(auto change : changes) {
		moves.push(change);
		int dist = max(abs(change.ie - change.is), abs(change.je - change.js));
		for(int k = 0; k < dist; k++) {
			int ip = change.is + k * change.idir;
			int jp = change.js + k * change.jdir;

			newHash ^= zobristTable[ip][jp][change.prvColor] ^ 
				zobristTable[ip][jp][change.curColor];
			grid[ip][jp] = change.curColor;
		}
	}
	return newHash;
}

void undoMoves(const int N, int **grid, int player, unsigned long long int desHash) {
	while(moves.size() && moves.top().prvHash == desHash) {
		auto change = moves.top();
		moves.pop();
		
		int dist = max(abs(change.ie - change.is), abs(change.je - change.js));
		for(int k = 0; k < dist; k++) {
			int ip = change.is + k * change.idir;
			int jp = change.js + k * change.jdir;

			grid[ip][jp] = change.prvColor;
		}
	}
}


PreCalcData MiniMax(const int N, int **grid, unsigned long long int curHash, 
		int remDepth, int curPlayer, int player, PreCalcData curBestChoice = {0, 0, {-1, -1}}) {
	cout << "Best move for " << curHash << " with depth " << remDepth << "is being calculated" << endl;
	printGrid(N, grid);
	if(preCalc[player].find(curHash) != preCalc[player].end()) {
		if(preCalc[player][curHash].value >= remDepth)
			return preCalc[player][curHash];
	}
	if(remDepth == 0) {
		return preCalc[player][curHash] = {evaluate(N, grid, player), 0, {-1, -1}};
	}
	auto posmoves = getPossibleMoves(N, grid, player);
	
	cout << posmoves.size() << endl;
	cout << __LINE__ << endl;

	if(posmoves.size() == 0) {
		bool boardFull = true;
		for(int i = 0; i < N && boardFull; i++)
			for(int j = 0; j < N; j++)
				if(grid[i][j] == 0) {
					boardFull = false;
					break;
				}

		if(boardFull)
			return preCalc[player][curHash] = {evaluate(N, grid, player), inf, {-1, -1}};
		else
			return preCalc[player][curHash] = {MiniMax(N, grid, curHash, remDepth - 1, 
					curPlayer ^ 3, player).value, remDepth, {-1, -1}};
	}
	cout << __LINE__ << endl;

	PreCalcData bestAnswer = {(__builtin_popcount(player ^ curPlayer) - 1) * inf, 
		remDepth, {-1, -1}};


	for(auto mv : posmoves) {
		unsigned long long int newHash = makeMove(N, grid, player, mv, curHash);

		auto val = MiniMax(N, grid, newHash, remDepth - 1, curPlayer, player);

		undoMoves(N, grid, curPlayer, curHash);

		if(curPlayer == player) {
			if(val.value > bestAnswer.value) {
				bestAnswer.value = val.value;
				bestAnswer.bestMove = mv;
			}
		} else {
			if(val.value < bestAnswer.value) {
				bestAnswer.value = val.value;
				bestAnswer.bestMove = mv;
			}
			if(val.value < curBestChoice.value) /* alpha-beta pruning */ 
				return {val.value, remDepth, mv};
		}

	}
	cout << __LINE__ << endl;
	return preCalc[player][curHash] = bestAnswer;
}


void setup(int N) {
	mt_rand = mt19937(time(0));

	generateZobristValues(N);

}

extern "C"
EXPORT int calc(int N, int grid[N][N], int player,
		int* bestMoveI, int* bestMoveJ, int max_depth = 5) {
	int **ngrid = new int*[N];
	for(int i = 0; i < N; i++)
		ngrid[i] = new int[N];
	setup(N);
	auto res = MiniMax(N, ngrid, generateHash(N, ngrid), max_depth, player, player);
	*bestMoveI = res.bestMove.first;
	*bestMoveJ = res.bestMove.second;
	return res.value;
}

int main() {
	const int N = 8;
	int **grid = new int*[N];
	for(int i = 0; i < N; i++)
		grid[i] = new int[N];
	for(int i = (N - 1) / 2; i < N / 2 + 1; i++)
		for(int j = (N - 1) / 2; j < N / 2 + 1; j++)
			grid[i][j] = (i + j) % 2 + 1;
	for(int i = 0; i < N; i++, cout << endl)
		for(int j = 0; j < N; j++)
			cout << grid[i][j];
	setup(N);
	unsigned long long int curHash = generateHash(N, grid);
	cout << "Hash: " << curHash << endl;
	printGrid(N, grid);
	for(int i = 0; i < 20; i++) {
		auto res = MiniMax(N, grid, curHash, 4, i % 2 + 1, i % 2 + 1);
		cout << "Best Outcome " << res.value << " with " << res.bestMove.first << ", " << res.bestMove.second << endl;

		unsigned long long int newHash = makeMove(N, grid, i % 2 + 1, res.bestMove, curHash);

		curHash = newHash;
		cout << "Hash: " << curHash << endl;
		printGrid(N, grid);
		cout << "End of MOVE" << endl;
		cout << "---------------------------------------" << endl;
	}

	return 0;
}
