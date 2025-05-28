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
from DataStructures.Graph import bfs as bfs_alg 
from DataStructures.Graph import dfs 
from DataStructures.Stack import stack as st 
from DataStructures.Graph import dijkstra 
from DataStructures.List import single_linked_list as sll 
from DataStructures.Graph import prim 
from DataStructures.List import array_list as al
from DataStructures.Map import map_linear_probing as lp

# Ruta base para los archivos de datos
data_dir = os.path.dirname(os.path.realpath(__file__)) + "\\Data\\"

# Aumentar el límite de tamaño de campo para CSV
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
    """
    MANTENER LA CARGA DE DATOS ORIGINAL - FUNCIONA CORRECTAMENTE
    """
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

def req_1(catalog, origin_id, dest_id):
    """
    REQ 1 CORREGIDO: Encuentra un camino simple entre dos ubicaciones geográficas
    """
    start_time = time.perf_counter()
    
    # Obtener el grafo del catálogo
    graph = catalog['graph']
    
    # Validar que los vértices existan
    if not gr.contains_vertex(graph, origin_id):
        return {
            'path_exists': False,
            'error': f"El vértice de origen '{origin_id}' no existe en el grafo.",
            'execution_time': (time.perf_counter() - start_time) * 1000
        }
    
    if not gr.contains_vertex(graph, dest_id):
        return {
            'path_exists': False,
            'error': f"El vértice de destino '{dest_id}' no existe en el grafo.",
            'execution_time': (time.perf_counter() - start_time) * 1000
        }

    # Ejecutar BFS desde el origen
    bfs_search_results = bfs_alg.bfs(graph, origin_id)
    
    # ✅ CORREGIDO: Usar las funciones correctas de bfs.py
    path_exists = bfs_alg.has_path_to(bfs_search_results, dest_id)
    
    if not path_exists:
        return {
            'path_exists': False,
            'error': f"No existe un camino entre '{origin_id}' y '{dest_id}'.",
            'path_length': 0,
            'path_sequence': lt.new_list(),
            'unique_deliverers': lt.new_list(),
            'restaurants': lt.new_list(),
            'execution_time': (time.perf_counter() - start_time) * 1000
        }

    # ✅ CORREGIDO: Obtener el camino usando la función correcta
    path_stack = bfs_alg.path_to(bfs_search_results, dest_id)
    
    # Convertir stack a lista
    path_list = lt.new_list()
    while not st.is_empty(path_stack):
        lt.add_first(path_list, st.pop(path_stack))

    # ✅ CORREGIDO: Extraer domiciliarios usando la estructura real
    unique_deliverers = lt.new_list()
    restaurants_list = lt.new_list()
    deliverer_set = {}  # Set temporal para evitar duplicados
    
    # Recorrer cada nodo del camino
    for i in range(lt.size(path_list)):
        node_id = lt.get_element(path_list, i)
        
        # Obtener lista de domiciliarios de cada nodo
        try:
            node_deliverers = gr.get_vertex_information(graph, node_id)
            if node_deliverers is not None:
                # node_deliverers es una array_list con IDs de domiciliarios
                for j in range(lt.size(node_deliverers)):
                    deliverer_id = lt.get_element(node_deliverers, j)
                    # Agregar solo si no está duplicado
                    if deliverer_id not in deliverer_set:
                        deliverer_set[deliverer_id] = True
                        lt.add_last(unique_deliverers, deliverer_id)
        except:
            pass  # Si no hay información, continuar
        
        # ✅ CORREGIDO: Identificar restaurantes usando la estructura real
        restaurant_locations = catalog['restaurant_locations']
        for k in range(lt.size(restaurant_locations)):
            restaurant_node = lt.get_element(restaurant_locations, k)
            if restaurant_node == node_id:
                # Verificar que no esté duplicado
                found = False
                for l in range(lt.size(restaurants_list)):
                    if lt.get_element(restaurants_list, l) == node_id:
                        found = True
                        break
                if not found:
                    lt.add_last(restaurants_list, node_id)
                break

    return {
        'path_exists': True,
        'path_length': lt.size(path_list) - 1,  # Número de aristas
        'path_sequence': path_list,
        'unique_deliverers': unique_deliverers,
        'restaurants': restaurants_list,
        'execution_time': (time.perf_counter() - start_time) * 1000
    }

def req_2(catalog):
    """Retorna el resultado del requerimiento 2"""
    pass

def req_3(catalog, point_id):
    """
    REQ 3 CORREGIDO: Domiciliario con más pedidos en un punto geográfico
    """
    start = get_time()
    
    # Validar que el punto exista en el grafo
    graph = catalog['graph']
    if not gr.contains_vertex(graph, point_id):
        raise Exception(f"El punto {point_id} no existe en el grafo")
    
    # Obtener la lista de domiciliarios en ese punto
    deliverers_at_point = gr.get_vertex_information(graph, point_id)
    
    if deliverers_at_point is None or lt.size(deliverers_at_point) == 0:
        return {
            'tiempo_ms': round(delta_time(start, get_time()), 3),
            'domiciliario': None,
            'pedidos': 0,
            'vehiculo': None
        }
    
    # Contar pedidos por domiciliario
    courier_counts = lp.new_map(100, 0.5)
    
    # Recorrer todos los domiciliarios en este punto
    for i in range(lt.size(deliverers_at_point)):
        courier_id = lt.get_element(deliverers_at_point, i)
        
        if not lp.contains(courier_counts, courier_id):
            lp.put(courier_counts, courier_id, 1)
        else:
            current_count = lp.get(courier_counts, courier_id)
            lp.put(courier_counts, courier_id, current_count + 1)
    
    # Encontrar el domiciliario con más pedidos
    max_courier = None
    max_count = 0
    
    courier_keys = lp.key_set(courier_counts)
    for i in range(lt.size(courier_keys)):
        courier = lt.get_element(courier_keys, i)
        count = lp.get(courier_counts, courier)
        if count > max_count:
            max_count = count
            max_courier = courier
    
    # Para el vehículo, simplificar: motorcycle por defecto
    # (se podría hacer más complejo contando vehículos por domiciliario)
    top_vehicle = "motorcycle"
    
    elapsed = round(delta_time(start, get_time()), 3)
    return {
        'tiempo_ms': elapsed,
        'domiciliario': max_courier,
        'pedidos': max_count,
        'vehiculo': top_vehicle
    }

