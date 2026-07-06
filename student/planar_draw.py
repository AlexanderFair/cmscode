import matplotlib.pyplot as plt
import networkx as nx
import random, copy
from time import sleep

# intialize the object with a graph and optionally an initall colouring.
# You can then update the colour of a vertex. It will pause for 1 second after an update!
# You should also have a sleep call at the end of your program otherwise it will just exit!
class Planar_Graph_Drawing:
    # can specity "planar" or "spring"
    # if other is specified, will use "planar"
    # "planar" is guaranteed to not have crossing edges, but it can
    # look a bit nasty
    # "spring" starts with a planar layout and then tries to make it look
    # nicer using springs, but it isn't guaranteed to avoid crossing edges
    def __init__(self, graph, colour_vals=None, mode="planar"):
        if colour_vals is None: self.colour_vals = dict()
        else: self.colour_vals = copy.deepcopy(colour_vals)

        self.G = nx.Graph()
        self.to_int = dict()
        self.labels = list()

        for u in graph:
            self.to_int[u] = len(self.to_int)
            self.G.add_node(self.to_int[u])

            for v in graph[u]:
                if v in self.G.nodes and v != u:
                    self.G.add_edge(self.to_int[u], self.to_int[v])
            self.labels.append(u)
            if u not in self.colour_vals: self.colour_vals[u] = 0
    
        self.colour_to_rgb = ["#FFFFFF", "#FFB3B3", "#B3D1FF", "#B3F0B3", "#FFEAA7", "#E1BEE7", "#E0E0E0"]

        # print(colour_vals)
        self.colours = [self.colour_to_rgb[self.colour_vals[self.labels[v]]] for v in range(len(graph))]

        # 2. Verify planarity and get the layout
        is_planar, embedding = nx.check_planarity(self.G)
        if not is_planar:
            raise ValueError("The provided graph is not planar.")

        self.pos = nx.planar_layout(self.G)

        if mode == "spring": self.pos = nx.spring_layout(self.G, k = len(self.to_int)**0.05, pos = self.pos, iterations = 2)

    
        plt.figure(figsize=(8, 6), facecolor="#FAFAFA")
        plt.title("Planar Graph Drawing (Pastel Palette)", color="#4A4A4A")
        plt.ion()
        self.draw()
        
    def draw(self):
        nx.draw(
            self.G,
            self.pos,
            with_labels=True,
            node_color=self.colours,
            node_size=400,
            font_weight="bold",
            font_color="#4A4A4A",  # Dark gray text is softer than pitch black
            edge_color="#CCCCCC",  # Lighter gray for the edges to match the aesthetic
            width=1.5,
            edgecolors='black',     # Color of the thin boundary around each node
            linewidths=0.5,          # Thickness of the boundary
            alpha = 0.8
        )

        plt.ion()
        plt.pause(0.001)
        plt.show()
        sleep(1)

    def update_colour(self, v, c):
        lbl = self.to_int[v]
        self.colour_vals[lbl] = c
        self.colours = [self.colour_to_rgb[self.colour_vals[self.labels[v]]] for v in range(self.G.number_of_nodes())]
        self.draw()


    

# --- Example Usage ---
if __name__ == "__main__":
    N = 10
    
    my_graph = nx.wheel_graph(N)
    vertex_colours = [random.choice(range(5)) for v in range(N)]
    drawing = Planar_Graph_Drawing(my_graph, vertex_colours)

    sleep(10)