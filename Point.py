__author__ = 'Ondřej Mejzlík'


class Point:
    """
    Trida reprezentujici bod se souradnicemi x,y
    """
    __position_x = 0
    __position_y = 0
    __point_id = 0
    __point_is_enabled = True
    __point_is_player = False
    __point_is_end = False
    __point_is_processed = False
    __up_neighbor = None
    __down_neighbor = None
    __left_neighbor = None
    __right_neighbor = None

    def __init__(self, pos_x, pos_y, point_id):
        """
        Konstruktor bodu se souradnicemi x,y
        :param pos_x: souradnice x
        :param pos_y: souradnice y
        :param point_id: identifikator
        """
        self.__position_x = pos_x
        self.__position_y = pos_y
        self.__point_id = point_id

    def get_x(self):
        """
        Vraci souradnici x
        :return: souradnice x
        """
        return self.__position_x

    def get_y(self):
        """
        Vraci souradnici y
        :return: souradnice y
        """
        return self.__position_y

    def get_id(self):
        """
        Vraci id bodu
        :return: id bodu
        """
        return self.__point_id

    def get_neighbors(self):
        """
        Vraci sousedy bodu
        :return: sousedi bodu
        """
        neighbors = []

        if self.__up_neighbor is not None:
            neighbors.append(self.__up_neighbor)

        if self.__down_neighbor is not None:
            neighbors.append(self.__down_neighbor)

        if self.__left_neighbor is not None:
            neighbors.append(self.__left_neighbor)

        if self.__right_neighbor is not None:
            neighbors.append(self.__right_neighbor)

        return neighbors

    def is_enabled(self):
        """
        Vraci true pokud je bod akivni, false pokud ne
        :return: True pro aktivni bod, false pro neaktivni
        """
        return self.__point_is_enabled

    def is_player(self):
        """
        Vraci true pokud je bod hrac, false pokud ne
        :return: True pokud je bod hrac false pokud neni
        """
        return self.__point_is_player

    def is_end(self):
        """
        Vraci true pokud je bod konec, false pokud ne
        :return: True pokud je bod konec false pokud neni
        """
        return self.__point_is_end

    def is_processed(self):
        """
        Vraci true pokud je bod zpracovavan pri hledani cesty, false pokud ne
        :return: True pokud je bod zpracovavan pri hledani cesty, false pokud ne
        """
        return self.__point_is_processed

    def set_processed(self, value):
        """
        Nastavuje bod jako zpracovavany
        :param value: True pro nastaveni zpracovavaneho bodu, false pro zruseni
        """
        self.__point_is_processed = value

    def set_end(self, value):
        """
        Nastavuje bod jako konec
        :param value: True pro nastaveni konce, false pro zruseni
        """
        self.__point_is_end = value

    def set_player(self, value):
        """
        Nastavuje bod jako hrace
        :param value: True pro nastaveni hrace, false pro zruseni
        """
        self.__point_is_player = value

    def set_enabled(self, value):
        """
        Nastavuje bod do aktivniho nebo neaktivniho stavu
        :param value: True pro aktivaci, false pro deaktivaci
        """
        self.__point_is_enabled = value

    def set_up_neighbor(self, point):
        """
        Nastavuje horniho souseda bodu
        :param point: novy sousedu bodu
        """
        self.__up_neighbor = point

    def set_down_neighbor(self, point):
        """
        Nastavuje spodniho souseda bodu
        :param point: novy sousedu bodu
        """
        self.__down_neighbor = point

    def set_left_neighbor(self, point):
        """
        Nastavuje leveho souseda bodu
        :param point: novy sousedu bodu
        """
        self.__left_neighbor = point

    def set_right_neighbor(self, point):
        """
        Nastavuje praveho souseda bodu
        :param point: novy sousedu bodu
        """
        self.__right_neighbor = point

    def get_up_neighbor(self):
        """
        Vraci horniho souseda bodu
        :return: vraci horniho osuseda bodu
        """
        return self.__up_neighbor

    def get_down_neighbor(self):
        """
        Vraci spodniho souseda bodu
        :return: vraci spodniho osuseda bodu
        """
        return self.__down_neighbor

    def get_right_neighbor(self):
        """
        Vraci praveho souseda bodu
        :return: vraci praveho osuseda bodu
        """
        return self.__right_neighbor

    def get_left_neighbor(self):
        """
        Vraci leveho souseda bodu
        :return: vraci leveho osuseda bodu
        """
        return self.__left_neighbor

    def set_x(self, x):
        """
        Nastavuje souradnici x
        :param x: nova souradnice x
        """
        self.__position_x = x

    def set_y(self, y):
        """
        Nastavuje souradnici y
        :param y: nova souradnice y
        """
        self.__position_y = y

    def to_string(self):
        """
        Vraci popis bodu
        :return: popis bodu jeho id a souradnice x,y (Point id=id x=x y=y)
        """
        return 'Point' + ' id=' + str(self.__point_id) + ' x=' + str(self.__position_x) + ' y=' + str(self.__position_y) \
               + ' neighbors=' + str(self.get_neighbors())
