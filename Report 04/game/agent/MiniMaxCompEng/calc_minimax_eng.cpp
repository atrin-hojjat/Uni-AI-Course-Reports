#include <cstring>
#include <math.h>
#include <iostream>
#include <unordered_map>
#include <map>
#include <stack>
#include <vector>
#include <random>
#include <stdio.h>
#include <Python.h>

#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <numpy/arrayobject.h>

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
	int k, is, js, idir, jdir;
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
map<unsigned long long int, PreCalcData> preCalc[STATES][STATES];
stack<ChangedSegment> moves = stack<ChangedSegment>();
mt19937 mt_rand;


unsigned long long randomGenerator() {
	uniform_int_distribution<unsigned long long int> dist(0, UINT_MAX);

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
	// printGrid(N, grid);
	// cout << "Evaluation: " << val << " " << player << endl;
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
	if(!~i || !~j || i < 0 || i >= N || j < 0 || j >= N)
		return curHash;
	if(grid[i][j] != 0) {
		cout << i << " " << j << endl;
		cout << grid[i][j] << endl;
		cout << "FATAL ERROR WRONG START" << endl;
		exit(-1);
	}
	vector<ChangedSegment> changes;

	changes.push_back({1, i, j, 0, 0, curHash, 0, player});


	for(int dir = -1; dir < 2; dir += 2) {
		for(int jp = j + dir; jp > -1 && jp < N; jp += dir) {
			if(grid[i][jp] == 0) 
				break;
			if(grid[i][jp] == player) {
				if(abs(jp - j) > 1) {
					ChangedSegment chngd;
					if(jp < j) 
						chngd = {abs(jp - j) - 1, i, j, 0, -1, curHash, 3 ^ player, player};
					else
						chngd = {abs(jp - j) - 1, i, j, 0, 1, curHash, 3 ^ player, player};
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
						chngd = {abs(ip - i) - 1, i, j, 1, 0, curHash, 3 ^ player, player};
					else
						chngd = {abs(ip - i) - 1, i, j, -1, 0, curHash, 3 ^ player, player};
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
						ChangedSegment chngd = {k - 1, i, j, id, jd, curHash, 3 ^ player, player};
						changes.push_back(chngd);
					}
					break;
				}
			}

	unsigned long long int newHash = curHash;
	
	for(auto change : changes) {
		moves.push(change);
		// int dist = max(abs(change.ie - change.is), abs(change.je - change.js));
		for(int k = 1; k <= change.k; k++) {
			int ip = change.is + k * change.idir;
			int jp = change.js + k * change.jdir;
			if(ip >= N || ip < 0 || jp >= N || jp < 0) {

				cout << "FATAL ERROR " << change.k << " " << change.is << " " << change.js << " - " << ip << " " << jp << endl;
				exit(-1);
			}

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
		
		// int dist = max(abs(change.ie - change.is), abs(change.je - change.js));
		for(int k = 1; k <= change.k; k++) {
			int ip = change.is + k * change.idir;
			int jp = change.js + k * change.jdir;

			grid[ip][jp] = change.prvColor;
		}
	}
}


PreCalcData MiniMax(const int N, int **grid, unsigned long long int curHash, 
		int remDepth, int curPlayer, int player, PreCalcData curBestChoice = {0, 0, {-1, -1}}) {
	if(preCalc[player][curPlayer].find(curHash) != preCalc[player][curPlayer].end()) {
		if(preCalc[player][curPlayer][curHash].depth >= remDepth)
			return preCalc[player][curPlayer][curHash];
	}
	if(remDepth == 0) {
		return preCalc[player][curPlayer][curHash] = {evaluate(N, grid, player), 0, {-1, -1}};
	}
	auto posmoves = getPossibleMoves(N, grid, player);

	if(posmoves.size() == 0) {
		bool boardFull = true;
		for(int i = 0; i < N && boardFull; i++)
			for(int j = 0; j < N; j++)
				if(grid[i][j] == 0) {
					boardFull = false;
					break;
				}

		if(boardFull)
			return preCalc[player][curPlayer][curHash] = {evaluate(N, grid, player), inf, {-1, -1}};
		else
			return preCalc[player][curPlayer][curHash] = {MiniMax(N, grid, curHash, remDepth - 1, 
					curPlayer ^ 3, player).value, remDepth, {-1, -1}};
	}

	PreCalcData bestAnswer = {(__builtin_popcount(player ^ curPlayer) - 1) * inf, 
		remDepth, {-1, -1}};


	for(auto mv : posmoves) {
		unsigned long long int newHash = makeMove(N, grid, player, mv, curHash);

		PreCalcData val;
		val = MiniMax(N, grid, newHash, remDepth - 1, curPlayer ^ 3, player, bestAnswer);

		undoMoves(N, grid, curPlayer, curHash);

		if(curPlayer == player) {
			if(val.value > bestAnswer.value) {
				bestAnswer.value = val.value;
				bestAnswer.bestMove = mv;
			}
			if(~curBestChoice.bestMove.first && val.value > curBestChoice.value) /* alpha-beta pruning */
				return {val.value, remDepth, mv};
		} else {
			if(val.value < bestAnswer.value) {
				bestAnswer.value = val.value;
				bestAnswer.bestMove = mv;
			}
			if(~curBestChoice.bestMove.first && val.value < curBestChoice.value) /* alpha-beta pruning */
				return {val.value, remDepth, mv};
		}

	}
	return preCalc[player][curPlayer][curHash] = bestAnswer;
}


void setup(int N) {
	for(int i = 0; i < STATES; i++)
		for(int j = 0; j < STATES; j++)
			preCalc[i][j] = map<unsigned long long int, PreCalcData>();
	moves = stack<ChangedSegment>();

	mt_rand = mt19937(time(0));

	generateZobristValues(N);

}


/* Deprecated */
extern "C"
EXPORT int calc(int N, int grid[N][N], int player,
		int* bestMoveI, int* bestMoveJ, int max_depth = 5) {
	int **ngrid = new int*[N];
	for(int i = 0; i < N; i++)
		ngrid[i] = new int[N];
	setup(N);
	for(int i = 0; i < STATES; i++)
		for(int j = 0; j < STATES; j++)
			preCalc[i][j] = map<unsigned long long int, PreCalcData>();
	moves = stack<ChangedSegment>();
	for(int i = 0; i < N; i++)
		for(int j = 0; j < N; j++)
			ngrid[i][j] = grid[i][j];
	auto res = MiniMax(N, ngrid, generateHash(N, ngrid), max_depth, player, player);
	*bestMoveI = res.bestMove.first;
	*bestMoveJ = res.bestMove.second;
	return res.value;
}

static PyObject* calculateMiniMax(PyObject* self, PyObject* args) { /* WIP */

	char *argnames[] = {"N", "grid", "player", "max_depth", NULL};

	int N, player, max_depth;
	int *gridVal;
	PyObject *gridArg = NULL;
	PyObject *gridArr = NULL;


	if(!PyArg_ParseTuple(args, "iOii", &N, &gridArg, &player, &max_depth)) {
		PyErr_SetString(PyExc_TypeError,
									"Invalid Parameter");
		return NULL;
	}

	// if(!PyArg_ParseTupleAndKeywords(args, kwds, "", argnames, &N, &grid, &player, &max_depth))
	//   return NULL;
	
	// PyArray_FROM_OTF(gridArg, NPY_INT32, NPY_ARRAY_IN_ARRAY);

	gridVal = (int*) PyArray_DATA((PyArrayObject*)gridArg);

	int **ngrid = new int*[N];
	for(int i = 0; i < N; i++)
		ngrid[i] = new int[N];
	setup(N);
	for(int i = 0; i < STATES; i++)
		for(int j = 0; j < STATES; j++)
			preCalc[i][j] = map<unsigned long long int, PreCalcData>();
	moves = stack<ChangedSegment>();
	for(int i = 0; i < N; i++)
		for(int j = 0; j < N; j++)
			ngrid[i][j] = gridVal[i * N + j];

	// cout << player << " " << max_depth<< endl;
	auto res = MiniMax(N, ngrid, generateHash(N, ngrid), max_depth, player, player);

	for(int i = 0; i < N; i++)
		for(int j = 0; j < N; j++)
			if(ngrid[i][j] != gridVal[i * N + j]) {
				cout << "FATAL ERROR" << endl;
				cout << "MOVE SEQUECE WASN'T SYMMETRICAL" << endl;
				for(int I = 0; I < N; I++, cout << endl)
					for(int J = 0; J < N; J++)
						cout << ngrid[I][J] << " ";
				for(int I = 0; I < N; I++, cout << endl)
					for(int J = 0; J < N; J++)
						cout << gridVal[I * N + J] << " ";
				exit(-1);
			}

	PyObject* ret = PyDict_New();

	PyDict_SetItem(ret, PyUnicode_FromString("value"), PyLong_FromLong(res.value));
	PyDict_SetItem(ret, PyUnicode_FromString("depth"), PyLong_FromLong(res.depth));
	PyDict_SetItem(ret, PyUnicode_FromString("move"), PyTuple_Pack(2, 
				PyLong_FromLong(res.bestMove.first), PyLong_FromLong(res.bestMove.second)));

	return ret;
}

/* Use this function for testing c++ */
int main2() {
	const int N = 8;
	int **grid = new int*[N];
	for(int i = 0; i < N; i++)
		grid[i] = new int[N];
	for(int i = (N - 1) / 2; i < N / 2 + 1; i++)
		for(int j = (N - 1) / 2; j < N / 2 + 1; j++)
			grid[i][j] = 2 - (i + j) % 2;
	for(int i = 0; i < N; i++, cout << endl)
		for(int j = 0; j < N; j++)
			cout << grid[i][j];
	setup(N);
	unsigned long long int curHash = generateHash(N, grid);
	cout << "Hash: " << curHash << endl;
	printGrid(N, grid);
	for(int i = 0; i < 80; i++) {
		auto res = MiniMax(N, grid, curHash, 11, i % 2 + 1, i % 2 + 1);
		cout << "Best Outcome " << res.value << " with " << res.bestMove.first << ", " << res.bestMove.second << " " << res.depth << endl;

		unsigned long long int newHash = makeMove(N, grid, i % 2 + 1, res.bestMove, curHash);

		curHash = newHash;
		cout << "Hash: " << curHash << endl;
		printGrid(N, grid);
		cout << "End of MOVE" << endl;
		cout << "---------------------------------------" << endl;
	}

	return 0;
}


static PyMethodDef MiniMaxMethods[] = {
	{"calculateMiniMax", calculateMiniMax, METH_VARARGS, "Calculate Minimax"},
	{NULL, NULL, 0, NULL}
};

static struct PyModuleDef MiniMaxModule = {
	PyModuleDef_HEAD_INIT,
	"MiniMax",   /* name of module */
	NULL, /* module documentation, may be NULL */
	-1,       /* size of per-interpreter state of the module,
							 or -1 if the module keeps state in global variables. */
	MiniMaxMethods
};

PyMODINIT_FUNC
PyInit_MiniMax(void)
{
	return PyModule_Create(&MiniMaxModule);
}


/* This function is for registering python modules */
int main(int argc, char *argv[]) {
	wchar_t *program = Py_DecodeLocale(argv[0], NULL);
	if (program == NULL) {
			fprintf(stderr, "Fatal error: cannot decode argv[0]\n");
			exit(1);
	}

	/* Add a built-in module, before Py_Initialize */
	if (PyImport_AppendInittab("MiniMax", PyInit_MiniMax) == -1) {
			fprintf(stderr, "Error: could not extend in-built modules table\n");
			exit(1);
	}

	/* Pass argv[0] to the Python interpreter */
	Py_SetProgramName(program);

	/* Initialize the Python interpreter.  Required.
		 If this step fails, it will be a fatal error. */
	Py_Initialize();

	PyMem_RawFree(program);
	return 0;
}
