from gen_planar import generate_planar_deg5_graph, generate_random_planar_graph
from planar_draw import Planar_Graph_Drawing
import copy
from time import sleep
drawing = None
# g a graph, v a node to delete
# returns the graph obtained by deleting v (does not modify g)
def delete_node(g, v):
    pass

# g a graph, S a node to delete
# returns the graph obtained by contracting S
# and the integer representing the new node

def contract_nodes(g, S):
    pass

def six_colour(g, colours):
    pass

def five_colour(g, colours):
    pass


if __name__ == "__main__":
    g = generate_random_planar_graph(20)
    # g = generate_planar_deg5_graph(20)
    drawing = Planar_Graph_Drawing(g)
    colours = {}
    six_colour(g, colours)
    
    # this makes the program pause for 3 seconds at the end to give you time to actually see the colouring.
    # change the time if its not enough!
    sleep(3)



  

