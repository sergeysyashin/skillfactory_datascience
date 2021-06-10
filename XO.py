import time

#   0 1 2
# 0 - - -
# 1 - - -
# 2 - - -

print(f'Привет! Играем в винатжные крестики-нолики.')
print(f'Вы можете сыграть вдвоем или против компьютера (Это версия 2.0 - с расширенным функционалом)')
print('---------0_0---------')

game_type = input('Если хотите сыграть вдвоем, то введите "2", если против компьютера, то введите любой '
                  'другой символ: ')

free_place = '-'
christ = 'x'
zero = 'o'


def print_game_field(dict):
    print(f'  1 2 3')
    for key, val in dict.items():
        print(f'{key} {val[0]} {val[1]} {val[2]}')


def check_step(step_list):
    # проверяем введенные пользователем координаты на нахождение в пределах игрового поля
    return True if (step_list[0] in [1, 2, 3] and step_list[1] in [1, 2, 3]) else False


def check_free_step(dict, step_list):
    # step_list = [x, y]
    x = step_list[0]
    y = step_list[1]
    return True if str(dict[x][y-1]) == free_place else False


def player_step(dict, player_name):
    # получаем от игрока данные хода, проверяем их на нахождение в предлах поля (отдельной функцией check_step) и на
    # релеватность типа введенных данных
    # возвращаем список координат по x и y

    while True:
        user_step = input(f'{player_name}, введите координаты вашего хода по горизонтали и вертикали через запятую '
                          f'(например: 1,2):')
        try:
            user_step_list = list(map(int, user_step.split(',')))
            if check_step(user_step_list):
                if check_free_step(dict, user_step_list):
                    return user_step_list
                else:
                    print(f'Эта ячейка занята:) Попробуйте ещё раз.')

            else:
                print(f'Координаты должны лежать в промежутке от 1 до 3 включительно! Пробуйте ещё.')
        except ValueError as e:
            print('Введите числа, не буквы')


def fill_game_progress_dict(dict, step_list, symbol=christ):
    # заполняем словарь символом symbol по данным хода игрока player_step_list

    x = step_list[0]
    y = step_list[1]
    dict[x][y-1] = symbol
    return dict


def win_check(dict):
    for key, val in dict.items():
        if (val[0] == val[1] == val[2] == 'x') or (val[0] == val[1] == val[2] == 'x'):
            return True
    if (dict[1][0] == dict[2][0] == dict[3][0] == 'x') or \
        (dict[1][0] == dict[2][0] == dict[3][0] == 'o') or \
        (dict[1][0] == dict[2][1] == dict[3][2] == 'x') or \
        (dict[1][0] == dict[2][1] == dict[3][2] == 'o') or \
        (dict[1][1] == dict[2][1] == dict[3][1] == 'x') or \
        (dict[1][1] == dict[2][1] == dict[3][1] == 'o') or \
        (dict[1][2] == dict[2][2] == dict[3][2] == 'x') or \
        (dict[1][2] == dict[2][2] == dict[3][2] == 'o'):
        return True


def game_process(user, dict, symbol):
    fill_game_progress_dict(dict, step_list=player_step(dict, user), symbol=symbol)
    print_game_field(dict)


# Функции для робота


def check_corner_and_christ_elements(dict):
    # Функция проверки свободных углов и элементов "креста"
    # функция проверяет последовательно все углы и если какой-то из них свободен - возвращает список robot_step_list,
    # из координат хода либо если все углы заняты (ну мало ли) - тогда проверяет крестовые и возвращает координаты
    # этого хода.
    # game_progress_dict = {
    #         1: ['-', '-', '-'],
    #         2: ['-', '-', '-'],
    #         3: ['-', '-', '-']
    #     }

    if check_free_step(dict, [1, 1]):
        robot_step_list = [1, 1]
    elif check_free_step(dict, [1, 3]):
        robot_step_list = [1, 3]
    elif check_free_step(dict, [3, 1]):
        robot_step_list = [3, 1]
    elif check_free_step(dict, [3, 3]):
        robot_step_list = [3, 3]
    else:
        if check_free_step(dict, [1, 2]):
            robot_step_list = [1, 2]
        elif check_free_step(dict, [2, 3]):
            robot_step_list = [2, 3]
        elif check_free_step(dict, [3, 1]):
            robot_step_list = [3, 1]
        elif check_free_step(dict, [2, 1]):
            robot_step_list = [2, 1]
        else:
            return False
    return robot_step_list


