from DataStructures.List import array_list as lt

def new_heap(is_min_pq=True):
    heap = {
        "elements": lt.new_list(),
        "size": 0,
        "cmp_function": None,
    }
    lt.add_last(heap["elements"], None)  # Índice 0 no se usa
    if is_min_pq:
        heap["cmp_function"] = cmp_function_lower_value
    else:
        heap["cmp_function"] = cmp_function_higher_value
    return heap

def cmp_function_higher_value(father_node, child_node):
    if father_node["key"] >= child_node["key"]:
        return True
    return False

def cmp_function_lower_value(father_node, child_node):
    if father_node["key"] <= child_node["key"]:
        return True
    return False

def size(my_heap):
    return my_heap["size"]

def is_empty(my_heap):
    return my_heap["size"] == 0

def insert(my_heap, element, key):
    my_heap["size"] += 1
    lt.insert_element(my_heap["elements"], {"key": key, "value": element}, my_heap["size"])
    swim(my_heap, my_heap["size"])
    return my_heap

def remove(my_heap):
    if my_heap["size"] > 0:
        min_element = lt.get_element(my_heap["elements"], 1)
        last = lt.get_element(my_heap["elements"], my_heap["size"])
        lt.change_info(my_heap["elements"], 1, last)
        lt.remove_last(my_heap["elements"])
        my_heap["size"] -= 1
        sink(my_heap, 1)
        return min_element["value"]
    return None

def get_first_priority(my_heap):
    if my_heap["size"] > 0:
        return lt.get_element(my_heap["elements"], 1)["value"]
    return None

def swim(my_heap, pos):
    found = False
    while pos > 1 and not found:
        parent = lt.get_element(my_heap["elements"], pos // 2)
        element = lt.get_element(my_heap["elements"], pos)
        if not priority(my_heap, parent, element):
            exchange(my_heap, pos, pos // 2)
        else:
            found = True
        pos = pos // 2

def sink(my_heap, pos):
    size = my_heap["size"]
    while 2 * pos <= size:
        j = 2 * pos
        if j < size:
            if not priority(my_heap, lt.get_element(my_heap["elements"], j), 
                          lt.get_element(my_heap["elements"], j + 1)):
                j += 1
        if priority(my_heap, lt.get_element(my_heap["elements"], pos), 
                   lt.get_element(my_heap["elements"], j)):
            break
        exchange(my_heap, pos, j)
        pos = j

def priority(my_heap, parent, child):
    cmp = my_heap["cmp_function"](parent, child)
    return cmp

def exchange(my_heap, pos_i, pos_j):
    lt.exchange(my_heap["elements"], pos_i, pos_j)