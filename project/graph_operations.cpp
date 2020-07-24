#include <utility>
#include <unordered_map>
#include <unordered_set>
#include <queue>
#include "utils.h"
#include "graph_operations.h"


unordered_set<pair<int, int>> edge_adding_BFS(unordered_map<int, unordered_set<int>>& graph, int source, int power)
{
    unordered_set<pair<int, int>> edges_to_add;
    unordered_set<int> visited;
    unordered_map<int, int> distances;
    distances[source] = 0;
    queue<int> queue;
    queue.push(source);

    while (!queue.empty())
    {
        int u = queue.front();
        queue.pop();
        visited.insert(u);
        for (auto const& v : graph[u])
        {
            if (!set_contains(visited, v))
            {
                visited.insert(v);
                distances[v] = distances[u] + 1;
                edges_to_add.insert(make_pair(source, v));
                if (distances[v] < power)
                    queue.push(v);
            }
        }
    }

    return edges_to_add;
}

unordered_set<int> raise_graph_to_power(unordered_map<int, unordered_set<int>>& graph, int power)
{
    unordered_set<int> solution;
    unordered_set<pair<int, int>> edges_to_add;
    for (auto const& vertex : graph)
    {
        int source = vertex.first;
        // if we have a vertex of degree 0, we just add it to the solution and go on
        if (vertex.second.empty())
            solution.insert(source);
        else
        {
            unordered_set<pair<int, int>> new_edges = edge_adding_BFS(graph, source, power);
            set_union(edges_to_add, new_edges);
        }
    }

    // remove vertices of degree 0 from the graph (they're already in the solution)
    for (auto const& v : solution)
        graph.erase(v);

    for (auto const& edge : edges_to_add)
    {
        int u = edge.first;
        int v = edge.second;
        graph[v].insert(u);
        graph[u].insert(v);
    }

    return solution;
}


unordered_map<int, unordered_set<int>> get_graph_complement(unordered_map<int, unordered_set<int>>& graph, int k)
{
    unordered_map<int, unordered_set<int>> graph_complement;
    int V = graph.size();

    unordered_set<int> vertices;
    for (auto const& vertex : graph)
        vertices.insert(vertex.first);

    for (auto const& vertex : graph)
    {
        int vertex_degree = vertex.second.size();

        // ignore vertices that would have degree < k in complement - we'll be searching for k-clique there
        int complement_degree = V - vertex_degree;
        if (complement_degree < k)
            continue;

        unordered_set<int> vertex_complement;
        for (auto const& v : vertices)
            if (!set_contains(vertex.second, v))
                vertex_complement.insert(v);

        graph_complement[vertex.first] = vertex_complement;
    }

    return graph_complement;
}
