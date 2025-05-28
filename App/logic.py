import time
import sys
import os
import csv

default_limit = 1000000
sys.setrecursionlimit(default_limit * 10)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from DataStructures.List.list_iterator import iterator
from DataStructures.List import array_list as lt 
from DataStructures.Map import map_linear_probing as mp 
from DataStructures.Graph import udgraph as gr 
from DataStructures.Graph import bfs as bfs
from DataStructures.Graph import dfs 
from DataStructures.Stack import stack as st
from DataStructures.Queue import queue as qu
from DataStructures.Graph import dijkstra 
from DataStructures.List import single_linked_list as sll 
from DataStructures.Graph import prim 
from DataStructures.List import array_list as al
from DataStructures.Map import map_linear_probing as lp
data_dir = os.path.dirname(os.path.realpath(__file__)) + "\\Data\\"
csv.field_size_limit(2147483647)
data_dir = os.path.dirname(os.path.realpath("__file__")) + "\\Data\\"
csv.field_size_limit(2147483647)
default_limit = 1000000
sys.setrecursionlimit(default_limit * 10)



def new_logic(size = 1000):
    """
    Crea el catálogo para almacenar las estructuras de datos
    """
    catalog =  {
        'graph': gr.new_graph(size),
        'nodes': lp.new_map(size, 0.5),
        'domiciliarios_ultimos_destinos': lp.new_map(size, 0.5),
        'domiciliarios_ultimos_tiempos': lp.new_map(size, 0.5),
        'restaurant_locations': al.new_list(),
        'delivery_locations': al.new_list(),
        'total_delivery_time': 0.0,
        'total_deliveries': 0,
        'total_edges': 0
    }
    return catalog



def format_location(latitude, longitude):
    try:
        lat = "{0:.4f}".format(float(latitude))
        lon = "{0:.4f}".format(float(longitude))
        return f"{lat}_{lon}"
    except:
        return "0.0000_0.0000"



