#include <iostream>
#include <algorithm>
#include <string>
#include <vector>
#include <cmath>
#include <unordered_set>
#include <set>
#include <unordered_map>
#include <map>
#include <functional>
#include <bitset>
#include <cstdint>
#include <queue>
#include <iomanip>
#include <limits>
#include <random>
#include <chrono>
#include <numeric>
#define _CRT_SECURE_NO_WARNINGS
#define endl "\n"
#define make(type, x) type x; cin >> x
#define all(a) (a).begin(), (a).end()
#define sz(ll) (int)(a).size()
#define pb push_back
#define mp make_pair
#define int long long
#define mass(n, x) vector<int> a(n); for (auto &i: a) cin >> i;

using namespace std;
using namespace std::chrono;

typedef long long ll;
typedef unsigned long long ull;
typedef long double ld;
typedef pair<int, int> pii;
typedef pair<ll, ll > pll;
mt19937 rnd(593);
const ll E5 = 100000, E6 = 10 * E5, E7 = 10 * E6, E8 = 10 * E7, E9 = 10 * E8;
const ll M7 = E9 + 7, M9 = E9 + 9, mod = 998244353;
const ll INF = M7*M7;

int Hungarian(vector<vector<int>> a, vector<int> &ans, bool pr=false) {
	int n = a.size(), m = a[0].size();

	a.insert(a.begin(), vector<int>(a[0].size(), 0));
	for (auto& i : a) i.insert(i.begin(), 0);

	int iter = 0;

	vector<int> u(n + 1), v(m + 1), p(m + 1), way(m + 1);
	for (int i = 1; i <= n; ++i) {
		p[0] = i;
		int j0 = 0;
		vector<int> minv(m + 1, INF);
		vector<char> used(m + 1, false);
		do {
			used[j0] = true;
			int i0 = p[j0], delta = INF, j1;
			for (int j = 1; j <= m; ++j)
				if (!used[j]) {
					int cur = a[i0][j] - u[i0] - v[j];
					if (cur < minv[j])
						minv[j] = cur, way[j] = j0;
					if (minv[j] < delta)
						delta = minv[j], j1 = j;
				}
			for (int j = 0; j <= m; ++j)
				if (used[j])
					u[p[j]] += delta, v[j] -= delta;
				else
					minv[j] -= delta;
			j0 = j1;
		} while (p[j0] != 0);
		do {
			int j1 = way[j0];
			p[j0] = p[j1];
			j0 = j1;
		} while (j0);
		++iter;
		if (pr) {
			cout << "Iteration: " << iter << endl;
			for (int pi = 0; pi < n; ++pi) {
				for (int pj = 0; pj < m; ++pj)
					cout << a[pi + 1][pj + 1] - u[pi + 1] - v[pj + 1] << " ";
				cout << endl;
			}
		}
	}

	for (int j = 1; j <= m; ++j)
		ans[p[j] - 1] = j - 1;
	return -v[0];
}

int Mak(vector<vector<int>> &source, vector<int> &ans, bool pr=false) {
	auto a = source;
	vector<set<int>> x(a.size());
	bool fin = true;

	for (int i = 0; i < a.size(); ++i) {
		int m = min_element(all(a[i])) - a[i].begin();
		x[m].insert(i);
		if (x[m].size() > 1) fin = false;
	}

	int iter = 0;

	while (!fin) {
		int m = 0, c = 0;
		fin = true;
		for (int i = 0; i < x.size(); ++i) if (m < x[i].size()) m = x[i].size(), c = i;
		set<int> max_col = { c };

		int k, m_delta;
		while (1) {
			k = 0, m_delta = INF;
			for (int i = 0; i < a.size(); ++i) {
				int cont = -1;
				for (auto& j : max_col) if (x[j].count(i)) cont = a[i][j];
				if (cont == -1) continue;
				for (int j = 0; j < a[0].size(); ++j) {
					if (max_col.count(j)) continue;
					if (a[i][j] - cont < m_delta) m_delta = a[i][j] - cont, k = i, c = j;
				}
			}
			for (auto& j : max_col) for (auto& i : a) i[j] += m_delta;
			if (x[c].size() == 0) {
				for (auto& i : x) i.erase(k);
				x[c].insert(k);
				break;
			}
			max_col.insert(c);
		}

		for (auto &i: x) if (i.size() > 1) fin = false;

		++iter;
		if (pr) {
			cout << "Iteration: " << iter << endl;
			for (int i = 0; i < x.size(); ++i) {
				cout << "Столбец " << i + 1 << " : ";
				for (auto& j : x[i]) cout << j + 1 << " ";
				cout << endl;
			}
		}
	}
	
	int s = 0;
	for (int j = 0; j < a.size(); ++j) for (auto& i : x[j]) {
		s += source[i][j];
		ans[i] = j;
	}
	return s;
}

void solve() {
	setlocale(LC_ALL, "Russian");
	vector<vector<int>> a = { 
		{50, 50, 120, 20}, 
		{70, 40, 20, 30},
		{90, 30, 50, 140},
		{70, 20, 60, 70} };
	vector<vector<int>> b = {
		{10, 5, 9, 18, 11},
		{13, 19, 6, 12, 14},
		{3, 2, 4, 4, 5},
		{18, 9, 12, 17, 15},
		{11, 6, 14, 19, 10} };
	vector<int> res(b.size());
	int ans = Mak(b, res, true);
	cout << "Ответ: " << ans << endl;
	for (int i = 0; i < b.size(); ++i) cout << "Для строки " << i + 1 << " выбран столбец " << res[i] + 1 << " со стоимостью " << b[i][res[i]] << endl;
}

signed main() {
    ios_base::sync_with_stdio(false);
    cin.tie(0);
    cout.tie(0);

    int t = 1;
    if (t == 0) cin >> t;
    while (t--) solve();

    return 0;
}