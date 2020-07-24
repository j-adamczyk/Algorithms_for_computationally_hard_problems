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


using namespace std;


/*
 * WARNING: this file is a huge mess, all other files merged into one, because we were forced to use a terrible
 * code checking system that could only take 1 .cpp file and no header files. For real, well developed and divided
 * project see other file, especially the main.cpp file, which is the entry point for it.
 */


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


void print_solution(const unordered_set<int>& solution)
{
    for (auto const& point : solution)
    {
        int row = point / W;
        int col = point % W;
        cout << col << " " << row << "\n";
    }
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


unordered_map<int, unordered_set<int>> load_graph(int W, int H)
{
    unordered_map<int, unordered_set<int>> graph;
    string prev_line, curr_line;
    for (int i = 0; i < H; i++)
    {
        getline(cin, curr_line);
        process_line_tokens(prev_line, curr_line, graph, i, W);
        prev_line = curr_line;
    }
    return graph;
}


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
            if (visited.find(v) == visited.end())
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
            edges_to_add.insert(new_edges.begin(), new_edges.end());
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
                if (graph.find(v) != graph.end())
                    neighbors = graph[v];
                else
                    continue;

                graph.erase(v);

                for (auto const& u : neighbors)
                {
                    if (graph.find(u) == graph.end() || graph[u].find(v) == graph[u].end())
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
        if ((neighbors.find(edge.first) == neighbors.end()) && (neighbors.find(edge.second) == neighbors.end()))
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


int main()
{
    string line;
    getline(cin, line);
    istringstream buffer(line);
    vector<string> first_line_tokens{istream_iterator<string>(buffer), istream_iterator<string>()};

    W = stoi(first_line_tokens.at(0));  // grid width
    int H = stoi(first_line_tokens.at(1));  // grid height
    int L = stoi(first_line_tokens.at(2));  // distance between chosen vertices, number of edges
    int K = stoi(first_line_tokens.at(3));  // number of vertices to choose
    getline(cin, line);  // ignore second line

    // load graph grid from standard input
    unordered_map<int, unordered_set<int>> graph = load_graph(W, H);

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
