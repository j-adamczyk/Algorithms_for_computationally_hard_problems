#include <fstream>
#include <iostream>
#include <iterator>
#include <queue>
#include <string>
#include <sstream>
#include <unordered_map>
#include <unordered_set>
#include <utility>
#include <vector>
#include "vertex_cover.h"
#include "utils.h"
#include "graph_operations.h"


using namespace std;


void check_and_add_left(string& curr_line, unordered_map<int, unordered_set<int>>& graph, int vertex,
                        int row, int col, int W)
{
    if (col > 0 && (curr_line[col - 1] == '-' || curr_line[col - 1] == '+'))
    {
        int vertex_2 = index(row, col - 1, W);
        graph[vertex].insert(vertex_2);
        graph[vertex_2].insert(vertex);
    }
}


void check_and_add_right(string& curr_line, unordered_map<int, unordered_set<int>>& graph, int vertex,
                         int row, int col, int W)
{
    if (col < W - 1 && (curr_line[col + 1] == '-' || curr_line[col + 1] == '+'))
    {
        int vertex_2 = index(row, col + 1, W);
        graph[vertex].insert(vertex_2);
        graph[vertex_2].insert(vertex);
    }
}


void check_and_add_above(string& prev_line, string& curr_line, unordered_map<int, unordered_set<int>>& graph,
                         int vertex, int row, int col, int W)
{
    if (row > 0 && (prev_line[col] == '|' || prev_line[col] == '+'))
    {
        int vertex_2 = index(row - 1, col, W);
        graph[vertex].insert(vertex_2);
        graph[vertex_2].insert(vertex);
    }
}


void process_line_tokens(string& prev_line, string& curr_line,
                         unordered_map<int, unordered_set<int>>& graph, int row, int W)
{
    for (int col = 0; col < W; col++)
    {
        char tile = curr_line[col];
        int vertex = index(row, col, W);

        // add vertex to the graph, if it isn't there already and tile isn't empty
        if (graph.count(vertex) == 0 && tile != '.')
        {
            unordered_set<int> empty_set;
            graph[vertex] = empty_set;
        }

        if (tile == '-')  // vertex may be connected to the one to the left/right
        {
            check_and_add_left(curr_line, graph, vertex, row, col, W);
            check_and_add_right(curr_line, graph, vertex, row, col, W);
        }
        else if (tile == '|')
        {
            check_and_add_above(prev_line, curr_line, graph, vertex, row, col, W);
            // can't check below, but can check above while calling this for the next line
        }
        else if (tile == '+')
        {
            check_and_add_left(curr_line, graph, vertex, row, col, W);
            check_and_add_right(curr_line, graph, vertex, row, col, W);
            check_and_add_above(prev_line, curr_line, graph, vertex, row, col, W);
            // can't check below, but can check above while calling this for the next line
        }
        // ignore tile == "." (empty)
    }
}


unordered_map<int, unordered_set<int>> load_graph(int W, int H, ifstream& source)
{
    unordered_map<int, unordered_set<int>> graph;
    string prev_line, curr_line;
    for (int i = 0; i < H; i++)
    {
        getline(source, curr_line);
        process_line_tokens(prev_line, curr_line, graph, i, W);
        prev_line = curr_line;
    }
    return graph;
}


int main()
{
    string in_file = "../graphs/wave_3.in";
    string out_file = "../graphs/wave_3.out";

    ifstream source(in_file);
    if (!source)
    {
        cout << "\nUnable to open file!";
        return -1;
    }

    string line;
    getline(source, line);
    istringstream buffer(line);
    vector<string> first_line_tokens{istream_iterator<string>(buffer), istream_iterator<string>()};

    W = stoi(first_line_tokens.at(0));  // grid width
    int H = stoi(first_line_tokens.at(1));  // grid height
    int L = stoi(first_line_tokens.at(2));  // distance between chosen vertices, number of edges
    int K = stoi(first_line_tokens.at(3));  // number of vertices to choose
    getline(source, line);  // ignore second line

    // load graph grid from standard input
    unordered_map<int, unordered_set<int>> graph = load_graph(W, H, source);

    // calculate G^L to solve Independent Set instead of L-distance Independent Set
    // vertices of degree 0 can be added to the solution here
    unordered_set<int> partial_solution = raise_graph_to_power(graph, L);
    K -= partial_solution.size();

    if (K == 0)
    {
        print_solution(partial_solution);
        return 0;
    }
    // Vertex Cover searches for k = V - K
    int k = graph.size() - K;

    /*
     * WARNING:
     * kernelization was turned off because it has some minor bug that sometimes gives wrong answers (people
     * are too close to each other). It should be fixed for better efficiency, but I don't have time.
    */

    // calculate graph kernel for efficiency
    /*bool solution_can_exist = kernelize(graph, partial_solution, k);

    if (!solution_can_exist && k <= 0)
    {
        cout << "ERROR: solution can't exist!";
        return 1;
    }

    if (solution_can_exist && k == 0)
    {
        // partial solution is the entire solution
        print_solution(partial_solution);
        return 0;
    }*/

    // convert to edge list, since I can't manage to debug the hashmap-based Vertex Cover
    vector<pair<int, int>> edge_list = to_edge_list(graph);
    unordered_set<int> solution_complement;
    solution_complement = vertex_cover(edge_list, solution_complement, k);

    unordered_set<int> solution;
    for (auto const& vertex : graph)
        solution.insert(vertex.first);

    for (auto const& vertex : solution_complement)
        solution.erase(vertex);

    for (auto const& point : partial_solution)
        solution.insert(point);

    print_solution(solution);

    return 0;
}
