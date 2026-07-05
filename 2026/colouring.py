from gen_planar import generate_planar_deg5_graph, generate_random_planar_graph
from planar_draw import Planar_Graph_Drawing
import copy
drawing = None
# g a graph, v a node to delete
# returns the graph obtained by deleting v (does not modify g)
def delete_node(g, v):
  h = copy.deepcopy(g)

  for u in h: h[u].discard(v)
  h.pop(v)

  return h

# g a graph, S a node to delete
# returns the graph obtained by contracting S
# and the integer representing the new node

def contract_nodes(g, S):
  h = copy.deepcopy(g)
  newnode = max(g.keys()) + 1
  
  h[newnode] = set()
  for u in h:
    if u not in S and h[u].intersection(S):
      h[newnode].add(u)
      h[u].add(newnode)
      h[u].difference_update(S)
  for u in S: h.pop(u)

  return h, newnode

def six_colour(g, colours):
  if not g: return

  v = None

  for u in g:
    if len(g[u]) <= 5:
      v = u
  
  assert v is not None

  h = delete_node(g, v)

  six_colour(h, colours)

  used = [colours[u] for u in g[v]]
  colours[v] = 1
  while colours[v] in used: colours[v] += 1
  assert colours[v] <= 6
  drawing.update_colour(v, colours[v])

def five_colour(g, colours):
  if not g: return

  v = None

  for u in g:
    if len(g[u]) <= 5:
      v = u

      # makes it so we can test this method
      if len(g[u]) == 5: break 
  
  assert v is not None

  if len(g[v]) < 5:
    h = delete_node(g, v)
    five_colour(h, colours)
  else:
    u = w = None
    for a in g[v]:
      for b in g[v]:
        if a != b and b not in g[a]:
          u, w = a, b
    assert u is not None

    h, vS = contract_nodes(g, {u,v,w})
    five_colour(h, colours)
    colours[u] = colours[w] = colours[vS]
    drawing.update_colour(u, colours[vS])
    drawing.update_colour(w, colours[vS])
    colours.pop(vS)
  
  # either case, we now have that v only sees <= 4 colours
  # among its neighbours
  used = [colours[u] for u in g[v]]
  colours[v] = 1
  while colours[v] in used: colours[v] += 1
  assert colours[v] <= 5



if __name__ == "__main__":
  g = generate_random_planar_graph(20)
  # g = generate_planar_deg5_graph(20)
  drawing = Planar_Graph_Drawing(g)
  colours = {}

  six_colour(g, colours)

  # "planar" is guaranteed to be a planar drawing but
  # it can be a bit nasty
  # "spring" starts with a planar embedding but then runs
  # a "springs" routine to try and separate nodes, it might create crossings

  # draw_planar_graph(g, colours, "planar")
  # draw_planar_graph(g, colours, "spring")


  

