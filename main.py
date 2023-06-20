import random as rnd


# Размер поля
SIZE = 6


class Board:
    def __init__(self) -> None:
        # Кораблики
        self.ships = []
        # Координаты попаданий по полю
        self.shots_on_board = Coordinates()
        # Генерация корабликов
        self.__init_ships()
        # Подсчёт кол-ва координат корабликов (для возможной кастомизации кол-ва и размеров корабликов?)
        self.__coords_count = self._count_coords()

    def __init_ships(self) -> None:
        """Добавление корабликов на доску"""
        # Передача параметров функции по переменным для удобства восприятия
        self._add_multiple_ships(ship_size = 3, count = 1)
        self._add_multiple_ships(ship_size = 2, count = 2)
        self._add_multiple_ships(ship_size = 1, count = 4)

    def _add_multiple_ships(self, ship_size, count) -> None:
        """Добавление множества корабликов"""
        # Подсчёт корабликов
        ship_count = 0
        while True:
            # Подготовка нового кораблика
            new_ship = ShipFactory.create_ship(ship_size)

            # Проверка пересечения координат нового корабля с координатами старых
            if self._check_for_free_space(new_ship):
                # Добавление кораблика
                self.ships.append(new_ship)
                # Увеличение счётчика созданных корабликов
                ship_count += 1
            else: continue

            # Если успешно создано необходимое кол-во корабликов, то хватит
            if ship_count == count: break

    def _check_for_free_space(self, new_ship) -> bool:
        """Проверка поля на наличие свободного места"""
        for old_ship in self.ships: # Перебор корабликов
            for old_coords in old_ship.coords: # Перебор координат ячейек корабликов
                for new_coords in new_ship.coords:
                    # Проверка на соседние ячейки
                    if any(
                        [(new_coords[0] - 1, new_coords[1]) == old_coords,
                         (new_coords[0] + 1, new_coords[1]) == old_coords,
                         (new_coords[0], new_coords[1] - 1) == old_coords,
                         (new_coords[0], new_coords[1] + 1) == old_coords
                         ]):
                        return False
                    if new_coords == old_coords: # Если встречено пересечение координат (ячейка занята)
                        return False
        return True

    def _count_coords(self):
        """Подсчёт кол-ва используемых координат"""
        result = 0
        for ship in self.ships:
            result += len(ship.coords)

        return result

    def check_is_defeated(self) -> bool:
        """Проверка поля на все подбитые корабли
        True - все корабли подбиты
        False - есть ещё порох в пороховницах"""
        # Если на поле отсутствуют координаты
        if not len(self.shots_on_board()):
            return False

        # Подсчёт успешно подбитых кораблей (а точнее подбитых координат)
        success_shot_count = 0

        for shot_coord in self.shots_on_board:
            for ship in self.ships:
                for ship_coord in ship.coords:
                    # Если координаты ячейки поля с выстрелами совпадают с координатами какого-либо кораблика
                    if shot_coord == ship_coord: success_shot_count += 1

        # Если кол-во подсчитанных подбитых координат не равно общему количеству координат
        if success_shot_count != self.__coords_count: return False

        return True


class Player(Board):
    def __init__(self):
        super().__init__()


class AI(Player):
    def __init__(self):
        super().__init__()

    def do_turn(self) -> object:
        """Делает ход, возвращает class Coordinates"""
        coords = Coordinates()
        coords.add_coordinate((rnd.randint(0, SIZE - 1), rnd.randint(0, SIZE - 1)))
        return coords


