import sys
import random

def calculator():
    f = open(sys.argv[1], 'r')
    puzzle = str(input("Puzzle: "))
    (times_lst, name, PB_single, PB_avg5, PB_scramble) = read_file(f, puzzle)
    f.close()
    scramble = generate_scramble(puzzle)
    print(name)
    print(scramble)
    new_time = str(input('Time: '))
    while(new_time.replace('.', '', 1).isdigit()):
        times_lst.insert(0, new_time)
        current_ao5 = mid_avg(times_lst[:5], 5)
        try:
            if(float(new_time) < float(PB_single)):
                PB_single = new_time
                PB_scramble = scramble
                print('New PB: ' + str(PB_single))
        except:
            PB_single = new_time
            PB_scramble = scramble
            print('New PB: ' + str(PB_single))
        try:
            if(current_ao5 < float(PB_avg5)):
                PB_avg5 = current_ao5
                print('New PB AO5: ' + str(PB_avg5))
        except:
            if(len(times_lst) > 4):
                PB_avg5 = current_ao5
                print('New PB AO5: ' + str(PB_avg5))
        print(str(current_ao5) + " Average of 5")
        print(str(mid_avg(times_lst[:12], 12)) + ' Average of 12')
        print(str(mid_avg(times_lst[:20], 20)) + ' Average of 20')
        scramble = generate_scramble(puzzle)
        print(scramble)
        new_time = str(input('Time: '))
    f = open(sys.argv[1], 'w')
    write_file(f, name, times_lst, PB_avg5, PB_single, PB_scramble)
    f.close()
    print(str(mid_avg(times_lst, len(times_lst))) + " Average of " + str(len(times_lst)))

def mid_avg(lst, length):
    for i, t in enumerate(lst):
        t = t.split(':')
        t.reverse()
        t = [float(u) for u in t]
        for j in range(len(t)):
            t[j] *= (60 ** j)
        t = sum(t)
        lst[i] = t
    lst_copy = list(lst)
    lst_copy.sort()
    updated_times_lst = lst_copy[1:len(lst_copy) - 1]
    try:
        if(len(updated_times_lst) < length - 2):
            raise ValueError
    except ValueError as e:
        return('NA')
    else:
        avg_time = (sum(updated_times_lst))/(len(updated_times_lst))
        return(round(avg_time, 2))

def read_file(file, puzzle):
    text = file.read()
    text = text.split('\n')
    name = text[0]
    (PB_avg5, PB_single) = (text[2][3:], text[1][3:])
    if(puzzle[0] == 'M'):
        PB_scramble = text[3][13:] + '\n' + text[4] + '\n' + text[5] + '\n' + text[6] + '\n' + text[7] + '\n' + text[8] + '\n' + text[9]
        times_lst = text[10:]
    else:
        PB_scramble = text[3][13:]
        times_lst = text[4:]
    if(type(PB_single) == None):
        PB_single = None
        PB_avg5 = None
    if(type(PB_avg5) == None):
        PB_avg5 = None
    for i, elem in enumerate(times_lst):
        elem = elem.split(' ')
        times_lst[i] = elem
    return_lst = []
    for lst in times_lst:
        for t in lst:
            return_lst.append(t)
    if(return_lst == None):
        return_lst = []
    return(return_lst, name, PB_single, PB_avg5, PB_scramble)
    
def write_file(file, name, times_lst, avg5, single, scramble):
    return_str = name + '\nS: ' + str(single) + '\nA: ' + str(avg5) + '\nPB Scramble: ' + scramble
    if(len(times_lst) != 0):
        return_str += '\n'
    for i, t in enumerate(times_lst):
        return_str += t
        if(i == len(times_lst) - 1):
            break
        elif(i % 10 == 9):
            return_str += '\n'
        else:
            return_str += ' '
    file.write(str(return_str))

def generate_scramble(puzzle):
    moves = ['F', 'U', 'R', 'L', 'D', 'B']
    rotation_modifiers = ['', '2', '\'']
    layer_modifiers = ['', '']
    scramble = []
    if(puzzle.isnumeric()):
        layer_modifiers = list(range(1, int(puzzle)))
        length = 30 * (int(puzzle) - 2)
        if(puzzle == '2'):
            moves = ['F', 'U', 'R']
            length = 20
    else: 
        if(puzzle[0] == 'M'):
            moves = ['--', '-+', '+-', '++']
            rotation_modifiers = ['', '', '', '\'']
            length = 77
        else:
            length = 30
            if(puzzle[0] == 'P'):
                moves = ['U', 'L', 'R', 'B', 'u', 'l', 'r', 'b']
                rotation_modifiers[1] = ''
            elif(puzzle.find('1') == -1):
                moves = ['F', 'L', 'R', 'B']
            else:
                sys.exit("We don't support Sqaure-1. Please rerun the program.")
    layer_modifiers[0] = ''
    layer_modifiers[len(layer_modifiers) - 1] = ''
    return_value = ''
    prev_moves = []
    while(len(scramble) < length):
        new_move = (moves[random.randint(0, len(moves) - 1)], rotation_modifiers[random.randint(0, 2)], layer_modifiers[random.randint(0, len(layer_modifiers) - 1)])
        try:
            prev_moves.index(new_move[0])
            continue
        except Exception as e:
            pass
        scramble.append(new_move)
        prev_moves = []
        for i in range(len(scramble)):
            prev_moves.append(scramble[i][0])
        prev_moves = prev_moves[-2:]
    if(puzzle[0] == 'M'):
        for (i, move) in enumerate(scramble):
            if(i % 11 == 10):
               scramble[i] = ('U', rotation_modifiers[random.randint(2, 3)] + '\n', '')
            if(i == 76):
                scramble[76] = ('U', rotation_modifiers[random.randint(2, 3)], '')
            
    for move in scramble:
        return_value += str(move[2])
        return_value += move[0]
        return_value += move[1]
        return_value += ' '
    return return_value 

calculator()