#include <unordered_map>
#include <unordered_set>
#include <fstream>
#include <iterator>
#include <iostream>
#include <string>
#include "utils.h"


int W;


int index(int row, int col, int W)
{
    return row * W + col;
}

void print_point(int point)
{
    int row = point / W;
    int col = point % W;
    cout << "(" << row << ", " << col << ")";
}

void print_graph(unordered_map<int, unordered_set<int>> graph)
{
    for (auto const& x : graph)
    {
        cout << x.first << " ";
        print_point(x.first);
        cout << " -> [";
        for (auto const& y : x.second)
        {
            print_point(y);
            cout << " ";
        }
        cout << "]\n";
    }
}

void print_solution(const unordered_set<int>& solution)
{
    for (auto const& point : solution)
    {
        int row = point / W;
        int col = point % W;
        cout << row << " " << col << "\n";
    }
}


void print_solution_to_file(const unordered_set<int>& solution, const string& filename)
{
    ofstream file;
    file.open(filename);
    for (auto const& point : solution)
    {
        int row = point / W;
        int col = point % W;
        // reverse order because of the project requirements
        file << col << " " << row << "\n";
    }
    file.close();
}


vector<pair<int, int>> to_edge_list(unordered_map<int, unordered_set<int>>& graph)
{
    unordered_set<pair<int, int>> edges;
    for (auto const& vertex : graph)
    {
        int v = vertex.first;
        for (auto const& u : vertex.second)
            v < u ? edges.insert(make_pair(v, u)) : edges.insert(make_pair(u, v));
    }

    vector<pair<int, int>> edge_list(edges.size());
    copy(edges.begin(), edges.end(), edge_list.begin());
    return edge_list;
}