def check_2_line_elements(dict, symbol):
# Функция проверки двух подряд по вертикали или горизонтали символа (своих) и сразу поставновки туда знака
# Принимает dict, symbol
# Возвращает свободный элемент с координатами в списке [x, y]

# Алгоритм:
# game_progress_dict = {
#         1: ['-', '-', '-'],
#         2: ['-', '-', '-'],
#         3: ['-', '-', '-']
#     }

    for key, val in dict.items():
        if (val[0] == val[1] == symbol) and (val[2] == free_place):
            robot_step_list = [key,3]
        elif (val[0] == val[2] == symbol) and (val[1] == free_place):
            robot_step_list = [key,2]
        elif (val[1] == val[2] == symbol) and (val[0] == free_place):
            robot_step_list = [key,1]
        else:
            continue
        return robot_step_list


def check_2_column_elements(dict, symbol):
    # game_progress_dict = {
    #         1: ['-', '-', '-'],
    #         2: ['-', '-', '-'],
    #         3: ['-', '-', '-']
    #     }
    if (dict[1][0] == dict[2][0] == symbol) and (dict[3][0] == free_place):
        robot_step_list = [3,1]
    elif (dict[1][0] == dict[3][0] == symbol) and (dict[2][0] == free_place):
        robot_step_list = [2,1]
    elif (dict[2][0] == dict[3][0] == symbol) and (dict[2][0] == free_place):
        robot_step_list = [1,1]

    elif (dict[1][1] == dict[2][1] == symbol) and (dict[3][1] == free_place):
        robot_step_list = [3,2]
    elif (dict[1][1] == dict[3][1] == symbol) and (dict[2][1] == free_place):
        robot_step_list = [2,2]
    elif (dict[2][1] == dict[3][1] == symbol) and (dict[2][1] == free_place):
        robot_step_list = [1,2]

    elif (dict[1][2] == dict[2][2] == symbol) and (dict[3][2] == free_place):
        robot_step_list = [3,3]
    elif (dict[1][2] == dict[3][2] == symbol) and (dict[2][2] == free_place):
        robot_step_list = [2,3]
    elif (dict[2][2] == dict[3][2] == symbol) and (dict[1][2] == free_place):
        robot_step_list = [1,3]
    else:
        return False
    return robot_step_list


def check_2_diagonal_elements(dict, symbol):
    # game_progress_dict = {
    #         1: ['-', '-', '-'],
    #         2: ['-', '-', '-'],
    #         3: ['-', '-', '-']
    #     }
    if (dict[1][0] == dict[2][1] == symbol) and (dict[3][2] == free_place):
        robot_step_list = [3, 3]
    elif (dict[1][0] == dict[3][2] == symbol) and (dict[2][1] == free_place):
        robot_step_list = [2, 2]
    elif (dict[2][1] == dict[3][2] == symbol) and (dict[1][0] == free_place):
        robot_step_list = [1, 1]

    elif (dict[1][2] == dict[2][1] == symbol) and (dict[3][0] == free_place):
        robot_step_list = [3, 1]
    elif (dict[1][2] == dict[3][0] == symbol) and (dict[2][1] == free_place):
        robot_step_list = [2, 2]
    elif (dict[2][1] == dict[3][0] == symbol) and (dict[1][2] == free_place):
        robot_step_list = [1, 3]
    else:
        return False
    return robot_step_list


