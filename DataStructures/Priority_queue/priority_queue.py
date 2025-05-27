from DataStructures.List import array_list as lt

def new_heap(is_min_pq=True):
    """
    Crea un nuevo heap (cola de prioridad)
    """
    heap = {
        'elements': lt.new_list(),
        'size': 0,
        'is_min_heap': is_min_pq
    }
    return heap

def size(my_heap):
    """
    Retorna el tamaño del heap
    """
    return my_heap['size']

def is_empty(my_heap):
    """
    Verifica si el heap está vacío
    """
    return my_heap['size'] == 0

def swim(my_heap, pos):
    """
    Reestablecer propiedad del heap hacia arriba
    """
    while pos > 1:
        parent_pos = pos // 2
        parent = lt.get_element(my_heap["elements"], parent_pos - 1)
        child = lt.get_element(my_heap["elements"], pos - 1)
        
        # Para min-heap: hijo < padre, para max-heap: hijo > padre
        should_swap = False
        if my_heap['is_min_heap']:
            should_swap = child['key'] < parent['key']
        else:
            should_swap = child['key'] > parent['key']
        
        if should_swap:
            lt.exchange(my_heap["elements"], pos - 1, parent_pos - 1)
            pos = parent_pos
        else:
            break
    return my_heap

def sink(my_heap, pos):
    """
    Reestablecer propiedad del heap hacia abajo
    """
    elements_list = my_heap['elements']
    heap_size = my_heap['size']
    
    while 2 * pos <= heap_size:
        left = 2 * pos
        right = left + 1
        extremo = pos
        
        current_key = lt.get_element(elements_list, extremo - 1)['key']
        
        if left <= heap_size:
            left_key = lt.get_element(elements_list, left - 1)['key']
            if my_heap['is_min_heap']:
                if left_key < current_key:
                    extremo = left
                    current_key = left_key
            else:
                if left_key > current_key:
                    extremo = left
                    current_key = left_key
        
        if right <= heap_size:
            right_key = lt.get_element(elements_list, right - 1)['key']
            if my_heap['is_min_heap']:
                if right_key < current_key:
                    extremo = right
            else:
                if right_key > current_key:
                    extremo = right
        
        if extremo == pos:
            break
        
        lt.exchange(elements_list, pos - 1, extremo - 1)
        pos = extremo

def insert(my_heap, value, key):
    """
    Inserta un nuevo elemento en el heap
    """
    my_heap['size'] += 1
    lt.add_last(my_heap['elements'], {'key': key, 'value': value})
    swim(my_heap, my_heap['size'])

def get_first_priority(my_heap):
    """
    Retorna el elemento con mayor prioridad sin removerlo
    """
    if my_heap['size'] == 0:
        return None
    return lt.first_element(my_heap["elements"])['value']

def remove(my_heap):
    """
    Remueve y retorna el elemento con mayor prioridad
    """
    if my_heap['size'] == 0:
        return None
    
    # Obtener el elemento con mayor prioridad
    max_priority_element = lt.get_element(my_heap['elements'], 0)
    
    # Mover el último elemento al principio
    last_element = lt.remove_last(my_heap['elements'])
    my_heap['size'] -= 1
    
    if my_heap['size'] > 0:
        lt.change_info(my_heap['elements'], 0, last_element)
        sink(my_heap, 1)
    
    return max_priority_element['value']