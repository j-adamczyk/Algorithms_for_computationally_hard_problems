#ifndef GRAPH_POWER_H
#define GRAPH_POWER_H

#include <unordered_map>
#include <unordered_set>

using namespace std;

unordered_set<pair<int, int>> edge_adding_BFS(unordered_map<int, unordered_set<int>>& graph, int source, int power);

unordered_set<int> raise_graph_to_power(unordered_map<int, unordered_set<int>>& graph, int power);

unordered_map<int, unordered_set<int>> get_graph_complement(unordered_map<int, unordered_set<int>>& graph, int k);

#endif //GRAPH_POWER_H