def load_data(catalog, filename):
    start = get_time()
    persons_map = lp.new_map(1000, 0.5)
    file_path = data_dir + filename
    with open(file_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            origin      = format_location(row['Restaurant_latitude'], row['Restaurant_longitude'])
            dest        = format_location(row['Delivery_location_latitude'], row['Delivery_location_longitude'])
            pid         = row['Delivery_person_ID']
            t_taken     = float(row.get('Time_taken(min)', 0))
            if not gr.contains_vertex(catalog['graph'], origin):
                alist = al.new_list()
                al.add_last(alist, pid)
                gr.insert_vertex(catalog['graph'], origin, alist)
            else:
                alist = gr.get_vertex_information(catalog['graph'], origin)
                al.add_last(alist, pid)
            if not gr.contains_vertex(catalog['graph'], dest):
                alist = al.new_list()
                al.add_last(alist, pid)
                gr.insert_vertex(catalog['graph'], dest, alist)
            else:
                alist = gr.get_vertex_information(catalog['graph'], dest)
                al.add_last(alist, pid)
            catalog['total_deliveries']      += 1
            catalog['total_delivery_time']   += t_taken
            if not lp.contains(persons_map, pid):
                lp.put(persons_map, pid, True)
            if not al.contains(catalog['restaurant_locations'], origin):
                al.add_last(catalog['restaurant_locations'], origin)
            if not al.contains(catalog['delivery_locations'], dest):
                al.add_last(catalog['delivery_locations'], dest)
            e = gr.get_edge(catalog['graph'], origin, dest)
            if e is None:
                avg = t_taken
                catalog['total_edges'] += 1
            else:
                avg = (e['weight'] + t_taken) / 2
            gr.add_edge(catalog['graph'], origin, dest, avg)
            gr.add_edge(catalog['graph'], dest, origin, avg)
            prev_dest = lp.get(catalog['domiciliarios_ultimos_destinos'], pid)
            prev_time = lp.get(catalog['domiciliarios_ultimos_tiempos'], pid)
            if prev_dest and prev_dest != dest:
                avg2 = (prev_time + t_taken) / 2
                e2 = gr.get_edge(catalog['graph'], prev_dest, dest)
                if e2 is None:
                    catalog['total_edges'] += 1
                    gr.add_edge(catalog['graph'], prev_dest, dest, avg2)
                    gr.add_edge(catalog['graph'], dest, prev_dest, avg2)
                else:
                    avg3 = (e2['weight'] + avg2) / 2
                    gr.add_edge(catalog['graph'], prev_dest, dest, avg3)
                    gr.add_edge(catalog['graph'], dest, prev_dest, avg3)
            lp.put(catalog['domiciliarios_ultimos_destinos'], pid, dest)
            lp.put(catalog['domiciliarios_ultimos_tiempos'], pid, t_taken)
    total_doms    = catalog['total_deliveries']
    total_persons = lp.size(persons_map)
    total_nodes   = gr.order(catalog['graph'])
    total_edges   = catalog['total_edges']
    total_rest    = al.size(catalog['restaurant_locations'])
    total_dloc    = al.size(catalog['delivery_locations'])
    avg_time      = (catalog['total_delivery_time'] / total_doms) if total_doms > 0 else 0.0
    end_time = get_time()
    time_elapsed = delta_time(start, end_time)
    return total_doms, total_persons, total_nodes, total_edges, total_rest, total_dloc, avg_time, time_elapsed



def req_1(catalog, A, B):
    """
    Encuentra un camino simple entre dos ubicaciones geográficas
    """
    start = get_time()
    try:
        A = str(A).strip()
        B = str(B).strip()
        if not gr.contains_vertex(catalog['graph'], A):
            end = get_time()
            return {
                'execution_time': delta_time(start, end),
                'points_count': 0,
                'path': al.new_list(),
                'domiciliarios': al.new_list(),
                'restaurants': al.new_list(),
                'message': f'El vértice de origen {A} no existe en el grafo.'
            }
        if not gr.contains_vertex(catalog['graph'], B):
            end = get_time()
            return {
                'execution_time': delta_time(start, end),
                'points_count': 0,
                'path': al.new_list(),
                'domiciliarios': al.new_list(),       
                'restaurants': al.new_list(),
                'message': f'El vértice de destino {B} no existe en el grafo.'
            }
        if A == B:
            path = al.new_list()
            al.add_last(path, A)
            doms = al.new_list()
            try:
                pids_list = gr.get_vertex_information(catalog['graph'], A)
                if pids_list is not None:
                    for i in range(al.size(pids_list)):
                        pid = al.get_element(pids_list, i)
                        if not al.contains(doms, pid):
                            al.add_last(doms, pid)
            except:
                pass
            rests = al.new_list()
            if al.contains(catalog['restaurant_locations'], A):
                al.add_last(rests, A)
            end = get_time()
            return {
                'execution_time': delta_time(start, end),
                'points_count': 1,
                'path': path,
                'domiciliarios': doms,
                'restaurants': rests,
                'message': f'Camino encontrado (mismo punto de origen y destino).'
            }
        search = dfs.dfs(catalog['graph'], A)
        if not dfs.has_path_to(B, search):
            end = get_time()
            return {
                'execution_time': delta_time(start, end),
                'points_count': 0,
                'path': al.new_list(),
                'domiciliarios': al.new_list(),
                'restaurants': al.new_list(),
                'message': f'No hay conexión entre {A} y {B}.'
            }
        path_stack = dfs.path_to(B, search)
        path = al.new_list()
        while not st.is_empty(path_stack):
            al.add_last(path, st.pop(path_stack))
        doms = al.new_list()
        for i in range(al.size(path)):
            loc = al.get_element(path, i)
            try:
                pids_list = gr.get_vertex_information(catalog['graph'], loc)
                if pids_list is not None:
                    for j in range(al.size(pids_list)):
                        pid = al.get_element(pids_list, j)
                        if not al.contains(doms, pid):
                            al.add_last(doms, pid)
            except:
                continue 
        rests = al.new_list()
        for i in range(al.size(path)):
            loc = al.get_element(path, i)
            if al.contains(catalog['restaurant_locations'], loc):
                if not al.contains(rests, loc): 
                    al.add_last(rests, loc)
        end = get_time()
        time_elapsed = delta_time(start, end)
        return {
            'execution_time': round(time_elapsed, 3),
            'points_count': al.size(path),
            'path': path,
            'domiciliarios': doms,
            'restaurants': rests,
            'message': f'Camino encontrado entre {A} y {B}.'
        }
    except Exception as e:
        end = get_time()
        return {
            'execution_time': delta_time(start, end),
            'points_count': 0,
            'path': al.new_list(),
            'domiciliarios': al.new_list(),
            'restaurants': al.new_list(),
            'message': f'Error durante la ejecución: {str(e)}'
        }



def req_2(catalog):
    """Retorna el resultado del requerimiento 2"""
    pass



def req_3(catalog, point_id):
    """
    Domiciliario con más pedidos en un punto geográfico
    """
    start = get_time()
    try:
        point_id = str(point_id).strip()
        graph = catalog['graph']
        if not gr.contains_vertex(graph, point_id):
            end_time = get_time()
            return {
                'tiempo_ms': round(delta_time(start, end_time), 3),
                'domiciliario': None,
                'pedidos': 0,
                'vehiculo': None,
                'error': f"El punto {point_id} no existe en el grafo"
            }
        deliverers_at_point = gr.get_vertex_information(graph, point_id)
        if deliverers_at_point is None or al.size(deliverers_at_point) == 0:
            end_time = get_time()
            return {
                'tiempo_ms': round(delta_time(start, end_time), 3),
                'domiciliario': None,
                'pedidos': 0,
                'vehiculo': None,
                'error': f"No hay domiciliarios registrados en el punto {point_id}"
            }
        courier_counts = lp.new_map(100, 0.5)
        for i in range(al.size(deliverers_at_point)):
            courier_id = al.get_element(deliverers_at_point, i)
            if not lp.contains(courier_counts, courier_id):
                lp.put(courier_counts, courier_id, 1)
            else:
                current_count = lp.get(courier_counts, courier_id)
                lp.put(courier_counts, courier_id, current_count + 1)
        max_courier = None
        max_count = 0
        courier_keys = lp.key_set(courier_counts)
        for i in range(al.size(courier_keys)):
            courier = al.get_element(courier_keys, i)
            count = lp.get(courier_counts, courier)
            if count > max_count:
                max_count = count
                max_courier = courier
        top_vehicle = "motorcycle"
        if max_courier is None:
            end_time = get_time()
            return {
                'tiempo_ms': round(delta_time(start, end_time), 3),
                'domiciliario': None,
                'pedidos': 0,
                'vehiculo': None,
                'error': f"No se pudieron procesar los domiciliarios en el punto {point_id}"
            }
        end_time = get_time()
        elapsed = round(delta_time(start, end_time), 3)
        return {
            'tiempo_ms': elapsed,
            'domiciliario': max_courier,
            'pedidos': max_count,
            'vehiculo': top_vehicle,
            'punto_analizado': point_id,
            'total_domiciliarios_unicos': al.size(courier_keys),
            'error': None
        }
    except Exception as e:
        end_time = get_time()
        return {
            'tiempo_ms': round(delta_time(start, end_time), 3),
            'domiciliario': None,
            'pedidos': 0,
            'vehiculo': None,
            'error': f"Error durante la ejecución: {str(e)}"
        }
        
        
        
def req_4(catalog, A, B):
    """Retorna el resultado del requerimiento 4 de forma determinista usando solo TAD del curso."""
    start = get_time()

    if not gr.contains_vertex(catalog['graph'], A) or not gr.contains_vertex(catalog['graph'], B):
        elapsed = round(delta_time(start, get_time()), 3)
        empty = al.new_list()
        return elapsed, empty, empty

    order = gr.order(catalog['graph'])
    visited = mp.new_map(order, 0.5)
    parent  = mp.new_map(order, 0.5)
    q = qu.new_queue()

    mp.put(visited, A, True)
    mp.put(parent,  A, None)
    qu.enqueue(q, A)

    found = False
    while not qu.is_empty(q):
        u = qu.dequeue(q)
        if u == B:
            found = True
            break
        neighs = gr.adjacents(catalog['graph'], u)
        al.selection_sort(neighs, al.default_sort_criteria)
        for v in iterator(neighs):
            if not mp.contains(visited, v):
                mp.put(visited, v, True)
                mp.put(parent,  v, u)
                qu.enqueue(q, v)

    if not found:
        elapsed = round(delta_time(start, get_time()), 3)
        empty = al.new_list()
        return elapsed, empty, empty
    path_stack = st.new_stack()
    cur = B
    while cur is not None:
        st.push(path_stack, cur)
        cur = mp.get(parent, cur)
    path_alist = al.new_list()
    while not st.is_empty(path_stack):
        al.add_last(path_alist, st.pop(path_stack))

    common = None
    for loc in iterator(path_alist):
        info = gr.get_vertex_information(catalog['graph'], loc) or al.new_list()
        if common is None:
            common = al.new_list()
            for pid in iterator(info):
                if not al.contains(common, pid):
                    al.add_last(common, pid)
        else:
            filtered = al.new_list()
            for pid in iterator(common):
                if al.contains(info, pid):
                    al.add_last(filtered, pid)
            common = filtered

    if common is None:
        common = al.new_list()

    elapsed = round(delta_time(start, get_time()), 3)
    return elapsed, path_alist, common



def req_5(catalog):
    """Retorna el resultado del requerimiento 5"""
    pass



def req_6(catalog, origin):
    """
    Caminos de costo mínimo en tiempo desde un punto A
    """
    start = get_time()
    try:
        origin = str(origin).strip()
        graph = catalog['graph']
        if not gr.contains_vertex(graph, origin):
            end_time = get_time()
            return {
                'tiempo_ms': round(delta_time(start, end_time), 3),
                'cantidad_ubicaciones': 0,
                'alcanzables': al.new_list(),
                'ruta_mas_larga': al.new_list(),
                'tiempo_ruta_mas_larga': 0.0,
                'error': f"El punto {origin} no existe en el grafo"
            }
        search = dijkstra.dijkstra(graph, origin)
        alcanzables = al.new_list()
        all_vertices = gr.vertices(graph)
        for i in range(al.size(all_vertices)):
            vertex = al.get_element(all_vertices, i)
            if dijkstra.has_path_to(vertex, search):
                al.add_last(alcanzables, vertex)
        alcanzables = sort_vertices_alphabetically(alcanzables)
        cantidad = al.size(alcanzables)
        if cantidad == 0:
            end_time = get_time()
            return {
                'tiempo_ms': round(delta_time(start, end_time), 3),
                'cantidad_ubicaciones': 0,
                'alcanzables': alcanzables,
                'ruta_mas_larga': al.new_list(),
                'tiempo_ruta_mas_larga': 0.0,
                'error': f"No hay ubicaciones alcanzables desde {origin}"
            }
        max_vertex = None
        max_time = 0.0
        for i in range(cantidad):
            vertex = al.get_element(alcanzables, i)
            try:
                dist = dijkstra.dist_to(vertex, search)
                if dist > max_time and dist < float('inf'):
                    max_time = dist
                    max_vertex = vertex
            except:
                continue 
        ruta_max = al.new_list()
        if max_vertex is not None:
            try:
                path_stack = dijkstra.path_to(max_vertex, search)
                if path_stack is not None:
                    while not st.is_empty(path_stack):
                        al.add_last(ruta_max, st.pop(path_stack))
            except:
                pass
        end_time = get_time()
        elapsed = round(delta_time(start, end_time), 3)
        return {
            'tiempo_ms': elapsed,
            'cantidad_ubicaciones': cantidad,
            'alcanzables': alcanzables,
            'ruta_mas_larga': ruta_max,
            'tiempo_ruta_mas_larga': max_time,
            'punto_origen': origin,
            'vertice_mas_lejano': max_vertex,
            'error': None
        }
    except Exception as e:
        end_time = get_time()
        return {
            'tiempo_ms': round(delta_time(start, end_time), 3),
            'cantidad_ubicaciones': 0,
            'alcanzables': al.new_list(),
            'ruta_mas_larga': al.new_list(),
            'tiempo_ruta_mas_larga': 0.0,
            'error': f"Error durante la ejecución: {str(e)}"
        }
def sort_vertices_alphabetically(vertex_list):
    """
    Función auxiliar para ordenar vértices alfabéticamente
    """
    if al.size(vertex_list) <= 1:
        return vertex_list
    vertices_py = []
    for i in range(al.size(vertex_list)):
        vertices_py.append(al.get_element(vertex_list, i))
    vertices_py.sort()
    sorted_list = al.new_list()
    for vertex in vertices_py:
        al.add_last(sorted_list, vertex)
    return sorted_list



def req_7(catalog, origin, courier_id):
    """
    Árbol de recubrimiento mínimo para un domiciliario
    """
    start = get_time()
    try:
        origin = str(origin).strip()
        courier_id = str(courier_id).strip()
        graph = catalog['graph']
        if not gr.contains_vertex(graph, origin):
            end_time = get_time()
            return {
                'tiempo_ms': round(delta_time(start, end_time), 3),
                'cantidad_ubicaciones': 0,
                'ubicaciones': al.new_list(),
                'tiempo_total_mst': 0.0,
                'error': f"El punto {origin} no existe en el grafo"
            }
        ubic_set = {}
        courier_found = False
        all_vertices = gr.vertices(graph)
        for i in range(al.size(all_vertices)):
            location = al.get_element(all_vertices, i)
            try:
                deliverers_at_location = gr.get_vertex_information(graph, location)
                if deliverers_at_location is not None:
                    for j in range(al.size(deliverers_at_location)):
                        deliverer = al.get_element(deliverers_at_location, j)
                        if str(deliverer).strip() == courier_id:
                            ubic_set[location] = True
                            courier_found = True
                            break
            except:
                continue 
        if not courier_found:
            end_time = get_time()
            return {
                'tiempo_ms': round(delta_time(start, end_time), 3),
                'cantidad_ubicaciones': 0,
                'ubicaciones': al.new_list(),
                'tiempo_total_mst': 0.0,
                'error': f"El domiciliario {courier_id} no se encontró en ninguna ubicación"
            }
        ubic_set[origin] = True
        ubic_list = al.new_list()
        for location in ubic_set.keys():
            al.add_last(ubic_list, location)
        ubic_list = sort_locations_alphabetically(ubic_list)
        size_ul = al.size(ubic_list)
        if size_ul < 2:
            end_time = get_time()
            return {
                'tiempo_ms': round(delta_time(start, end_time), 3),
                'cantidad_ubicaciones': size_ul,
                'ubicaciones': ubic_list,
                'tiempo_total_mst': 0.0,
                'domiciliario_analizado': courier_id,
                'punto_origen': origin,
                'error': None
            }
        sub_graph = gr.new_graph(size_ul)
        for i in range(size_ul):
            u = al.get_element(ubic_list, i)
            gr.insert_vertex(sub_graph, u, None)
        edges_added = 0
        for i in range(size_ul):
            u = al.get_element(ubic_list, i)
            try:
                adjacents = gr.adjacents(graph, u)
                for j in range(al.size(adjacents)):
                    v = al.get_element(adjacents, j)
                    if v in ubic_set: 
                        edge = gr.get_edge(graph, u, v)
                        if edge is not None:
                            existing_edge = gr.get_edge(sub_graph, u, v)
                            if existing_edge is None:
                                weight = edge['weight'] if isinstance(edge, dict) else edge
                                gr.add_edge(sub_graph, u, v, weight)
                                edges_added += 1
            except:
                continue 
        if edges_added == 0:
            end_time = get_time()
            return {
                'tiempo_ms': round(delta_time(start, end_time), 3),
                'cantidad_ubicaciones': size_ul,
                'ubicaciones': ubic_list,
                'tiempo_total_mst': 0.0,
                'domiciliario_analizado': courier_id,
                'punto_origen': origin,
                'error': "Las ubicaciones del domiciliario no están conectadas"
            }
        try:
            prim_search = prim.prim_mst(sub_graph, origin)
            total_time = prim.weight_mst(sub_graph, prim_search)
        except Exception as e:
            total_time = 0.0
            end_time = get_time()
            return {
                'tiempo_ms': round(delta_time(start, end_time), 3),
                'cantidad_ubicaciones': size_ul,
                'ubicaciones': ubic_list,
                'tiempo_total_mst': 0.0,
                'domiciliario_analizado': courier_id,
                'punto_origen': origin,
                'error': f"Error calculando MST: {str(e)}"
            }
        end_time = get_time()
        elapsed = round(delta_time(start, end_time), 3)
        return {
            'tiempo_ms': elapsed,
            'cantidad_ubicaciones': size_ul,
            'ubicaciones': ubic_list,
            'tiempo_total_mst': total_time,
            'domiciliario_analizado': courier_id,
            'punto_origen': origin,
            'aristas_en_subgrafo': edges_added,
            'error': None
        }
    except Exception as e:
        end_time = get_time()
        return {
            'tiempo_ms': round(delta_time(start, end_time), 3),
            'cantidad_ubicaciones': 0,
            'ubicaciones': al.new_list(),
            'tiempo_total_mst': 0.0,
            'error': f"Error durante la ejecución: {str(e)}"
        }
def sort_locations_alphabetically(location_list):
    """
    Función auxiliar para ordenar ubicaciones alfabéticamente
    """
    if al.size(location_list) <= 1:
        return location_list
    locations_py = []
    for i in range(al.size(location_list)):
        locations_py.append(al.get_element(location_list, i))
    locations_py.sort()
    sorted_list = al.new_list()
    for location in locations_py:
        al.add_last(sorted_list, location)
    return sorted_list


def req_8(catalog):
    """Retorna el resultado del requerimiento 8"""
    pass

# Funciones para medir tiempos de ejecucion
def get_time():
    """devuelve el instante tiempo de procesamiento en milisegundos"""
    return float(time.perf_counter()*1000)

def delta_time(start, end):
    """devuelve la diferencia entre tiempos de procesamiento muestreados"""
    elapsed = float(end - start)
    return elapsed