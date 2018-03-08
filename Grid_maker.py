__author__ = 'Ondřej Mejzlík'

from Point import Point


def __make_grid(rows, cols):
    """
    Vyrobi mapu bodu se souradnicemi a jejich id jako klicem v mape. Souradnice skacou po 10.
    Kazdemu bodu se pridaji jeho sousede. Mrizka bodu vznika po sloupcich ne po radcich (0, pod ni je 1, ...)
    :param rows: pocet radku
    :param cols: pocet sloupcu
    """
    map_of_points = {}
    new_id = 0
    for i in range(rows):
        for j in range(cols):
            # Prida do mapy novou polozku {klic:hodonta}
            map_of_points.update({new_id: Point(i * 10, j * 10, new_id)})
            new_id += 1

    __initialize_neighbors(map_of_points, rows)
    return map_of_points


def __initialize_neighbors(map_of_points, rows):
    """
    Private metoda. Prida bodu seznam jeho sousedu. Sousedi pouze nahoru, dolu a do stran
    Tito sousedi jsou vzdaleni vzdy o 1 nebo o velikost radku. Pokud takovy soused existuje, ma svoje id v mape,
    prida se do listu. V pripade, ze jsme v prvnim nebo poslednim radku, nechceme do sousedu davat body z jinych
    sloupcu.
    :param rows: pocet radku plochy
    """
    for point_id in map_of_points.keys():
        if (point_id + 1) in map_of_points.keys():
            if not(map_of_points[point_id].get_x() < (rows*10)-10 and map_of_points[point_id].get_y() == (rows*10)-10):
                map_of_points[point_id].set_down_neighbor(point_id + 1)

        if (point_id - 1) in map_of_points.keys():
            if not(map_of_points[point_id].get_x() > 0 and map_of_points[point_id].get_y() == 0):
                map_of_points[point_id].set_up_neighbor(point_id - 1)

        if (point_id + rows) in map_of_points.keys():
            map_of_points[point_id].set_right_neighbor(point_id + rows)

        if (point_id - rows) in map_of_points.keys():
            map_of_points[point_id].set_left_neighbor(point_id - rows)


def get_grid(rows, cols):
    """
    Vraci vyrobeny grid bodu s inicializovanymi sousedy
    :param rows: pocet radku
    :param cols: pocet sloupcu
    :return: vyrobeny grid bodu
    """
    return __make_grid(rows, cols)