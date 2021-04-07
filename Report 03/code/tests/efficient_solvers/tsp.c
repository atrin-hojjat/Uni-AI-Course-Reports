#include <string.h>
#include <math.h>
#include <stdio.h>

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

/* #define int __int32_t */


const int MaxN = 20;
int dp[MaxN][1 << MaxN];

int min(int a, int b) {
	return a > b ? b : a;
}

EXPORT int solve(int N, int grid[N][N]) {
	/*
	 * Sum of all edges must be less than 1e9 + 7
	 * This runs on O(2^n * n^2) so for under 1s performans N < 20
	 */
	memset(dp, 63, sizeof(dp));
	dp[0][1] = 0;
	for(int mask = 1; mask < (1 << N); mask++) {
		for(int i = 0; i < N; i++) {
			if(!((1 << i) & mask))
				continue;
			for(int j = 0; j < N; j++) {
				if((1 << j) & mask)
					continue;
				dp[j][mask | (1 << j)] = min(dp[j][mask | (1 << j)], dp[i][mask] + grid[i][j]);
			}
		}
	}
	int mn = 1e9 + 7;
	for(int i = 0; i < N; i++) 
		mn = min(mn, grid[i][0] + dp[i][(1 << N) - 1]);
	return mn;
}
