from DataStructures.Graph import edge as ed
from DataStructures.Graph import vertex as vt
from DataStructures.Graph import digraph as G

from DataStructures.List import array_list as al
from DataStructures.List.list_iterator import iterator
from DataStructures.Map import map_linear_probing as mlp
from DataStructures.Stack import stack as s

def dfo(my_graph):
    marked = mlp.new_map(G.order(my_graph), 0.7)
    pre = al.new_list()
    post = al.new_list()
    reversepost = s.new_stack()
    aux = {
        'marked': marked,
        'pre': pre,
        'post': post,
        'reversepost': reversepost
    }
    
    def dfs_vertex(my_graph, v_key, aux):
        mlp.put(aux['marked'], v_key, True)
        al.add_last(aux['pre'], v_key)
        adjacents_keys = G.adjacents(my_graph, v_key)
        for w in iterator(adjacents_keys):
            if not mlp.contains(aux['marked'], w) or mlp.get(aux['marked'], w) is None:
                dfs_vertex(my_graph, w, aux)
        al.add_last(aux['post'], v_key)
        s.push(aux['reversepost'], v_key)
    for v_key in iterator(G.vertices(my_graph)):
        if not mlp.contains(marked, v_key) or mlp.get(marked, v_key) is None:
            dfs_vertex(my_graph, v_key, aux)
    return aux