def robot_tactic(dict, symbol_robot, symbol_user):
    # проверяем середину. Если свободно, то сразу ставим туда наш symbol_robot и вовзращаем robot_step_list
    if dict[2][1] == free_place:
        fill_game_progress_dict(dict, [2,2], symbol_robot)
    # если середина занята ИГРОКОМ, то пытаемся выиграть:
    elif dict[2][1] == symbol_user:
        # if ДИАГОНАЛЬ есть НАШИ символы, то:
        if check_2_diagonal_elements(dict, symbol_robot):
            # ставим свой 3-й элемент и WIN
            robot_step_list = check_2_diagonal_elements(dict, symbol_robot)
            fill_game_progress_dict(dict, robot_step_list, symbol_robot)
            # if ЛИНИИ есть НАШИ символы, то:
        elif check_2_line_elements(dict, symbol_robot):
            # ставим свой 3-й элемент и WIN
            robot_step_list = check_2_line_elements(dict, symbol_robot)
            fill_game_progress_dict(dict, robot_step_list, symbol_robot)
            # if СТОЛБЦЫ есть НАШИ символы, то:
        elif check_2_column_elements(dict, symbol_robot):
            # ставим свой 3-й элемент и WIN
            robot_step_list = check_2_column_elements(dict, symbol_robot)
            fill_game_progress_dict(dict, robot_step_list, symbol_robot)

        # if КРЕСТ и ДИАГОНАЛЬ нет НАШИХ символов, то пытаемся обрезать шаги ИГРОКУ если он почему-то имеет 2 символа:
            # if КРЕСТ и ДИАГОНАЛЬ ЕСТЬ символы ИГРОКА, тогда:
            # ставим СВОЙ 3-й элемент и не даём выиграть ИГРОКУ

        if check_2_diagonal_elements(dict, symbol_user):
            # ставим свой 3-й элемент и WIN
            robot_step_list = check_2_diagonal_elements(dict, symbol_user)
            fill_game_progress_dict(dict, robot_step_list, symbol_robot)
            # if ЛИНИИ есть НАШИ символы, то:
        elif check_2_line_elements(dict, symbol_user):
            # ставим свой 3-й элемент и WIN
            robot_step_list = check_2_line_elements(dict, symbol_user)
            fill_game_progress_dict(dict, robot_step_list, symbol_robot)
            # if СТОЛБЦЫ есть НАШИ символы, то:
        elif check_2_column_elements(dict, symbol_user):
            # ставим свой 3-й элемент и WIN
            robot_step_list = check_2_column_elements(dict, symbol_user)
            fill_game_progress_dict(dict, robot_step_list, symbol_robot)

        # if КРЕСТ и ДИАГОНАЛЬ нет символов ИГРОКА, то:
        else:
        # проверяем углы и крестовые
            robot_step_list = check_corner_and_christ_elements(dict)
            # ставим в угол symbol_robot.
            fill_game_progress_dict(dict, robot_step_list, symbol_robot)

    # но если середина занята РОБОТОМ, то:
    elif dict[2][1] == symbol_robot:
        # if КРЕСТ и ДИАГОНАЛЬ есть НАШИ символы, то:
        if check_2_diagonal_elements(dict, symbol_robot):
            # ставим свой 3-й элемент и WIN
            robot_step_list = check_2_diagonal_elements(dict, symbol_robot)
            fill_game_progress_dict(dict, robot_step_list, symbol_robot)
        elif check_2_line_elements(dict, symbol_robot):
            robot_step_list = check_2_line_elements(dict, symbol_robot)
            fill_game_progress_dict(dict, robot_step_list, symbol_robot)
        elif check_2_column_elements(dict, symbol_robot):
            robot_step_list = check_2_column_elements(dict, symbol_robot)
            fill_game_progress_dict(dict, robot_step_list, symbol_robot)

        # if КРЕСТ и ДИАГОНАЛЬ нет НАШИХ символов, то:
            # проверяем не успел ли ИГРОК вперед:
            # if КРЕСТ и ДИАГОНАЛЬ ЕСТЬ символов ИГРОКА, тогда:
        if check_2_diagonal_elements(dict, symbol_user):
            # ставим СВОЙ 3-й элемент и не даём выиграть ИГРОКУ
            robot_step_list = check_2_diagonal_elements(dict, symbol_user)
            fill_game_progress_dict(dict, robot_step_list, symbol_robot)
        elif check_2_line_elements(dict, symbol_user):
            robot_step_list = check_2_line_elements(dict, symbol_user)
            fill_game_progress_dict(dict, robot_step_list, symbol_robot)
        elif check_2_column_elements(dict, symbol_user):
            robot_step_list = check_2_column_elements(dict, symbol_user)
            fill_game_progress_dict(dict, robot_step_list, symbol_robot)

        # if КРЕСТ и ДИАГОНАЛЬ нет символов ИГРОКА (а значит они свободные), то:
            # проверяем углы
        else:
            robot_step_list = check_corner_and_christ_elements(dict)
            # ставим в свбодное место в углу наш символ
            fill_game_progress_dict(dict, robot_step_list, symbol_robot)


