from file_utils import file_reader


def count_computers_with_t(data: list[str]) -> int:
    graph: dict[str, list[str]] = __build_graph(data)
    cycles: list[list[str]] = __find_cycles_of_length(graph)
    return sum([1 if sum([1 if c.startswith("t") else 0 for c in cycle]) > 0 else 0 for cycle in cycles])


def find_the_larget_set(data: list[str]) -> list[str]:
    graph: dict[str, list[str]] = __build_graph(data)
    cliques: list[set[str]] = []
    __bron_kerbosch(graph, set(), set(graph.keys()), set(), cliques)
    result = max(cliques, key=len) if cliques else list()
    return sorted(result)


# not mine, copied/adjusted from google
def __bron_kerbosch(graph: dict[str, list[str]], r: set[str], p: set[str], x: set[str], cliques: list[set[str]]):
    if not p and not x:
        cliques.append(r)
        return

    for v in list(p):
        neighbors = set(graph.get(v, []))
        __bron_kerbosch(graph, r | {v}, p & neighbors, x & neighbors, cliques)
        p.remove(v)
        x.add(v)


def __find_cycles_of_length(graph: dict[str, list[str]], k: int = 3) -> list[list[str]]:
    cycles: list[list[str]] = []

    def dfs(start: str, current: str, path: list[str]):
        if len(path) == k:
            if start in graph[current]:
                cycle = tuple(sorted(path))
                if cycle not in seen:
                    cycles.append(path[:])
                    seen.add(cycle)
            return

        for neighbor in graph[current]:
            if neighbor not in path:
                path.append(neighbor)
                dfs(start, neighbor, path)
                path.pop()

    seen = set()
    for node in graph:
        dfs(node, node, [node])
    return cycles


def __build_graph(data: list[str]) -> dict[str, list[str]]:
    graph: dict[str, list[str]] = {}
    for line in data:
        nodes = line.split("-")
        __add_edge(graph, nodes[0], nodes[1])
    return graph


def __add_edge(graph, u, v):
    if u not in graph:
        graph[u] = []
    graph[u].append(v)

    if v not in graph:
        graph[v] = []
    graph[v].append(u)


test_data = """kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn"""

SOLUTION_INPUT = file_reader.read_str_from_file("input/day23.txt")

assert count_computers_with_t(test_data.splitlines()) == 7
assert count_computers_with_t(SOLUTION_INPUT) == 1184

assert find_the_larget_set(test_data.splitlines()) == ["co", "de", "ka", "ta"]
expected_solution = ["hf", "hz", "lb", "lm", "ls", "my", "ps", "qu", "ra", "uc", "vi", "xz", "yv"]
assert find_the_larget_set(SOLUTION_INPUT) == expected_solution
