import matplotlib.pyplot as plt
import networkx as nx
import random, copy


# can specity "planar" or "spring"
# if other is specified, will use "planar"
# "planar" is guaranteed to not have crossing edges, but it can
# look a bit nasty
# "spring" starts with a planar layout and then tries to make it look
# nicer using springs, but it isn't guaranteed to avoid crossing edges
def draw_planar_graph(graph, colour_vals = None, mode = "planar"):
    """Draws a planar graph without crossing edges, using pastel colors.

    Parameters:
    - graph: A dictionary mapping vertices to the set of its neighbours
         is assumed to be undirected (i.e. u is a neighbour of v
         if and only v is a neighbour of u)
    - colors: A list of basic color names (e.g., 'red', 'blue', 'green', 'yellow',
    'purple')
    """

    if colour_vals is None: colour_vals = dict()
    else: colour_vals = copy.deepcopy(colour_vals)

    G = nx.Graph()
    to_int = dict()
    labels = list()

    for u in graph:
        to_int[u] = len(to_int)
        G.add_node(to_int[u])

        for v in graph[u]:
            if v in G.nodes and v != u:
                G.add_edge(to_int[u], to_int[v])
        labels.append(u)
        if u not in colour_vals: colour_vals[u] = 0

    # 1. Define a quick mapping from standard colors to pastel hex codes
    colour_to_rgb = ["#FFFFFF", "#FFB3B3", "#B3D1FF", "#B3F0B3", "#FFEAA7", "#E1BEE7", "#E0E0E0"]

    print(colour_vals)
    colours = [colour_to_rgb[colour_vals[labels[v]]] for v in range(len(graph))]

    # 2. Verify planarity and get the layout
    is_planar, embedding = nx.check_planarity(G)
    if not is_planar:
        raise ValueError("The provided graph is not planar.")

    pos = nx.planar_layout(G)

    if mode == "spring": pos = nx.spring_layout(G, k = len(to_int)**0.05, pos = pos, iterations = 2)

    # 3. Draw the graph with a clean, soft aesthetic
    plt.figure(figsize=(8, 6), facecolor="#FAFAFA")

    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color=colours,
        node_size=400,
        font_weight="bold",
        font_color="#4A4A4A",  # Dark gray text is softer than pitch black
        edge_color="#CCCCCC",  # Lighter gray for the edges to match the aesthetic
        width=1.5,
        edgecolors='black',     # Color of the thin boundary around each node
        linewidths=0.5,          # Thickness of the boundary
        alpha = 0.8
    )

    plt.title("Planar Graph Drawing (Pastel Palette)", color="#4A4A4A")
    plt.show()


# --- Example Usage ---
if __name__ == "__main__":
    N = 10
    
    my_graph = nx.wheel_graph(N)

    # Input the standard colors you want
    vertex_colours = [random.choice(range(5)) for v in range(N)]

    draw_planar_graph(my_graph, vertex_colours)