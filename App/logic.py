import time
import sys
import os
import csv
from datetime import datetime
import math
import tabulate as tb

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

default_limit=1000000
sys.setrecursionlimit(default_limit*10)

from DataStructures.List.list_iterator import iterator
from DataStructures.List import array_list as al
from DataStructures.Map import map_linear_probing as lp
from DataStructures.Graph import digraph as gr
from DataStructures.Graph import bfs
from DataStructures.Graph import dfs
from DataStructures.Stack import stack as stk
from DataStructures.Graph import udgraph as gr
from DataStructures.List import array_list as al
from DataStructures.List.list_iterator import iterator
from DataStructures.Map import map_linear_probing as lp
from DataStructures.Graph import dijkstra 
from DataStructures.List import single_linked_list as sll
from DataStructures.Graph import prim

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
    time = delta_time(start, end_time)
    return total_doms, total_persons, total_nodes, total_edges, total_rest, total_dloc, avg_time, time

# Funciones de requerimientos restantes (placeholder)
def req_1(catalog, origin, destination):
    """
    Requerimiento 1: Camino simple usando DFS.
    Usa estructuras propias (map, array_list).
    Parámetros:
      - catalog: catálogo con grafo y estructuras.
      - origin: id del punto de inicio.
      - destination: id del punto destino.
    Retorna dict con:
      * tiempo_ms: tiempo de ejecución en ms.
      * nodos: número de ubicaciones en el camino.
      * camino: array_list con la secuencia de ubicaciones.
      * couriers: array_list de domiciliarios únicos.
      * restaurants: array_list de restaurantes en ruta.
    """
    start = get_time()
    # Validaciones
    if not lp.contains(catalog['nodes'], origin):
        raise Exception(f"Punto origen {origin} no existe")
    if not lp.contains(catalog['nodes'], destination):
        raise Exception(f"Punto destino {destination} no existe")
    graph = catalog['graph']
    visited = lp.new_map(gr.order(graph), 0.5)
    ruta_al = al.new_list()
    found_route = {'flag': False, 'path': None}
    def dfs(u: str, target: str, current: any):
        if found_route['flag']:
            return
        lp.put(visited, u, True)
        al.add_last(current, u)
        if u == target:
            found_route['flag'] = True
            # Copiar current a path
            found_route['path'] = al.new_list()
            for node in iterator(current):
                al.add_last(found_route['path'], node)
            return
        for v in iterator(gr.adjacents(graph, u)):
            if not lp.contains(visited, v):
                dfs(v, target, current)
                if found_route['flag']:
                    return
        # backtrack: eliminar último
        # recrear lista sin el último elemento
        tmp = al.new_list()
        size = al.size(current)
        for idx in range(size - 1):
            al.add_last(tmp, al.get_element(current, idx))
        current.clear() if hasattr(current, 'clear') else None
        for node in iterator(tmp):
            al.add_last(current, node)
    dfs(origin, destination, ruta_al)
    if not found_route['flag'] or found_route['path'] is None:
        elapsed = round(delta_time(start, get_time()), 3)
        return {
            'tiempo_ms': elapsed,
            'nodos': 0,
            'camino': al.new_list(),
            'couriers': al.new_list(),
            'restaurants': al.new_list()
        }
    path_found = found_route['path']
    # Extraer couriers y restaurantes
    couriers_map = lp.new_map(10, 0.5)
    restaurants_al = al.new_list()
    for loc in iterator(path_found):
        if lp.contains(catalog['restaurants'], loc):
            al.add_last(restaurants_al, loc)
        vtx = gr.get_vertex(graph, loc)
        for order in iterator(vtx['value']['deliveries']):
            c = lp.get(catalog['order_courier'], order)
            if not lp.contains(couriers_map, c):
                lp.put(couriers_map, c, True)
    couriers_al = al.new_list()
    for c in iterator(lp.key_set(couriers_map)):
        al.add_last(couriers_al, c)

    elapsed = round(delta_time(start, get_time()), 3)
    return {
        'tiempo_ms': elapsed,
        'nodos': al.size(path_found),
        'camino': path_found,
        'couriers': couriers_al,
        'restaurants': restaurants_al
    }


