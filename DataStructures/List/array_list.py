def new_list():
    return {
        'size': 0,
        'elements': [],
        'type': 'array_list'
    }
    
def is_empty(my_list):
    return my_list['size'] == 0

def size(my_list):
    return my_list['size']

def add_first(my_list, element):
    my_list['elements'].insert(0, element)
    my_list['size'] += 1
    return my_list

def first_element(my_list):
    if my_list['size'] == 0:
        raise IndexError("list index out of range")
    return my_list['elements'][0]

def get_element(my_list, pos):
    if pos < 0 or pos >= my_list['size']:
        raise IndexError("list index out of range")
    return my_list['elements'][pos]

def delete_element(my_list, pos):
    if pos < 0 or pos >= my_list['size']:
        raise IndexError("list index out of range")
    element = my_list['elements'].pop(pos)
    my_list['size'] -= 1
    return element

def remove_last(my_list):
    if my_list['size'] == 0:
        raise IndexError("list index out of range")    
    element = my_list['elements'].pop()
    my_list['size'] -= 1
    return element

def insert_element(my_list, element, pos):
    if pos < 0 or pos > my_list['size']:
        raise IndexError("list index out of range")
    my_list['elements'].insert(pos, element)
    my_list['size'] += 1
    return my_list

def default_function(element_1, element_2):
    if element_1 > element_2:
        return 1
    elif element_1 < element_2:
        return -1
    else:
        return 0

def is_present(my_list, element, cmp_function):
    for i in range(my_list['size']):
        if cmp_function(my_list['elements'][i], element) == 0:
            return i
    return -1

def change_info(my_list, pos, new_info):
    if pos < 0 or pos >= my_list['size']:
        raise IndexError("list index out of range")
    my_list['elements'][pos] = new_info
    return my_list

def exchange(my_list, pos_1, pos_2):
    if (pos_1 < 0 or pos_1 >= my_list['size']) or (pos_2 < 0 or pos_2 >= my_list['size']):
        raise IndexError("list index out of range")
    temp = my_list['elements'][pos_1]
    my_list['elements'][pos_1] = my_list['elements'][pos_2]
    my_list['elements'][pos_2] = temp
    return my_list

def sub_list(my_list, pos_i, num_elements):
    if pos_i < 0 or pos_i >= my_list['size']:
        raise IndexError("list index out of range")
    if pos_i + num_elements > my_list['size']:
        raise IndexError("list index out of range")
    sub_elements = my_list['elements'][pos_i : pos_i + num_elements]
    new_list = {
        'size': num_elements,
        'elements': sub_elements,
        'type': 'array_list'
    }
    return new_list

def default_sort_criteria(element_1, element_2):
   is_sorted = False
   if element_1 < element_2:
      is_sorted = True
   return is_sorted

def selection_sort(lst, sort_crit):
    n = size(lst)
    for i in range(n - 1):
        minimum = i
        for j in range(i + 1, n):
            if sort_crit(get_element(lst, j), get_element(lst, minimum)):
                minimum = j
        exchange(lst, i, minimum)
    return lst

def insertion_sort(lst, sort_crit):
    n = size(lst)
    for i in range(1, n):
        j = i
        while j > 0 and sort_crit(get_element(lst, j), get_element(lst, j-1)):
            exchange(lst, j, j-1)
            j -= 1
    return lst

def shell_sort(lst, sort_crit):
    n = size(lst)
    h = 1
    while h < n/3:
        h = 3 * h + 1
    while h >= 1:
        for i in range(h, n):
            j = i
            while j >= h and sort_crit(get_element(lst, j), get_element(lst, j - h)):
                exchange(lst, j, j - h)
                j -= h
        h //= 3
    return lst

def merge_sort(lst, sort_crit):
    n = size(lst)
    if n > 1:
        mid = n // 2
        left_list = sub_list(lst, 0, mid)
        right_list = sub_list(lst, mid, n - mid)
        merge_sort(left_list, sort_crit)
        merge_sort(right_list, sort_crit)
        i = j = k = 0
        left_size = size(left_list)
        right_size = size(right_list)
        while i < left_size and j < right_size:
            if sort_crit(get_element(right_list, j), get_element(left_list, i)):
                change_info(lst, k, get_element(right_list, j))
                j += 1
            else:
                change_info(lst, k, get_element(left_list, i))
                i += 1
            k += 1
        while i < left_size:
            change_info(lst, k, get_element(left_list, i))
            i += 1
            k += 1
        while j < right_size:
            change_info(lst, k, get_element(right_list, j))
            j += 1
            k += 1
    return lst

def quick_sort(lst, sort_crit):
    def partition(lo, hi):
        follower = lo
        pivot = get_element(lst, hi)
        for leader in range(lo, hi):
            if sort_crit(get_element(lst, leader), pivot):
                exchange(lst, follower, leader)
                follower += 1
        exchange(lst, follower, hi)
        return follower
    def quicksort(lo, hi):
        if lo < hi:
            pivot_index = partition(lo, hi)
            quicksort(lo, pivot_index - 1)
            quicksort(pivot_index + 1, hi)
    n = size(lst)
    if n > 0:
        quicksort(0, n - 1)
    return lst

def add_last(my_list, element):
    my_list['elements'].append(element)
    my_list['size'] += 1
    return my_list

def last_element(my_list):
    if my_list['size'] == 0:
        raise IndexError("list index out of range")
    return my_list['elements'][-1]

def remove_first(my_list):
    if my_list['size'] == 0:
        raise IndexError("list index out of range")
    element = my_list['elements'].pop(0)
    my_list['size'] -= 1
    return element