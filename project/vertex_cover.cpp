#include <iostream>
#include <vector>
#include <utility>
#include <unordered_map>
#include <unordered_set>
#include "utils.h"
#include "vertex_cover.h"

using namespace std;

// returns boolean value whether the solution can exist at all
bool kernelize(unordered_map<int, unordered_set<int>>& graph, unordered_set<int>& solution, int& k)
{
    while (true)
    {
        unordered_set<int> to_remove;
        for (auto const& vertex : graph)
        {
            int v = vertex.first;
            if (vertex.second.empty())
                to_remove.insert(v);
            else if (vertex.second.size() == 1)
            {
                int u = *vertex.second.begin();
                solution.insert(u);

                to_remove.insert(u);
                to_remove.insert(v);

                k -= 1;
                break;
            }
            else if (vertex.second.size() > k)
            {
                solution.insert(v);
                to_remove.insert(v);
                k -= 1;
                break;
            }
        }

        if (!to_remove.empty())
        {
            for (auto const& v : to_remove)
            {
                unordered_set<int> neighbors;
                if (map_contains(graph, v))
                    neighbors = graph[v];
                else
                    continue;

                graph.erase(v);

                for (auto const& u : neighbors)
                {
                    if (!map_contains(graph, u) || !set_contains(graph[u], v))
                        continue;

                    graph[u].erase(v);

                    if (graph[u].empty())
                        graph.erase(u);
                }
            }
        }
        else
            break;
    }

    return graph.size() <= k * k;
}


string check_solution(vector<pair<int, int>>& graph, int& k)
{
    // safety measure for cases when we remove too many neighbors
    if (k < 0)
        return "none";

    // if G is empty, then all needed vertices have been chosen
    if (graph.empty())
        return "solution";

    // if G is not empty, but k is 0, then we "used up" all k vertices,
    // therefore solution does not exist
    if (k == 0)
        return "none";

    // if none of the above happen, we should not yet finish
    return "continue";
}


int get_neighbor_of_vertex(vector<pair<int, int>>& graph, unsigned int u)
{
    for (auto const& edge : graph)
    {
        // return the neighbor after finding the edge with u
        if (edge.first == u)
            return edge.second;
        else if (edge.second == u)
            return edge.first;
    }

    return -1;
}


unordered_set<int> get_neighbors_of_vertex(vector<pair<int, int>>& graph, unsigned int u)
{
    unordered_set<int> neighbors;
    for (auto const& edge : graph)
    {
        if (edge.first == u)
            neighbors.insert(edge.second);
        else if (edge.second == u)
            neighbors.insert(edge.first);
    }
    return neighbors;
}


vector<pair<int, int>> remove_neighbors_of_vertex(vector<pair<int, int>>& graph, unsigned int u)
{
    vector<pair<int, int>> graph_after_removal;
    for (auto const& edge : graph)
        if (edge.first != u && edge.second != u)
            graph_after_removal.push_back(edge);

    return graph_after_removal;
}


unordered_map<int, int> get_vertices_degrees(vector<pair<int, int>>& graph)
{
    unordered_map<int, int> degrees;
    for (auto const& edge : graph)
    {
        // if map contains key, it'll be incremented
        // otherwise, it's initialized with value 0 and incremented
        degrees[edge.first] += 1;
        degrees[edge.second] += 1;
    }
    return degrees;
}


vector<pair<int, int>> remove_degree_1_vertices(vector<pair<int, int>>& graph, unordered_set<int>& solution, int& k,
        unordered_map<int, int>& degrees)
{
    /*
     * while graph contains at least one vertex with degree 1, remove them (add
     * their only neighbor to the solution, remove his edges)
     * it may create new vertices, hence the loop
     */
    bool changed = true;
    while (changed)
    {
        changed = false;
        for (auto const& vertex : degrees)
        {
            int u = vertex.first;
            int degree = vertex.second;


            if (degree == 1)
            {
                int v = get_neighbor_of_vertex(graph, u);
                if (v == -1)  // may happen if we removed all neighbors already
                    continue;

                solution.insert(v);
                k--;
                graph = remove_neighbors_of_vertex(graph, v);
                changed = true;
            }
        }

        degrees = get_vertices_degrees(graph);
    }
    return graph;
}


int get_highest_degree_vertex(unordered_map<int, int>& degrees)
{
    int max_degree = -1;
    int best_vertex = -1;
    for (auto const& vertex : degrees)
    {
        int u = vertex.first;
        int degree = vertex.second;
        if (degree > max_degree)
        {
            max_degree = degree;
            best_vertex = u;
        }
    }
    return best_vertex;
}


vector<pair<int, int>> remove_neighbors_edges(vector<pair<int, int>>& graph, unordered_set<int>& neighbors)
{
    vector<pair<int, int>> graph_after_removal;
    for (auto const& edge : graph)
    {
        if (!set_contains(neighbors, edge.first) && !set_contains(neighbors, edge.second))
            graph_after_removal.push_back(edge);
    }

    return graph_after_removal;
}


unordered_set<int> vertex_cover(vector<pair<int, int>>& graph, unordered_set<int>& solution, int& k)
{
    // check is we can finish with this solution
    string check = check_solution(graph, k);
    if (check == "none")
        return unordered_set<int>();
    else if (check == "solution")
        return solution;
    // else - continue

    // calculate degrees of vertices, remove degree 1 vertices
    unordered_map<int, int> degrees = get_vertices_degrees(graph);
    graph = remove_degree_1_vertices(graph, solution, k, degrees);

    // check if the solution can still exist
    check = check_solution(graph, k);
    if (check == "none")
        return unordered_set<int>();
    else if (check == "solution")
        return solution;

    // take vertex of the highest degree as u
    int u = get_highest_degree_vertex(degrees);
    vector<pair<int, int>> graph_copy = graph;
    graph_copy = remove_neighbors_of_vertex(graph_copy, u);

    unordered_set<int> solution_copy = solution;
    solution_copy.insert(u);
    int k_copy = k - 1;

    unordered_set<int> possible_sol_1 = vertex_cover(graph_copy, solution_copy, k_copy);
    if (!possible_sol_1.empty())
        return possible_sol_1;

    // take neighbors of u, remove all of their neighbors
    unordered_set<int> neighbors = get_neighbors_of_vertex(graph, u);
    graph = remove_neighbors_edges(graph, neighbors);

    solution.insert(neighbors.begin(), neighbors.end());
    k -= neighbors.size();
    unordered_set<int> possible_sol_2 = vertex_cover(graph, solution, k);
    return possible_sol_2;
}