class GameGraphics:
    def __init__(self) -> None: pass

    def print_board(self, board) -> None:
        """Печать союзного поля для игрока"""
        print("""
            -------------------------------
                       ВАШЕ ПОЛЕ
            -------------------------------
            """)
        for i in range(SIZE + 1):
            for j in range(SIZE + 1):
                # Если угловая позиция, то печать "ничего"
                if not (i or j):
                    print('   ', end='|')
                # Если первая строка, то печать шапки
                elif not i:
                    print(f' {j} ', end='|')
                # Если первый элемент в строке, то печать шапки
                elif not j:
                    print(f' {i} ', end='|')
                # Иначе печать значения
                else:
                    # Для проверки на статус ячейки
                    # True - с ней что-то случилось
                    # False - с ней ничего не случилось
                    cell_status = False

                    # Проверка на уже простреленную ячейку
                    for cell_coord in board.shots_on_board(): # Перебор записаных ячеек
                        if cell_coord == (i - 1, j - 1): # Если проверяемая ячейка совпадает с записаной
                            for ship in board.ships: # Перебор корабликов
                                for ship_coords in ship.coords: # Перебор координат кораблика
                                    # Если записанная координата совпадает с координатой кораблика
                                    if ship_coords == cell_coord:
                                        print(' X ', end = '|')
                                        cell_status = True
                            if not cell_status:
                                print(' - ', end = '|')
                                cell_status = True

                    # Если с ячейкой уже что-то случилось, то переходим к следующей
                    if cell_status: continue

                    # Проверка принадлежности координаты корабля к ячейке
                    for ship in board.ships:
                        for coords in ship.coords:
                            if coords == (i - 1, j - 1):
                                print(' ■ ', end='|')
                                cell_status = True
                        if cell_status: break

                    # Если с ячейкой ничего не случилось, то печатаем "пусто"
                    if not cell_status:
                        print('   ', end = '|')
            print()

    def print_enemy_board(self, board) -> None:
        """Печать предполагаемого поля противника"""
        print("""
            -------------------------------
                    ПОЛЕ ПРОТИВНИКА
            -------------------------------
            """)
        for i in range(SIZE + 1):
            for j in range(SIZE + 1):
                # Если угловая позиция, то печать "ничего"
                if not (i or j):
                    print('   ', end='|')
                # Если первая строка, то печать шапки
                elif (i == 0):
                    print(f' {j} ', end='|')
                # Если первый элемент в строке, то печать шапки
                elif (j == 0):
                    print(f' {i} ', end='|')
                # Иначе печать значения
                else:
                    # Для проверки на статус ячейки
                    # True - с ней что-то случилось
                    # False - с ней ничего не случилось
                    cell_status = False

                    # Проверка на уже простреленную ячейку
                    for cell_coord in board.shots_on_board():  # Перебор записаных ячеек
                        if cell_coord == (i - 1, j - 1):  # Если проверяемая ячейка совпадает с записаной
                            for ship in board.ships:  # Перебор корабликов
                                for ship_coords in ship.coords:  # Перебор координат кораблика
                                    # Если записанная координата совпадает с координатой кораблика
                                    if ship_coords == cell_coord:
                                        print(' X ', end='|')
                                        cell_status = True
                            if not cell_status:
                                print(' - ', end='|')
                                cell_status = True

                    # Если с ячейкой уже что-то случилось, то переходим к следующей
                    if cell_status: continue

                    # Если с ячейкой ничего не случилось, то печатаем "пусто"
                    if not cell_status:
                        print('   ', end = '|')
            print()


class GameLogic:
    def __init__(self) -> None:
        # True - ход игрока
        # False - ход противника
        self.turn = True

    def proccess_event(self, event):
        """Обработчик событий
        True - Событие успешно выполнено
        False - Событие не было выполнено успешно"""
        # Если событие "Выстрел"
        if event.get_type() == GameEvent.EVENTS['SHOOT']:
            # Берём координаты
            coords = event.get_data()['coords']

            # Если выстрел по таким координатам уже был
            if coords()[0] in event.get_data()['player'].shots_on_board():
                # Выдаём ошибку о занятости ячейки
                return GameExceptions.raise_exception('CellIsAlreadyBeenShot')
            else:
                # Добавляем координаты на поле
                event.get_data()['player'].shots_on_board().append(coords()[0])

                # Смена хода
                self.proccess_event(GameEvent(GameEvent.EVENTS['TURN']))

                # Перебор корабликов
                for ship in event.get_data()['player'].ships:
                    # Перебор координат кораблика
                    for ship_coords in ship.coords:
                        # Если координаты выстрела совпадает с координатами кораблика
                        if ship_coords == coords()[0]:
                            # Смена хода обратно к последнему ходящему
                            self.proccess_event(GameEvent(GameEvent.EVENTS['TURN']))
                return True

        # Обработчик смены хода
        if event.get_type() == GameEvent.EVENTS['TURN']:
            self.turn = not self.turn
            return True

        # Обработчик проверки на выигрыш
        if event.get_type() == GameEvent.EVENTS['CHECK']:
            return event.get_data()['player'].check_is_defeated()

        return False

    def get_turn(self):
        """Возвращает ход, где:
        True - ход игрока
        False - ход противника"""
        return self.turn