game_progress_dict = {
    1: ['-', '-', '-'],
    2: ['-', '-', '-'],
    3: ['-', '-', '-']
}

if game_type == '2':

    user_1 = input('Введите имя первого игрока, он играет крестиками: ')
    user_2 = input('Введите имя второго игрока, он играет ноликами: ')
    print(f'{user_1}, {user_2}, вот ваше игровое поле:')
    print_game_field(game_progress_dict)
    print('')
    i = 0
    while i < 9:
        game_process(user_1, game_progress_dict, 'x')
        i += 1
        if win_check(game_progress_dict):
            print(f'{user_1}, ПОЗДРАВЛЯЕМ! Вы выиграли за {i} ходов!')
            print(f'{user_2}, ну а вы проиграли!')
            break
        if i == 9:
            print('НИЧЬЯ! Оба молодцы!')
        game_process(user_2, game_progress_dict, 'o')
        i += 1
        if win_check(game_progress_dict):
            print(f'{user_2}, ПОЗДРАВЛЯЕМ! Вы выиграли за {i} ходов!')
            print(f'{user_1}, ну а вы проиграли!')
            break
        if i == 9:
            print('НИЧЬЯ! Оба молодцы!')

else:

    game_mode = input('Вы хотите играть первым за крестики (введите 1) или вторым за нолики (введите любой '
                      'другой символ): ')
    if game_mode == '1':
        user = input('Введите ваше имя, вы играете крестиками (х): ')
        print(f'{user}, против вас играет компьютер!')
        time.sleep(1)
        print(f'Вот ваше игровое поле:')
        print_game_field(game_progress_dict)
        print('')
        i = 0

        while i < 9:
            # ход игрока
            game_process(user, game_progress_dict, 'x')
            i += 1
            if win_check(game_progress_dict):
                print(f'{user}, ПОЗДРАВЛЯЕМ! Вы выиграли у робота за {i} ходов!')
                break
            if i == 9:
                print('НИЧЬЯ! Вы держались молодцом!')
                break
            # ход компьютера
            robot_tactic(game_progress_dict, 'o', 'x')
            i += 1
            print_game_field(game_progress_dict)
            if win_check(game_progress_dict):
                print(f'{user}, вы проиграли! Компьютер выиграл у вас за {i} ходов!')
                break
            if i == 9:
                print('НИЧЬЯ! Вы держались молодцом!')
                break
    else:
        user = input('Введите ваше имя, вы играете ноликами (о): ')
        print(f'{user}, против вас играет компьютер!')
        print(f'Вот ваше игровое поле:')
        time.sleep(1)
        print_game_field(game_progress_dict)
        print('')
        i = 0

        while i < 9:
            # ход компьютера
            robot_tactic(game_progress_dict, 'x', 'o')
            i += 1
            print_game_field(game_progress_dict)
            if win_check(game_progress_dict):
                print(f'{user}, вы проиграли! Компьютер выиграл у вас за {i} ходов!')
                break
            if i == 9:
                print('НИЧЬЯ! Вы держались молодцом!')
                break
            # ход игрока
            game_process(user, game_progress_dict, 'o')
            i += 1
            if win_check(game_progress_dict):
                print(f'{user}, ПОЗДРАВЛЯЕМ! Вы выиграли у робота за {i} ходов!')
                break
            if i == 9:
                print('НИЧЬЯ! Вы держались молодцом!')










