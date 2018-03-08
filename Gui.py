
__author__ = 'Ondřej Mejzlík'

import Grid_maker
import random
from tkinter import *

# Promenna slouzici k ukonceni programu
stop = False


class Gui:
    # Nastaveni------------
    __size = 50
    __speed = 0
    # ---------------------

    __canvas = None
    __grid = {}
    __text = None
    __keyborad_enable = None
    __player_box = None
    __score = 0

    def __init__(self, tk):
        """
        Konstruktor pro GUI. Zalozi globalni canvas, na ktery se nakresli ctverce. Velikost je dana promennymi tridy
        __size a __size
        :param tk: tkinter okno
        """
        # Pouzivame frame layout rozdeleny na jeden sloupec a 3 radky. Framu se preda okno a zavola se pack
        frame = Frame(tk)
        # Pack nacpe frame do okna
        frame.pack()
        # Hlavnimu frame se priradi hlidac udalosti klavesnice, ktery dal spusti handler a preda mu vzniklou udalost
        self.__keyboard_enable = False
        frame.bind("<Key>", func=self.__keyboard_handler)
        # Hlavni frame musi mit focus, aby spravne zaznamenaval udalosti
        frame.focus_set()
        # Vytvorime promenou pro text a priradime ji labelu. Staticky text by bylo pouze text='zprava'
        # Pomoci metody grid umistime label do 0 radku, labelu se predava frame misto objektu tk
        self.__text = StringVar()
        self.__text.set('Ready')
        Label(frame, textvariable=self.__text).grid(row=0, column=0)
        # Vytvorime canvas a umistime ho do druheho radku
        self.__canvas = Canvas(frame, width=(self.__size * 10), height=(self.__size * 10))
        self.__canvas.grid(row=1, column=0)
        # Vytvorime druhy frame, ktery bude obsahovat tlacitka
        frame_lower = Frame(frame)
        frame_lower.grid(row=2, column=0)
        # Vytvorime tlacitko a urcime jeho funkci, nakonec vlozime do druheho frame
        # button = Button(frame_lower, text='Make maze', command=self.run)
        # button.grid(row=0, column=0)
        # Vykresleni velkeho ctverce na misto mrizky malych, ktere se vytvori po kliknuti na tlacitko
        self.__canvas.create_rectangle(0, 1, self.__size * self.__size, self.__size * self.__size, fill='orange',
                                       outline='orange')
        self.run()

    def __draw_initial_grid(self):
        """
        Vyrobi mrizku ctverecku velkou podle konstant a vykresli je na canvas okna 10px od sebe.
        Nejdrive necha canvas vsechny ctverce nakreslit v pozadi a pote cely kanvas obnovi, cimz se nove ctverce
        ojevi. To je rychlejsi, nez obnovovani po kazdem ctverci zvlast.
        """
        self.__grid = Grid_maker.get_grid(self.__size, self.__size)

        for point_id in self.__grid.keys():
            pos = self.__get_box_position(self.__grid[point_id])
            self.__canvas.create_rectangle(pos[0], pos[1], pos[2], pos[3], fill='orange', outline='orange')

        self.__canvas.after(self.__speed, self.__canvas.update())

    @staticmethod
    def __get_box_position(point):
        """
        Staticka metoda nepouziva .self (nevztahuje se k zadne instanci tridy, muze vykonat vypocet pouze na zaklade
        predanych parametru]
        Vyrati ctverici se souradnicemi bodu nachystanymi pro kresleni. Kazdy bod se upravi na ctverec zabirajici 10px
        +1 u levych souradnic je pro vystredeni
        :param point: bod pro ktery se maji ziskat kreslici souradnice
        """
        left_up_x = point.get_x() + 1
        left_up_y = point.get_y() + 1
        right_down_x = point.get_x() + 10
        right_down_y = point.get_y() + 10

        return left_up_x, left_up_y, right_down_x, right_down_y

    def __draw_box(self, point):
        """
        Vykresli na canvas ctverec podle predaneho bodu.
        V pripade, ze bod je hrac/start, barva bude zelena, pokud je konec, bude cervena, v pripade, ze bod je vypnuty,
        bude seda, pokud je zapnuty, bude oranzova. Parametry create_rectangle jsou levy horni roh a spodni
        pravy roh v pixelech.
        :param point: bod, podle ktereho se vykresli ctverec
        """
        # Nechceme provadet kod, jakmile se zavola metoda quit po stisknuti krizku
        if stop:
            return

        pos = self.__get_box_position(point)
        if point.is_player():
            self.__canvas.create_rectangle(pos[0], pos[1], pos[2], pos[3], fill='green', outline='green', tags='player')

        elif point.is_end():
            self.__canvas.create_rectangle(pos[0], pos[1], pos[2], pos[3], fill='red', outline='red')

        # Tagy se pouzivaji jako jmenovka objektu pro pozdejsi smazani
        elif point.is_processed():
            self.__canvas.create_rectangle(pos[0], pos[1], pos[2], pos[3], fill='grey', outline='blue', tags='blue')

        elif not point.is_enabled():
            self.__canvas.create_rectangle(pos[0], pos[1], pos[2], pos[3], fill='grey', outline='grey')

        self.__canvas.after(self.__speed, self.__canvas.update())

    def __make_random_paths(self, start):
        """
        Vyrobi nahodne cesty. Postupuje tak, ze vsechny odebrane ctverce uklada do listu. Na zacatku je v listu pouze
        pocatecni ctverec. Cyklus bezi, dokud neni list odebranych ctvercu prazdny. Pokazde se jeden nahodny ctverec
        vybere a zaroven odstrani z listu a vytvori se pro nej nova cesta a vsechny odebrane ctverce se pridaji do listu
        Odebrat lze pouze takovy ctverec, ktery ma kolem sebe maximalne jeden jiny odebrany ctverec.
        Cesty vznikaji napojene na uz vytvorene cesty, protoze se vybira z odebranych ctvercu.
        :param start: Pocatecni ctverec
        """
        removed_boxes = [start]

        # Vyrob cestu dlouhou max 100 od pocatecniho ctverce a vsechny odstranene ctverce ukladej do listu
        while len(removed_boxes) > 0:
            # Vyber nahodne jeden z odstranenych ctvercu, udelej z nej chosen box a vymaz ho z listu
            chosen_box = removed_boxes.pop(random.randint(0, len(removed_boxes) - 1))

            # Pro kazdy zvoleny ctverec spustime vyrabeni cesty
            for i in range(100):
                neighbors = chosen_box.get_neighbors()
                # Vyber nahodneho souseda zvoleneho ctverce
                random_neighbor = self.__grid[neighbors[random.randint(0, (len(neighbors)) - 1)]]
                number_of_disabled_neighbors = 0

                if not random_neighbor.is_enabled():
                    continue
                else:
                    # Point obsahuje pouze cisla svych sousedu, v gridu lze dohledat prislusne objekty bodu
                    # Zkontroluj kolik ma vybrany bod neaktivnich sousedu, muze mit pouze jednoho
                    for point in random_neighbor.get_neighbors():
                        if not self.__grid[point].is_enabled():
                            number_of_disabled_neighbors += 1
                if number_of_disabled_neighbors > 1:
                    continue
                else:
                    random_neighbor.set_enabled(False)
                    removed_boxes.append(random_neighbor)
                    self.__draw_box(random_neighbor)

                chosen_box = random_neighbor

    def __find_path(self, start):
        """
        Vyuziva prohledavani grafu do sirky. Jako graf chape sede neaktivni ctverce. Zpracovane ctverce vykresluje.
        Prohledavani do sirky pouziva frontu. Dokud ve fronte neco je, vezme z ni prvni ctverec, nakresli ho, a nastavi,
        ze byl zpracovan. Pro kazdy zpracovavany ctverec ulozi vsechny jeho neaktivni, jeste nezpracovane (sede) sousedy
        do fronty, pokud ve fronte jiz nejsou a opakuje cyklus pro dalsi ctverec z fronty. Takto musi zpracovat vsechny
        ctverce, ktere jsou dosazitelne z pocatecniho a jsou sede. Pokud najde cil behem prohledavani, na konci vrati
        true
        :param start: Ctverec od ktereho zaciname prohledavat
        :return: True pokud jde dosahnout konce po nejake ceste tvorene neaktivnimi (sedymi) ctverci. False, pokud ne.
        """

        end_found = False
        # List pouzivame jako frontu
        queue = []
        queue.insert(0, start)

        # Prohledavani
        while len(queue) > 0:
            # Vyber z fronty prvni bod, vykresli ho jako zpracovavany a zpracuj
            current = queue.pop(-1)
            current.set_processed(True)
            # Vykresleni modreho ctverce na miste zpracovavaneho bodu
            self.__draw_box(current)
            # Projdi jeho sousedy a pridej je do fronty na konec pokud uz tam nejsou, zajimaji nas pouze neaktivni,
            # nezpracovani sousedi
            for point in current.get_neighbors():
                if self.__grid[point].is_end():
                    end_found = True
                if not self.__grid[point].is_enabled():
                    if not self.__grid[point].is_processed():
                        if not self.__grid[point] in queue:
                            queue.insert(0, self.__grid[point])

        return end_found

    def __make_maze(self):
        # Vypocet startu a konce
        """
        Vyrobi bludiste nahodnym mazanim ctvercu. Vybere prvni bod jako start a nahodny sedy bod jako konec po vytvoreni
        bludiste. Nasledne zkontroluje dosazitelnost konce a pokud je dosazitelny vrati True jinak False. Pred kazdym
        novym vytvorenim bludiste, uklidi predchozi.
        :return: True pokud jde dosahnout konce, False, pokud ne.
        """
        # Pred vytvorenim noveho bludiste, smazeme stary grid a vsechny dosavadni objekty na canvasu
        self.__grid.clear()
        # Canvas je nutne po sobe mazat, jinak se proste prekresluje nad stary a vznika memory leak
        self.__canvas.delete("all")

        # Vytvoreni mrizky bodu a jejich vykresleni
        self.__draw_initial_grid()

        # Nastaveni prvniho ctverce jako pocatku a zaroven to bude hrac
        first_box = self.__grid[0]
        first_box.set_enabled(False)
        # Prvni ctverec nakreslime jako sedy driv, nez se z nej udela hrac, ktery je zeleny
        self.__draw_box(first_box)

        # Prvni ctverec bude hrac a start, nahodne vybrany bude konec
        first_box.set_player(True)
        # Player box musi byt uschovavan jako atribut tridy, jinak by pri kazdem zavolani funkce zanikl
        self.__player_box = first_box

        self.__make_random_paths(first_box)

        # Vyber nahodny sedy ctverec a udelej z nej konec.
        end_set = False
        while not end_set:
            # Konec chceme umistit daleko, takze alespon od poloviny dal
            last_box = self.__grid[random.randint(int((self.__size * self.__size)/2), (self.__size * self.__size) - 1)]
            if not last_box.is_enabled():
                last_box.set_end(True)
                self.__draw_box(last_box)
                end_set = True

        # Overit, ze konec je dosazitelny a vratit true pokud je
        return self.__find_path(first_box)

    def run(self):
        """
        Spousti vyrabeni bludiste porad dokola a uklizi za sebou graficke objekty a pouzity grid
        """
        # Pro pripad, ze by bludiste nebylo resitelne, potom by se cyklus spustil znovu
        while True:
            self.__text.set('Making maze')
            self.__canvas.update()
            if self.__make_maze():
                break

        self.__text.set('Maze is solvable. Score: ' + str(self.__score))
        self.__canvas.delete('blue')
        self.__canvas.update()
        self.__keyboard_enable = True

    def __keyboard_handler(self, event):
        """
        Tsato metoda je spustena pri stisknuti klavesy. Vyhodnoti, ktera klavesa byla stisknuta a podle toho pohne, nebo
        nepohne hracem.
        :param event: Predana hodnota stisknute klavesy
        """
        # Klavesnice muze byt spustena az kdyz je budiste vytvoreno, jinak neexistuje grid, ktereho se chceme dotazovat
        if self.__keyboard_enable:
            key = event.char

            # Pokud je zmacknuta klavesa, ziska se prislusny soused ctverce v danem smeru. Pokud tento ctverec existuje
            # tzn. nechceme jit pres okraj hraci plochy a zaroven neni zed, muzeme se na nej posunout.
            # Stavajici zeleny ctverec predstavujici hrace se smaze a odebere se mu atribut hrace. Za noveho hrace se
            # prohlasi soused a vykresli se. Aktualni pozice hrace se ulozi do globalni promenne. Jinak by pri kazdem
            # zavolani teto funkce nebyla.
            if key == 'w':
                up_neighbor = self.__player_box.get_up_neighbor()
                if up_neighbor is not None and not self.__grid[up_neighbor].is_enabled():
                    self.__player_box.set_player(False)
                    self.__canvas.delete('player')
                    self.__grid[up_neighbor].set_player(True)
                    self.__draw_box(self.__grid[up_neighbor])
                    self.__player_box = self.__grid[up_neighbor]

            elif key == 'a':
                left_neighbor = self.__player_box.get_left_neighbor()
                if left_neighbor is not None and not self.__grid[left_neighbor].is_enabled():
                    self.__player_box.set_player(False)
                    self.__canvas.delete('player')
                    self.__grid[left_neighbor].set_player(True)
                    self.__draw_box(self.__grid[left_neighbor])
                    self.__player_box = self.__grid[left_neighbor]

            elif key == 's':
                down_neighbor = self.__player_box.get_down_neighbor()
                if down_neighbor is not None and not self.__grid[down_neighbor].is_enabled():
                    self.__player_box.set_player(False)
                    self.__canvas.delete('player')
                    self.__grid[down_neighbor].set_player(True)
                    self.__draw_box(self.__grid[down_neighbor])
                    self.__player_box = self.__grid[down_neighbor]

            elif key == 'd':
                right_neighbor = self.__player_box.get_right_neighbor()
                if right_neighbor is not None and not self.__grid[right_neighbor].is_enabled():
                    self.__player_box.set_player(False)
                    self.__canvas.delete('player')
                    self.__grid[right_neighbor].set_player(True)
                    self.__draw_box(self.__grid[right_neighbor])
                    self.__player_box = self.__grid[right_neighbor]

            # Test jestli se hrac nachazi na cili. Pokud ano, pricteme 1 ke score a vyrobime nove bludiste.
            if self.__player_box.is_end():
                # Aby neyblo zaznamenano vice stisku klavesy
                self.__keyboard_enable = False
                self.__score += 1
                self.__text.set('Maze is solvable. Score: ' + str(self.__score))
                self.run()


def quit_it():
    """
    Ukoncuje program
    """
    global stop
    stop = True
    print("stop")
    sys.exit()


root = Tk()
root.wm_title('Maze')
root.wm_protocol('WM_DELETE_WINDOW', quit_it)
root.resizable(width=False, height=False)
gui = Gui(root)
root.mainloop()
