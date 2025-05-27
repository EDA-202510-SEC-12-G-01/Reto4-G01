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

data_dir = os.path.dirname(os.path.realpath("__file__")) + "\\Data\\"

csv.field_size_limit(2147483647)


default_limit = 1000000
sys.setrecursionlimit(default_limit * 10)

def get_time():
    return float(time.perf_counter() * 1000)

def delta_time(start, end):
    return float(end - start)

def new_logic(size=1):
    """
    Crea el catálogo para almacenar las estructuras de datos
    """
    catalog =  {
        'graph': gr.new_graph(10000),
        'nodes': lp.new_map(2000, 0.5),
        'domiciliarios_ultimos_destinos': lp.new_map(1000, 0.5),
        'domiciliarios_ultimos_tiempos': lp.new_map(1000, 0.5),
        'restaurant_locations': al.new_list(),
        'delivery_locations': al.new_list(),
        'total_delivery_time': 0.0,
        'total_deliveries': 0,
        'total_edges': 0,
        'load_time': 0.0
    }
    return catalog

def format_location(latitude, longitude):
    try:
        lat = "{0:.4f}".format(float(latitude))
        lon = "{0:.4f}".format(float(longitude))
        return f"{lat}_{lon}"
    except:
        return "0.0000_0.0000"

def list_contains(lst, value):
    """Comprueba si value está en el array_list lst."""
    for element in lst['elements']:
        if element == value:
            return True
    return False

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

            # ——— Nodos ———
            # origen
            if not gr.contains_vertex(catalog['graph'], origin):
                alist = al.new_list()
                al.add_last(alist, pid)
                gr.insert_vertex(catalog['graph'], origin, alist)
            else:
                alist = gr.get_vertex_information(catalog['graph'], origin)
                al.add_last(alist, pid)
            # destino
            if not gr.contains_vertex(catalog['graph'], dest):
                alist = al.new_list()
                al.add_last(alist, pid)
                gr.insert_vertex(catalog['graph'], dest, alist)
            else:
                alist = gr.get_vertex_information(catalog['graph'], dest)
                al.add_last(alist, pid)

            # ——— Contadores ———
            catalog['total_deliveries']      += 1
            catalog['total_delivery_time']   += t_taken
            # domiciliario único
            if not lp.contains(persons_map, pid):
                lp.put(persons_map, pid, True)

            # ubicaciones únicas de restaurantes y destinos
            if not list_contains(catalog['restaurant_locations'], origin):
                al.add_last(catalog['restaurant_locations'], origin)
            if not list_contains(catalog['delivery_locations'], dest):
                al.add_last(catalog['delivery_locations'], dest)

            # ——— Arcos (no dirigidos) ———
            # principal: origen <-> destino
            e = gr.get_edge(catalog['graph'], origin, dest)
            if e is None:
                avg = t_taken
                catalog['total_edges'] += 1
            else:
                avg = (e['weight'] + t_taken) / 2
            gr.add_edge(catalog['graph'], origin, dest, avg)
            gr.add_edge(catalog['graph'], dest, origin, avg)

            # arco entre entregas consecutivas de un mismo domiciliario
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

    catalog['load_time'] = delta_time(start, get_time())

    # ——— Resultados ———
    total_doms    = catalog['total_deliveries']
    total_persons = lp.size(persons_map)
    total_nodes   = gr.order(catalog['graph'])
    total_edges   = catalog['total_edges']
    total_rest    = al.size(catalog['restaurant_locations'])
    total_dloc    = al.size(catalog['delivery_locations'])
    avg_time      = (catalog['total_delivery_time'] / total_doms) if total_doms > 0 else 0.0

    return total_doms, total_persons, total_nodes, total_edges, total_rest, total_dloc, avg_time

# Funciones de requerimientos restantes (placeholder)
def req_1(catalog, A, B):
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

catalog = new_logic(1)

print(load_data(catalog, "deliverytime_100.csv"))

