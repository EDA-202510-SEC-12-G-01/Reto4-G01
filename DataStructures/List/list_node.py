"""
  Estructura que contiene la información a guardar en una lista encadenada
"""


def new_single_node(element):
    """ Estructura que contiene la información a guardar en una lista encadenada

        :param element: Elemento a guardar en el nodo
        :type element: any

        :returns: Nodo creado
        :rtype: dict
    """
    node = {'info': element, 'next': None}
    return (node)


def get_element(node):
    return node['info']


def new_double_node(element):
    """ Estructura que contiene la información a guardar en un nodo de una lista doblemente encadenada
    """
    node = {'info': element,
            'next': None,
            'prev': None
            }
    return node