def req_2(catalog):
    """Retorna el resultado del requerimiento 2"""
    pass

def req_3(catalog, point_id):
    """
    Requerimiento 3: Domiciliario con más pedidos en un punto geográfico A.
    Usa mapas lineales para recuentos de pedidos y de vehículos.
    """
    start = get_time()
    # 1) Validación de vértice
    if not lp.contains(catalog['nodes'], point_id):
        raise Exception(f"El punto {point_id} no existe en el catálogo")
    # 2) Obtener la lista de pedidos en ese punto
    vtx = lp.get(catalog['nodes'], point_id)
    deliveries = vtx['value']['deliveries']
    # 3) Mapas para conteos
    courier_counts = lp.new_map(lp.size(catalog['couriers']), 0.5)
    # Mapa de mapas: courier_id -> mapa(vehicle_type -> count)
    vehicle_maps   = lp.new_map(lp.size(catalog['couriers']), 0.5)
    # 4) Recorrer cada pedido registrado en ese punto
    for order_id in iterator(deliveries):
        courier = lp.get(catalog['order_courier'], order_id)
        vehicle = lp.get(catalog['order_vehicle'], order_id)
        # 4a) Contar un pedido más para el courier
        if not lp.contains(courier_counts, courier):
            lp.put(courier_counts, courier, 1)
        else:
            lp.put(courier_counts,
                   courier,
                   lp.get(courier_counts, courier) + 1)
        # 4b) Asegurar que hay un mapa de vehículos para este courier
        if not lp.contains(vehicle_maps, courier):
            lp.put(vehicle_maps, courier, lp.new_map(10, 0.5))
        vm = lp.get(vehicle_maps, courier)
        # 4c) Contar el vehículo
        if not lp.contains(vm, vehicle):
            lp.put(vm, vehicle, 1)
        else:
            lp.put(vm,
                   vehicle,
                   lp.get(vm, vehicle) + 1)
    # 5) Hallar el courier con más pedidos
    max_c, max_count = None, 0
    for c in iterator(lp.key_set(courier_counts)):
        cnt = lp.get(courier_counts, c)
        if cnt > max_count:
            max_count = cnt
            max_c     = c
    # 6) Determinar el vehículo más usado por ese courier
    top_vehicle, veh_count = None, 0
    if max_c is not None:
        vm = lp.get(vehicle_maps, max_c)
        for v in iterator(lp.key_set(vm)):
            vc = lp.get(vm, v)
            if vc > veh_count:
                veh_count   = vc
                top_vehicle = v
    elapsed = round(delta_time(start, get_time()), 3)
    return {
        'tiempo_ms': elapsed,
        'domiciliario': max_c,
        'pedidos':      max_count,
        'vehiculo':     top_vehicle
    }


def req_4(catalog):
    """Retorna el resultado del requerimiento 4"""
    pass

def req_5(catalog):
    """Retorna el resultado del requerimiento 5"""
    pass