class GameEvent:
    """Класс хранящий игровые события"""
    EVENTS = {
        'NONE'  : 0,
        'SHOOT' : 1,
        'TURN'  : 2,
        'CHECK' : 3
    }

    def __init__(self, type: int, data = None) -> None:
        self.__type = type
        self.__data = data

    def get_type(self) -> int:
        """Возвращает ID типа события"""
        return self.__type

    def get_data(self) -> object:
        """Возвращает аргументы события"""
        return self.__data


class GameExceptions:
    @staticmethod
    def raise_exception(args) -> str:
        """\"Обработка\" событий ошибки"""
        if str(args) == 'ValueError':
            return 'Введённые координаты не являются целыми числами!'
        if str(args) == 'WrongInput':
            return 'Координаты записаны некорректно!'
        if str(args) == 'OutOfRange':
            return 'Введённые координаты выходят за пределы игрового поля!'
        if str(args) == 'CellIsAlreadyBeenShot':
            return 'Вы уже стреляли в эти координаты, попробуйте другие!'
        else:
            return 'Произошла непредвиденная ошибка, попробуйте ещё раз'


class Coordinates:
    def __init__(self) -> None:
        # Массив координат чего-либо в формате tuple(x, y)
        self.__coords = []

    def __getitem__(self, item) -> tuple:
        return self.__coords[item]

    def __call__(self):
        return self.__coords

    @property
    def coords(self):
        return self.__coords

    def add_coordinate(self, coords) -> None:
        """Добавление координаты"""
        self.__coords.append(coords)

    @staticmethod
    def validate(coords):
        """Проверка валидности введённых координат"""
        try:
            # Проверка и преобразование "сырых" координат к числу
            coords = int(coords)

            # Проверка на корректно введённый формат координат
            if not (10 <= coords <= 100):
                raise Exception('WrongInput')

            # Разбивка координат на X и Y
            coords = (coords // 10 - 1, coords % 10 - 1)
            # Проверка на выход за границу поля
            if not (coords[0] in range(0, SIZE) and coords[1] in range(0, SIZE)):
                raise Exception('OutOfRange')

        except Exception as args:
            # Генерация ошибки текста
            exception_text = GameExceptions.raise_exception(args)
            # Возвращение текста об ошибке
            return exception_text
        else:
            # Или возвращение координат
            return coords


class Ship(Coordinates):
    def __init__(self, type) -> None:
        super().__init__()
        # Размер корабля
        self.type = type

    def get_type(self) -> int:
        """Возвращает размер корабля"""
        return self.type


# Завод по созданию корабликов
class ShipFactory:
    @staticmethod
    def create_ship(ship_size: int) -> Ship:
        while True:
            # Берётся случайная позиция
            x, y = rnd.randint(0, SIZE - 1), rnd.randint(0, SIZE - 1)
            # Инициализация кораблика
            new_ship = Ship(ship_size)
            # Добавление координат кораблику
            new_ship.add_coordinate((x, y))

            # Если однопалубный
            if ship_size == 1:
                return new_ship
            elif 2 <= ship_size:
                # 0 - Направление по X вправо || 1 - Направление по Y вниз
                direction = rnd.randint(0, 1)

                # Если увеличение по оси X
                if not direction:
                    # Если размер попадает в пределы игрового поля
                    if new_ship.coords[0][0] + ship_size <= SIZE:
                        for i in range(1, ship_size):
                            # Добавляем следующую координату по X
                            new_ship.add_coordinate((new_ship.coords[0][0] + i, new_ship.coords[0][1]))
                    else: continue  # Иначе ищем новую позицию
                else:  # Если увеличение по оси Y
                    if new_ship.coords[0][1] + ship_size <= SIZE:  # Если размер попадает в пределы игрового поля
                        for i in range(1, ship_size):
                            # Добавляем следующую координату по Y
                            new_ship.add_coordinate((new_ship.coords[0][0], new_ship.coords[0][1] + i))
                    else: continue  # Иначе ищем новую позицию
                return new_ship


class Game:
    def __init__(self, graphics: GameGraphics, logic: GameLogic) -> None:
        # Игрок
        self.ally = Player()
        # Бот
        self.AI = AI()

        self.graphics = graphics
        self.logic = logic

    def start_game(self) -> None:
        # Переменная для хранения текста об ошибке
        exception_string = ''

        # Игровой цикл
        while True:
            # Печать союзного поля
            self.graphics.print_board(self.ally)
            # Печать вражеского поля
            self.graphics.print_enemy_board(self.AI)

            # Печать ошибки, если таковая есть
            print(exception_string)
            exception_string = ''

            # Если ход игрока
            if self.logic.get_turn():
                choice = input("""Введите координаты согласно формату "11" (без ковычек),
где 1-е число - номер строки, 2-е число номер столбца: """)

                # Проверка валидности и присвоения координат
                exception_check_result = Coordinates().validate(choice)
                if type(exception_check_result) == str:
                    # Если координаты не валидны, то получаем ошибку и возвращаем игрока опять вводить координаты
                    exception_string = exception_check_result
                    continue

                # Инициализация координат
                coords = Coordinates()
                coords.add_coordinate(Coordinates.validate(choice))

                # Генерация события ВЫСТРЕЛ
                event = GameEvent(
                    GameEvent.EVENTS['SHOOT'],
                    {'coords': coords,
                     'player': self.AI})

                # Отправка события
                # Если не успешно, то попытаться отправить событие с новыми координатами
                event_result = self.logic.proccess_event(event)
                if type(event_result) == str:
                    # Получаем ошибку
                    exception_string = event_result
                # Если всё же что-то пошло не так, отправить игрока вводить новые координаты
                if event_result == bool and not event_result: continue

            # Проверка на конец игры
            # True - выход из игрового цикла
            if self.logic.proccess_event(
                    GameEvent(
                        GameEvent.EVENTS['CHECK'],
                        {'player': self.AI})):
                break

            # Если ход противника
            if not self.logic.get_turn():
                # Генерация события
                event = GameEvent(
                    GameEvent.EVENTS['SHOOT'],
                    {'coords': self.AI.do_turn(),
                     'player': self.ally})
                # Отправка события
                # Если не успешно, то попытаться отправить событие с новыми координатами
                if not self.logic.proccess_event(event): continue

            # Проверка на конец игры
            # True - выход из игрового цикла
            if self.logic.proccess_event(
                    GameEvent(
                        GameEvent.EVENTS['CHECK'], {'player': self.ally})):
                break

        self.end_game()

    def end_game(self) -> None:
        """Вывод поздравлений"""
        self.winner = ''

        # Если ходил последним человек
        if self.logic.get_turn():
            # Вывод вражеской обстрелянной доски
            self.graphics.print_enemy_board(self.AI)
            self.winner = 'Игрок'
        # Если ходил последним бот
        else:
            # Вывод союзной обстрелянной доски
            self.graphics.print_board(self.ally)
            self.winner = 'Компьютер'

        print(f'Победил {self.winner}!')


# ------------------------------------------------

# Начало
Game(GameGraphics(), GameLogic()).start_game()
