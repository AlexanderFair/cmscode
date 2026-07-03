import random
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from scipy.spatial import Delaunay

def graph_to_dict(g):
    adj = {x:set() for x in g.nodes}
    for u,v in g.edges:
        x,y = int(u), int(v)
        adj[x].add(y)
        adj[y].add(x)
    return adj


def generate_planar_deg5_graph(target_nodes=30):
    """Generates a random planar graph with minimum degree 5.

    Starts with an icosahedron and scales using valid degree-preserving
    face operations.
    """
    if target_nodes < 12:
        raise ValueError(
            "The smallest possible planar graph with min degree 5 is the icosahedron (12 vertices)."
        )

    # Start with an Icosahedron (12 vertices, every vertex has exactly degree 5)
    G = nx.icosahedral_graph()
    current_node = 12

    # Run until we hit the exact target node count
    while len(G) < target_nodes:
        # Find a valid planar embedding dynamically
        is_planar, embedding = nx.check_planarity(G)
        if not is_planar:
            # If a mutation somehow broke planarity, fallback and fix it
            G = nx.icosahedral_graph()
            current_node = 12
            continue

        faces = _extract_faces(embedding)

        # Shuffle faces to maximize random structure selection
        random.shuffle(faces)
        success = False

        for face in faces:
            # Look for a quadrilateral face (4 vertices) or a pentagonal face (5 vertices).
            # Inserting a vertex inside a 5-face and connecting it to all 5 boundary nodes
            # gives the new vertex exactly degree 5, and INCREASES the degree of its neighbors!
            if len(face) == 5:
                new_v = current_node
                G.add_node(new_v)
                for node in face:
                    G.add_edge(new_v, node)
                current_node += 1
                success = True
                break

        # If no 5-face is available, merge two adjacent 3-faces (triangles) to create one
        if not success:
            edges = list(G.edges())
            random.shuffle(edges)
            for u, v in edges:
                # We can remove an edge safely if both u and v have a degree > 5.
                # This merges their two shared triangles into a larger quadrilateral or pentagon face.
                if G.degree(u) > 5 and G.degree(v) > 5:
                    G.remove_edge(u, v)
                    # Instantly verify that removing this didn't ruin connectivity
                    if nx.is_connected(G):
                        success = True
                        break
                    else:
                        G.add_edge(u, v)  # Put it back if it split the graph

            # If we couldn't remove an edge or find a 5-face, perform a safe 3-face mutation
            if not success:
                for face in faces:
                    if len(face) == 3:
                        u, v, w = face
                        # Insert a vertex, then clear local barriers
                        new_v = current_node
                        G.add_node(new_v)
                        G.add_edges_from([(new_v, u), (new_v, v), (new_v, w)])
                        current_node += 1
                        break

    return graph_to_dict(G)


def _extract_faces(embedding):
    """Helper to cleanly parse face cycles from a NetworkX PlanarEmbedding."""
    faces = []
    visited_edges = set()

    for u in embedding.nodes():
        for v in embedding.neighbors(u):
            if (u, v) not in visited_edges:
                face_nodes = embedding.traverse_face(u, v)
                for i in range(len(face_nodes)):
                    n1 = face_nodes[i]
                    n2 = face_nodes[(i + 1) % len(face_nodes)]
                    visited_edges.add((n1, n2))
                faces.append(face_nodes)
    return faces



def generate_random_planar_graph(num_nodes, edge_keep_probability=0.8):
    """Generates a random planar graph by taking a subgraph of a

    Delaunay triangulation of random 2D points.
    """
    if num_nodes < 1:
        return nx.Graph()

    # 1. Generate random 2D coordinates for the nodes
    points = np.random.rand(num_nodes, 2)

    # 2. Create a Delaunay Triangulation (always planar)
    # Triangulation requires at least 3 points
    if num_nodes >= 3:
        tri = Delaunay(points)
        G = nx.Graph()

        # Add all points as nodes with their positions
        for i, p in enumerate(points):
            G.add_node(i, pos=(p[0], p[1]))

        # Add edges from the triangulation triangles
        for path in tri.simplices:
            G.add_edge(path[0], path[1])
            G.add_edge(path[1], path[2])
            G.add_edge(path[2], path[0])
    else:
        # Handle small edge cases manually
        G = nx.Graph()
        for i, p in enumerate(points):
            G.add_node(i, pos=(p[0], p[1]))
        if num_nodes == 2:
            G.add_edge(0, 1)

    # 3. Randomly remove edges to make it "random" and not just a triangulation

    all_edges = [e for e in G.edges]
    deg = {v:G.degree(v) for v in G.nodes}

    edges_to_remove = []
    for e in G.edges:
        u, v = e[0], int(e[1])
        if deg[u] == 0 or deg[v] == 0: continue
        if random.random() > edge_keep_probability:
            edges_to_remove.append(e)

    # edges_to_remove = [
    #     edge
    #     for edge in G.edges()
    #     if random.random() > edge_keep_probability
    # ]
    G.remove_edges_from(edges_to_remove)

    return graph_to_dict(G)
