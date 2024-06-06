from random import randint
class BoardException(BaseException):
    pass
class BoardOutException(BaseException):
    def __str__(self):
        return "Вы пытаетесь выстрелить за доску! Повторите попытку."
class BoardUsedException(BaseException):
    def __str__(self):
        return "Эта клетка не доступна. Повторите попытку."
class BoardWrongShipException(BaseException):
    pass
class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    def __repr__(self):
        return [self.x, self.y]
class Ship:
    def __init__(self, length, nose, direction):
        self.length = length
        self.nose = nose
        self.direction = direction
        self.lifes = length
    def dots(self):
        dots_ship=[]
        dots_ship.append([self.nose[0], self.nose[1]])
        if self.direction == 0:
            for i in range(self.length-1):
                self.nose[0] += 1
                dots_ship.append([self.nose[0], self.nose[1]])
        elif self.direction == 1:
            for i in range(self.length-1):
                self.nose[1] += 1
                dots_ship.append([self.nose[0], self.nose[1]])
        return dots_ship
class Board:
    def __init__(self, size=6):
        self.size = size
        self.amount = 0
        self.field_1 = [["🟦"] * size for _ in range(size)]
        self.field_2 = [["🟦"] * size for _ in range(size)]
        self.ships = []
    def add_ship(self, shdots):
        for i in shdots:
            if self.out(i) and self.contour(shdots, 0):
                pass
            else:
                raise BoardWrongShipException()
        for i in shdots:
            self.field_2[i[0]][i[1]] = '🚢'
        self.amount += 1
        self.ships.append(shdots)
        return self.field_2
    def contour(self, shdots, soz_ud):
        ship_cont = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        ship_cont_list=[]
        if soz_ud == 0:
            for t in shdots:
                for j in ship_cont:
                    j = [j[0] + t[0], j[1] + t[1]]
                    if (not (j in ship_cont_list)) and self.out(j):
                        ship_cont_list.append(j)
            for i in ship_cont_list:
                if self.field_2[i[0]][i[1]] == '🚢':
                    return False
            return self.field_2
        else:
            shot_ship = []
            for i in self.ships:
                lifsh=len(i)
                for j in i:
                    if self.field_1[j[0]][j[1]] == '💥':
                        lifsh -=1
                if lifsh == 0:
                    shot_ship.append(i)
                    self.amount -= 1
            for t in shot_ship:
                for i in t:
                    for j in ship_cont:
                        j = [j[0] + i[0], j[1] + i[1]]
                        if (not (j in ship_cont_list)) and self.out(j):
                            ship_cont_list.append(j)
            for i in ship_cont_list:
                if self.field_1[i[0]][i[1]] == '💥':
                    pass
                else:
                    self.field_1[i[0]][i[1]] = '🚫'
                    self.field_2[i[0]][i[1]] = '🚫'
            return self.field_1
    def board_consol(self, hid):# hid - 1, если нужно скрытую доску и 0 если нескрытую
        if hid:
            print("  | 1  |  2  | 3  | 4  | 5  | 6  |")
            fp = 1
            for i in self.field_1:
                print(fp,'|',i[0],'|',i[1],'|',i[2],'|',i[3],'|',i[4],'|',i[5],'|')
                fp +=1
        else:
            print("  | 1  |  2  | 3  | 4  | 5  | 6  |")
            fp = 1
            for i in self.field_2:
                print(fp, '|', i[0], '|', i[1], '|', i[2], '|', i[3], '|', i[4], '|', i[5], '|')
                fp += 1
    def out(self, dot):
        if (dot[0] in range(self.size)) and (dot[1] in range(self.size)):
            return True
        return False
    def shoot(self, dot_shoot): # shep1 должен отображать список всех кораблей dot_shoot - точка выстрела
        if not self.out(dot_shoot):
            raise BoardOutException()
        elif (self.field_1[dot_shoot[0]][dot_shoot[1]] == '💥') or (self.field_1[dot_shoot[0]][dot_shoot[1]] == '🚫'):
            raise BoardUsedException()
        elif self.field_1[dot_shoot[0]][dot_shoot[1]] == '🟦':
            if self.field_2[dot_shoot[0]][dot_shoot[1]] == '🚢':
                self.field_1[dot_shoot[0]][dot_shoot[1]] = '💥'
                self.field_2[dot_shoot[0]][dot_shoot[1]] = '💥'
                return self.contour(None, 1)
            elif (self.field_2[dot_shoot[0]][dot_shoot[1]] == '🚫') or (self.field_2[dot_shoot[0]][dot_shoot[1]] == '🟦'):
                self.field_1[dot_shoot[0]][dot_shoot[1]] = '🚫'
                self.field_2[dot_shoot[0]][dot_shoot[1]] = '🚫'
    def clean(self): # метод для очистки поля
        self.field_2 = [["🟦"] * self.size for _ in range(self.size)]
    def win(self): # метод для проверки выигрыша
        for i in self.field_2:
            for j in i:
                if j == "🚢":
                    return False
        return True
