import sys
import os
import csv
import time
import math
from datetime import datetime
import tabulate as tb

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
default_limit = 1_000_000
sys.setrecursionlimit(default_limit * 10)

from DataStructures.Graph import udgraph as gr
from DataStructures.List import array_list as al
from DataStructures.List.list_iterator import iterator
from DataStructures.Map import map_linear_probing as lp

data_dir = os.path.dirname(os.path.realpath("__file__")) + "\\Data\\"
csv.field_size_limit(2_147_483_647)        # 2 GB

# creación del catálogo
def new_logic(size = 1000):
    """
    Crea el catalogo para almacenar las estructuras de datos
    """
    return {
        'graph'                : gr.new_graph(size),
        'nodes'                : lp.new_map(size, 0.5),      # loc_id -> vertex
        'couriers_last_dest'   : lp.new_map(size, 0.5),      # Delivery_person_ID -> loc_id
        'couriers_last_time'   : lp.new_map(size, 0.5),      # Delivery_person_ID -> tiempo
        'couriers'             : lp.new_map(size, 0.5),      # set lógico de couriers
        'restaurants'          : lp.new_map(size, 0.5),      # set lógico de orígenes
        'destinations'         : lp.new_map(size, 0.5),      # set lógico de destinos
        'edges_stats'          : {},                         # (u,v) tuple ordenada -> [∑pesos, n]
        'total_delivery_time'  : 0.0,
        'total_deliveries'     : 0
    }

def format_location(latitude: str, longitude: str) -> str:
    try:
        lat = "{0:.4f}".format(float(latitude))
        lon = "{0:.4f}".format(float(longitude))
    except:
        lat, lon = "0.0000", "0.0000"
    return f"{lat}_{lon}"


def vertex_deliveries(vertex_dict):
    return vertex_dict['value']['deliveries']


def get_or_create_vertex(catalog: dict, loc_id: str):
    nodes = catalog['nodes']
    graph = catalog['graph']

    if lp.contains(nodes, loc_id):
        return lp.get(nodes, loc_id)

    value = {'deliveries': al.new_list()}
    gr.insert_vertex(graph, loc_id, value)
    vtx = gr.get_vertex(graph, loc_id)
    lp.put(nodes, loc_id, vtx)
    return vtx


def update_edge_weight(catalog: dict, u: str, v: str, new_weight: float):
    if u == v:
        return
    key = (u, v) if u < v else (v, u)
    stats = catalog['edges_stats']
    if key in stats:
        suma, cnt = stats[key]
        suma += new_weight
        cnt  += 1
        stats[key] = [suma, cnt]
        avg = suma / cnt
        gr.add_edge(catalog['graph'], u, v, avg)
    else:
        stats[key] = [new_weight, 1]
        gr.add_edge(catalog['graph'], u, v, new_weight)

# Funciones para la carga de datos
def load_data(catalog: dict, filename: str):
    """
    Procesa el CSV indicado y devuelve una tupla con:
      (domicilios_total, domiciliarios_total, nodos, arcos,
       restaurantes_unicos, destinos_unicos, tiempo_promedio, tiempo_carga_ms)
    """
    start_time = get_time()
    path = os.path.join(data_dir, filename)

    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            order_id  = row.get('ID') or 'Unknown'
            courier   = row.get('Delivery_person_ID') or 'Unknown'
            t_taken   = float(row.get('Time_taken(min)', '0') or 0)

            loc_org = format_location(row.get('Restaurant_latitude'),
                                       row.get('Restaurant_longitude'))
            loc_dst = format_location(row.get('Delivery_location_latitude'),
                                       row.get('Delivery_location_longitude'))
            
            catalog['total_deliveries']    += 1
            catalog['total_delivery_time'] += t_taken

            if not lp.contains(catalog['couriers'], courier):
                lp.put(catalog['couriers'], courier, True)

            if not lp.contains(catalog['restaurants'], loc_org):
                lp.put(catalog['restaurants'], loc_org, True)

            if not lp.contains(catalog['destinations'], loc_dst):
                lp.put(catalog['destinations'], loc_dst, True)

            v_org = get_or_create_vertex(catalog, loc_org)
            v_dst = get_or_create_vertex(catalog, loc_dst)

            al.add_last(vertex_deliveries(v_org), order_id)
            al.add_last(vertex_deliveries(v_dst), order_id)

            update_edge_weight(catalog, loc_org, loc_dst, t_taken)

            last_dest = lp.get(catalog['couriers_last_dest'], courier) \
                        if lp.contains(catalog['couriers_last_dest'], courier) else None

            if last_dest and last_dest != loc_dst:
                last_time = lp.get(catalog['couriers_last_time'], courier)
                avg_time  = (last_time + t_taken) / 2
                update_edge_weight(catalog, last_dest, loc_dst, avg_time)

            lp.put(catalog['couriers_last_dest'],  courier, loc_dst)
            lp.put(catalog['couriers_last_time'],  courier, t_taken)

    domicilios_total     = catalog['total_deliveries']
    domiciliarios_total  = lp.size(catalog['couriers'])
    nodos_total          = gr.order(catalog['graph'])
    arcos_total          = gr.size(catalog['graph'])
    restaurantes_total   = lp.size(catalog['restaurants'])
    destinos_total       = lp.size(catalog['destinations'])
    tiempo_promedio      = (catalog['total_delivery_time'] / domicilios_total if domicilios_total else 0.0)
    end_time = get_time()
    
    tiempo_carga_ms = round(delta_time(start_time, end_time), 3)

    return domicilios_total, domiciliarios_total, nodos_total, arcos_total, restaurantes_total, destinos_total, tiempo_promedio, tiempo_carga_ms

# Funciones de requerimientos restantes (placeholder)
def req_1(catalog):
    """Retorna el resultado del requerimiento 1"""
    pass

def req_2(catalog):
    """Retorna el resultado del requerimiento 2"""
    pass

def req_3(catalog):
    """Retorna el resultado del requerimiento 3"""
    pass

def req_4(catalog):
    """Retorna el resultado del requerimiento 4"""
    pass

def req_5(catalog):
    """Retorna el resultado del requerimiento 5"""
    pass

def req_6(catalog):
    """Retorna el resultado del requerimiento 6"""
    pass

def req_7(catalog):
    """Retorna el resultado del requerimiento 7"""
    pass

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