def req_6(catalog, origin):
    """
    Requerimiento 6: Caminos de costo mínimo en tiempo desde un punto A.
    """
    start = get_time()
    if not lp.contains(catalog['nodes'], origin):
        raise Exception(f"El punto {origin} no existe en el catálogo")
    graph = catalog['graph']
    search = dijkstra.dijkstra(graph, origin)
    # Crear lista de alcanzables
    alcanzables = sll.new_list()
    for v in iterator(gr.vertices(graph)):
        if dijkstra.has_path_to(v, search):
            sll.add_last(alcanzables, v)
    # Ordenar lista alcanzables alfabéticamente usando insertion sort
    def compare(v1, v2):
        return v1 < v2  # orden lexicográfico
    alcanzables = sll.insertion_sort(alcanzables, compare)
    # Contar cantidad de elementos en alcanzables
    cantidad = 0
    for _ in iterator(alcanzables):
        cantidad += 1
    # Buscar el vértice más lejano (con mayor dist_to)
    max_v = None
    max_t = 0.0
    for v in iterator(alcanzables):
        t = dijkstra.dist_to(v, search)
        if t > max_t:
            max_t = t
            max_v = v
    # Recuperar la ruta hacia max_v
    ruta_max = sll.new_list()
    if max_v is not None:
        stack = dijkstra.path_to(max_v, search)
        while not stack.is_empty():
            sll.add_last(ruta_max, stack.pop())

    elapsed = round(delta_time(start, get_time()), 3)
    return {
        'tiempo_ms': elapsed,
        'cantidad_ubicaciones': cantidad,
        'alcanzables': alcanzables,
        'ruta_mas_larga': ruta_max,
        'tiempo_ruta_mas_larga': max_t
    }

def req_7(catalog: dict, origin: str, courier_id: str) -> dict:
    """
    Requerimiento 7: Árbol de recubrimiento mínimo para un domiciliario.
    Parámetros:
      - catalog: catálogo con grafo y estructuras auxiliares.
      - origin: id del punto geográfico de partida.
      - courier_id: identificador del domiciliario.
    Retorna dict con:
      * tiempo_ms: tiempo de ejecución en ms.
      * cantidad_ubicaciones: número de ubicaciones en la sub-red.
      * ubicaciones: array_list alfabetizada de ids de la sub-red.
      * tiempo_total_mst: peso total del árbol de costo mínimo.
    """
    start = get_time()
    # Validaciones
    if not lp.contains(catalog['nodes'], origin):
        raise Exception(f"Punto {origin} no existe en el catálogo")
    if not lp.contains(catalog['couriers'], courier_id):
        raise Exception(f"Domiciliario {courier_id} no está registrado")
    graph = catalog['graph']
    # 1) Recolectar ubicaciones en las que entregó el courier
    ubic_map = lp.new_map(lp.size(catalog['nodes']), 0.5)
    for loc in iterator(gr.vertices(graph)):
        vtx = gr.get_vertex(graph, loc)
        for order in iterator(vtx['value']['deliveries']):
            if lp.get(catalog['order_courier'], order) == courier_id:
                lp.put(ubic_map, loc, True)
    # Incluir origen
    lp.put(ubic_map, origin, True)
    # 2) Convertir keys del map a array_list
    ubic_list = al.new_list()
    for loc in iterator(lp.key_set(ubic_map)):
        al.add_last(ubic_list, loc)
    # 3) Ordenar ubic_list alfabéticamente con insertion sort
    def compare(a, b): return a < b
    ubic_list = al.insertion_sort(ubic_list, compare)
    # 4) Construir subgrafo inducido
    size_ul = al.size(ubic_list)
    sub_g = gr.new_graph(size_ul)
    # Insertar vértices
    for i in range(size_ul):
        u = al.get_element(ubic_list, i)
        gr.insert_vertex(sub_g, u, None)
    # Insertar aristas
    for i in range(size_ul):
        u = al.get_element(ubic_list, i)
        for v in iterator(gr.adjacents(graph, u)):
            if lp.contains(ubic_map, v):
                edge = gr.get_edge(graph, u, v)
                gr.add_edge(sub_g, u, v, edge['weight'])
    # 5) Calcular MST con Prim y peso total
    prim_search = prim.prim_mst(sub_g, origin)
    total_time = prim.weight_mst(sub_g, prim_search)
    # 6) Contar ubicaciones
    cantidad = al.size(ubic_list)
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


catalog = new_logic(1)

load_data(catalog, "deliverytime_min.csv")
print(req_1(catalog, "22.7452_75.9161", "22.7352_75.9061"))