class Player:
    def __init__(self, f_sv, f_ch):
        self.f_sv = f_sv
        self.f_ch = f_ch
    def ask(self):
        pass
    def move(self):
        hod_dot = self.ask()
        if self.f_ch.shoot(hod_dot):
            return 1
class AI(Player):
    def ask(self):
        ask = [randint(0,5),randint(0,5)]
        return ask
class User(Player):
    def ask(self):
        while True:
            askx = int(input('Введите вертикальную координату: '))
            asky = int(input('Введите горизонтальную координату: '))
            if (askx in range(1,7)) and (asky in range(1,7)):
                ask = [askx - 1, asky - 1]
                return ask
class Game:
    def __init__(self):
        self.field_us = Board()
        self.field_ai = Board()
        self.us = User(self.field_us, self.field_ai)
        self.ai = AI(self.field_ai, self.field_us)
    def random_board(self, fld):
        ship_lengths = [3,2,2,1,1,1,1]
        while True:
            popitka = 0
            for i in ship_lengths:
                while popitka <= 4000:
                    popitka = popitka +1
                    try:
                        l = Ship(i, [randint(0,5),randint(0,5)], randint(0,1))
                        fld.add_ship(l.dots())
                    except BaseException:
                        pass
                    else:
                        break
          #  print(popitka)
            if popitka >= 4000:
                fld.clean()
            else:
                break
    def greet(self):
        print('''                          Игра "Морской Бой"
        Игра организована следующим образом: Противники (Вы и ИИ) по очереди
        указывают 2 координаты (вертикальную и горизонтальную) ячеек в которые 
        собираются стрелять. При своем очередном ходе игрок, попавший в корабль, 
        получает дополнительный ход. Выигрывает тот, кто первым уничтожит все 
        корабли противника!
        Обозначения:
        🟦 - не занятая либо скрытая ячейка
        🚫 - промах либо ячейка в которую нельзя стрелять 
        🚢 - корабль
        💥 - подбитый корабль 
        ''')
    def loop(self):
        self.random_board(self.field_us)
        self.random_board(self.field_ai)
        while True:
            print('----------МОЯ ДОСКА-----------------')
            self.field_us.board_consol(0)
            print('----------ДОСКА ИИ------------------')
            self.field_ai.board_consol(1)
            per = True
            while per:
                try:
                    while True:
                        if self.us.move():
                            if self.field_ai.win():
                                print('----------МОЯ ДОСКА-----------------')
                                self.field_us.board_consol(0)
                                print('----------ДОСКА ИИ------------------')
                                self.field_ai.board_consol(0)
                                print('Вы победили!')
                                return 1
                            #    break
                            print('----------МОЯ ДОСКА-----------------')
                            self.field_us.board_consol(0)
                            print('----------ДОСКА ИИ------------------')
                            self.field_ai.board_consol(1)

                        else:
                            break
                except (BaseException) as e:
                    print(e)
                else:
                    per = False
            per = True
            while per:
                try:
                    while True:
                        if self.ai.move():
                            if self.field_us.win():
                                print('----------МОЯ ДОСКА-----------------')
                                self.field_us.board_consol(0)
                                print('----------ДОСКА ИИ------------------')
                                self.field_ai.board_consol(0)
                                print('Победил ИИ :(')
                                return 1
                        else:
                            break
                except BaseException:
                    pass
                else:
                    per = False
    def start(self):
        self.greet()
        self.loop()
g = Game()
g.start()



#kikikukuуaue