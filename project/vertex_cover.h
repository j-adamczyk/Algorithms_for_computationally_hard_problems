#ifndef VERTEX_COVER_H
#define VERTEX_COVER_H

#include <unordered_set>

using namespace std;

bool kernelize(unordered_map<int, unordered_set<int>>& graph, unordered_set<int>& solution, int& k);

unordered_set<int> vertex_cover(vector<pair<int, int>>& graph, unordered_set<int>& solution, int& k);


#endif //VERTEX_COVER_H
