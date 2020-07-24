#ifndef UTILS_H
#define UTILS_H

#include <unordered_map>
#include <unordered_set>

using namespace std;

int index(int row, int col, int W);

void print_point(int point);

void print_graph(unordered_map<int, unordered_set<int>> graph);

void print_solution(const unordered_set<int>& solution);

void print_solution_to_file(const unordered_set<int>& solution, const string& filename);

template<class T>
void set_union(unordered_set<T>& add_to, unordered_set<T>& add_from)
{
    add_to.insert(add_from.begin(), add_from.end());
}


template<class T>
bool set_contains(const unordered_set<T>& s, const T& elem)
{
    return s.find(elem) != s.end();
}

template<typename Key, typename Value, typename Arg>
bool map_contains(const unordered_map<Key, Value> m, const Arg& key)
{
    return m.find(key) != m.end();
}

namespace std
{
    // enables using pairs in sets
    template <> struct hash<pair<int, int>>
    {
        inline size_t operator()(const pair<int, int> &v) const
        {
            hash<int> int_hasher;
            return int_hasher(v.first) ^ int_hasher(v.second);
        }
    };
}

vector<pair<int, int>> to_edge_list(unordered_map<int, unordered_set<int>>& graph);


extern int W;


#endif //UTILS_H