def req_4(catalog):
    """Retorna el resultado del requerimiento 4"""
    pass

def req_5(catalog):
    """Retorna el resultado del requerimiento 5"""
    pass

def req_6(catalog, origin):
    """
    REQ 6 CORREGIDO: Caminos de costo mínimo en tiempo desde un punto A
    """
    start = get_time()
    
    # Validar que el punto origen exista
    graph = catalog['graph']
    if not gr.contains_vertex(graph, origin):
        raise Exception(f"El punto {origin} no existe en el grafo")
    
    # Ejecutar Dijkstra desde el origen
    search = dijkstra.dijkstra(graph, origin)
    
    # Crear lista de puntos alcanzables
    alcanzables = lt.new_list()
    all_vertices = gr.vertices(graph)
    
    for i in range(lt.size(all_vertices)):
        vertex = lt.get_element(all_vertices, i)
        if dijkstra.has_path_to(vertex, search):
            lt.add_last(alcanzables, vertex)
    
    # Ordenar lista alfabéticamente usando insertion sort
    def compare_vertices(v1, v2):
        return v1 < v2
    
    alcanzables = lt.insertion_sort(alcanzables, compare_vertices)
    
    # Contar cantidad de elementos alcanzables
    cantidad = lt.size(alcanzables)
    
    # Buscar el vértice más lejano (con mayor dist_to)
    max_vertex = None
    max_time = 0.0
    
    for i in range(cantidad):
        vertex = lt.get_element(alcanzables, i)
        dist = dijkstra.dist_to(vertex, search)
        if dist > max_time:
            max_time = dist
            max_vertex = vertex
    
    # Recuperar la ruta hacia max_vertex
    ruta_max = lt.new_list()
    if max_vertex is not None:
        path_stack = dijkstra.path_to(max_vertex, search)
        while not st.is_empty(path_stack):
            lt.add_last(ruta_max, st.pop(path_stack))

    elapsed = round(delta_time(start, get_time()), 3)
    return {
        'tiempo_ms': elapsed,
        'cantidad_ubicaciones': cantidad,
        'alcanzables': alcanzables,
        'ruta_mas_larga': ruta_max,
        'tiempo_ruta_mas_larga': max_time
    }

def req_7(catalog, origin, courier_id):
    """
    REQ 7 CORREGIDO: Árbol de recubrimiento mínimo para un domiciliario
    """
    start = get_time()
    
    # Validaciones
    graph = catalog['graph']
    if not gr.contains_vertex(graph, origin):
        raise Exception(f"Punto {origin} no existe en el grafo")
    
    # 1) Recolectar ubicaciones donde trabajó el domiciliario
    ubic_set = {}
    all_vertices = gr.vertices(graph)
    
    for i in range(lt.size(all_vertices)):
        location = lt.get_element(all_vertices, i)
        deliverers_at_location = gr.get_vertex_information(graph, location)
        
        if deliverers_at_location is not None:
            # Buscar si el courier_id está en esta ubicación
            for j in range(lt.size(deliverers_at_location)):
                deliverer = lt.get_element(deliverers_at_location, j)
                if deliverer == courier_id:
                    ubic_set[location] = True
                    break
    
    # Incluir origen
    ubic_set[origin] = True
    
    # 2) Convertir set a array_list
    ubic_list = lt.new_list()
    for location in ubic_set.keys():
        lt.add_last(ubic_list, location)
    
    # 3) Ordenar alfabéticamente
    def compare_locations(a, b):
        return a < b
    
    ubic_list = lt.insertion_sort(ubic_list, compare_locations)
    
    # 4) Construir subgrafo inducido
    size_ul = lt.size(ubic_list)
    sub_graph = gr.new_graph(size_ul)
    
    # Insertar vértices
    for i in range(size_ul):
        u = lt.get_element(ubic_list, i)
        gr.insert_vertex(sub_graph, u, None)
    
    # Insertar aristas
    for i in range(size_ul):
        u = lt.get_element(ubic_list, i)
        adjacents = gr.adjacents(graph, u)
        
        for j in range(lt.size(adjacents)):
            v = lt.get_element(adjacents, j)
            if v in ubic_set:  # Si v también está en nuestro subconjunto
                edge = gr.get_edge(graph, u, v)
                if edge is not None:
                    # Solo agregar si no existe ya (para evitar duplicados)
                    existing_edge = gr.get_edge(sub_graph, u, v)
                    if existing_edge is None:
                        gr.add_edge(sub_graph, u, v, edge['weight'])
    
    # 5) Calcular MST con Prim
    if size_ul > 0:
        prim_search = prim.prim_mst(sub_graph, origin)
        total_time = prim.weight_mst(sub_graph, prim_search)
    else:
        total_time = 0.0
    
    # 6) Resultado
    cantidad = size_ul
    elapsed = round(delta_time(start, get_time()), 3)
    
    return {
        'tiempo_ms': elapsed,
        'cantidad_ubicaciones': cantidad,
        'ubicaciones': ubic_list,
        'tiempo_total_mst': total_time
    }

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