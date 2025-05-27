from DataStructures.Graph import edge as ed
from DataStructures.Graph import vertex as vt
from DataStructures.Graph import digraph as G  # Usar tu digraph.py

from DataStructures.List import array_list as al
from DataStructures.List.list_iterator import iterator
from DataStructures.Map import map_linear_probing as mlp
from DataStructures.Stack import stack as s

def dfs(my_graph, source):
    if not G.contains_vertex(my_graph, source):
        raise Exception("El vertice source no existe")
    
    marked = mlp.new_map(G.order(my_graph), 0.7)
    edge_to = mlp.new_map(G.order(my_graph), 0.7)
    pre = al.new_list()
    post = al.new_list()
    reversepost = s.new_stack()

    def dfs_vertex(v_key):
        mlp.put(marked, v_key, True)
        al.add_last(pre, v_key)
        
        adjacents_keys = G.adjacents(my_graph, v_key)
        for w in iterator(adjacents_keys):
            if not mlp.contains(marked, w) or mlp.get(marked, w) is None:
                mlp.put(edge_to, w, v_key)
                dfs_vertex(w)
        
        al.add_last(post, v_key)
        s.push(reversepost, v_key)
    
    dfs_vertex(source)

    return {
        'pre': pre,
        'post': post,
        'reversepost': reversepost,
        'edge_to': edge_to,
        'marked': marked
    }

def has_path_to(search, key_v):
    marked = search['marked']
    return mlp.contains(marked, key_v) and mlp.get(marked, key_v) is True

def path_to(search, key_v):
    if not has_path_to(search, key_v):
        return None
    
    path = s.new_stack()
    edge_to = search['edge_to']
    v = key_v
    
    while mlp.contains(edge_to, v) and mlp.get(edge_to, v) is not None:
        s.push(path, v)
        v = mlp.get(edge_to, v)
    s.push(path, v)
    
    return path