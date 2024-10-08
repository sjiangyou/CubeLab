import random

class Computer:
    def __init__(self, file, puzzle):
        self.file = file
        self.puzzle = puzzle
        self.times = []
        self.single = False
        self.average = False
        self.average_type = 'AO5'
    
    def read_file(self):
        file = open(self.file, 'r')
        text = file.read()
        text = text.split('\n')
        name = text[0]
        average_type = text[2][0:3]
        PB_avg, PB_single = text[2][5:], text[1][3:]
        PB_scramble = text[3][13:]
        times_lst = text[4:]
        if(PB_single == None):
            PB_avg = None
        times_lst = [elem.split(' ') for elem in times_lst]
        return_lst = [t for lst in times_lst for t in lst]
        self.times, self.name, self.PB_single, self.PB_avg, self.PB_scramble, self.average_type \
        = return_lst, name, PB_single, PB_avg, PB_scramble, average_type
        file.close()
    
    def set_possible_moves(self):
        moves = ['F', 'U', 'R', 'L', 'D', 'B']
        rotation_modifiers = ['', '2', '\'']
        layer_modifiers = ['', '']
        if(self.puzzle.isnumeric()):
            if(int(self.puzzle) > 7):
                self.scramble = 'Non-WCA. '
                return 'Non-WCA. ', None, None, None
            layer_modifiers = list(range(1, ((int(self.puzzle) // 2) + 1)))
            length = 20 * (int(self.puzzle) - 2)
            if(self.puzzle == '2'):
                moves = ['F', 'U', 'R']
                length = 10
        elif(self.puzzle[0] == 'M'):
            moves = ['--', '-+', '+-', '++']
            rotation_modifiers = ['']
            del layer_modifiers[1]
            length = 42
        else:
            length = 30
            del rotation_modifiers[1]
            del layer_modifiers[1]
            if(self.puzzle[0] == 'P'):
                moves = ['U', 'L', 'R', 'B', 'u', 'l', 'r', 'b']
            elif(self.puzzle[0] == 'C'):
                length = 15
                moves = [str(i) for i in range(-5, 7)]
                del rotation_modifiers[1]
            elif(self.puzzle.find('1') == -1):
                moves = ['U', 'L', 'R', 'B']
            elif(self.puzzle[0] == 'S'):
                length = 15
                del rotation_modifiers[1]
                top_moves = [0, 1, 3, 4, 6, 7, 10]
                bottom_moves = [0, 2, 3, 5, 6, 8, 9, 11]
                moves = [[top, bottom] for bottom in bottom_moves for top in top_moves]
                length += random.randint(-5, 5)
            else:
                self.scramble = 'Invalid Puzzle. '
                return 'Invalid Puzzle. ', None, None, None
        layer_modifiers[0] = ''
        return moves, rotation_modifiers, layer_modifiers, length
    
    def generate_scramble(self):
        moves, rotation_modifiers, layer_modifiers, length = self.set_possible_moves()
        if(type(moves) == str):
            return moves
        scramble = []
        return_value = ''
        prev_moves = []
        while(len(scramble) < length):
            new_move = (random.choice(moves), random.choice(rotation_modifiers), random.choice(layer_modifiers))
            if(self.puzzle[0] != 'M' and self.puzzle[0] != 'C'):
                try:
                    prev_moves.index(new_move[0][0])
                    continue
                except(ValueError, IndexError): pass
            if type(new_move[2]) == int:
                new_move = (new_move[0] + 'w', new_move[1], new_move[2])
                if new_move[2] == 2:
                    new_move = (new_move[0], new_move[1], '')
            scramble.append(new_move)
            prev_moves.append(new_move[0][0])
            prev_moves = prev_moves[-2:]
            if(self.puzzle[0] == 'S' and self.puzzle.find('1') != -1):
                top_layer = [1, 2] * 4
                bottom_layer = [2, 1] * 4
                top_moves = [sum(top_layer[:i]) for i in range(len(top_layer))]
                bottom_moves = [sum(bottom_layer[:i]) for i in range(len(bottom_layer))]
                for i, move in enumerate(scramble):
                    top_moves = [sum(top_layer[:i]) for i in range(len(top_layer))]
                    bottom_moves = [sum(bottom_layer[:i]) for i in range(len(bottom_layer))]
                    top_index = top_moves.index(move[0][0])
                    bottom_index = bottom_moves.index(move[0][1])
                    U_top_layer = top_layer[top_index:] + top_layer[:top_index]
                    D_bottom_layer = bottom_layer[bottom_index:] + bottom_layer[:bottom_index]
                    slice_top_index = top_moves.index(move[0][0] - 6) if move[0][0] >= 6 else top_moves.index(move[0][0] + 6)
                    slice_top_index -= top_index
                    slice_bottom_index = bottom_moves.index(move[0][1] - 6) if move[0][1] >= 6 else bottom_moves.index(move[0][1] + 6)
                    slice_bottom_index -= bottom_index
                    top_layer = D_bottom_layer[slice_bottom_index:] + U_top_layer[slice_top_index:]
                    bottom_layer = D_bottom_layer[:slice_bottom_index] + U_top_layer[:slice_top_index]
                    top_moves = [sum(top_layer[:i]) for i in range(len(top_layer))]
                    bottom_moves = [sum(bottom_layer[:i]) for i in range(len(bottom_layer))]
                idx = 0
                while idx < len(top_moves):
                    try:
                        if top_moves[idx] < 6: top_moves.index(top_moves[idx] + 6)
                        else: top_moves.index(top_moves[idx] - 6)
                    except ValueError:
                        del top_moves[idx]
                        continue
                    idx += 1
                idx = 0
                while idx < len(bottom_moves):
                    try:
                        if bottom_moves[idx] < 6: bottom_moves.index(bottom_moves[idx] + 6)
                        else: bottom_moves.index(bottom_moves[idx] - 6)
                    except ValueError:
                        del bottom_moves[idx]
                        continue
                    idx += 1
                moves = [[top, bottom] for bottom in bottom_moves for top in top_moves]
                del moves[0]
        if(self.puzzle[0] == 'M'):
            for (i, move) in enumerate(scramble):
                if(i % 6 == 5):
                    scramble[i] = ('U', random.choice(('', '\'')), '')
        if(self.puzzle[0] == 'C'):
            move_order = ['UR', 'DR', 'DL', 'UL', 'U', 'R', 'D', 'L', 'ALL', 'y2', 'U', 'R', 'D', 'L', 'ALL']
            for (i, move) in enumerate(scramble):
                if i == 9:
                    scramble[i] = ('y2', '', '')
                else:
                    if int(move[0]) >= 0:
                        scramble[i] = (move_order[i], f'{move[0]}+', '')
                    else:
                        scramble[i] = (move_order[i], f'{move[0][1]}-', '')
        if(self.puzzle[0] == 'S' and self.puzzle.find('1') != -1):
            for i, move in enumerate(scramble):
                temp = move[0]
                if int(move[0][0]) > 6: temp[0] -= 12
                if int(move[0][1]) > 6: temp[1] -= 12
                scramble[i] = (f'{temp[0]},{temp[1]}/', '', '') if i < length else (f'{temp[0]},{temp[1]}', '', '')
        for move in scramble:
            return_value = f'{return_value}{str(move[2])}{str(move[0])}{str(move[1])} '
        self.scramble = return_value
        return return_value
    
    def prepare_times(self, length):
        if(self.times == []):
            return('NA')
        self.times = [float(time) if time != 'DNF' else float('inf') for time in self.times]
        lst_copy = list(self.times[:length])
        lst_copy.sort()
        return lst_copy
    
    def do_mean(self, length):
        lst_copy = self.prepare_times(length)
        if(len(lst_copy) < length):
            return 'NA'
        mean_time = (sum(lst_copy))/(len(lst_copy))
        if(mean_time == float('inf')):
            return 'DNF'
        return(round(mean_time, 2))
    
    def do_avg(self, length):
        lst_copy = self.prepare_times(length)
        updated_times_lst = lst_copy[1:len(lst_copy) - 1]
        if(len(updated_times_lst) < length - 2):
            return 'NA'
        avg_time = (sum(updated_times_lst))/(len(updated_times_lst))
        if(avg_time == float('inf')):
            return'DNF'
        return(round(avg_time, 2))
    
    def calculate_average(self, average):
        length = int(average[2:])
        if(str(average[0]).upper() == 'A'):
            return self.do_avg(length)
        elif(str(average[0]).upper() == 'M'):
            return self.do_mean(length)
        else:
            return 'NA'
        
    def convert_time(self, time):
        if(time == 'DNF'):
            return float('inf')
        if(time == 'NA'):
            return 'NA'
        time = str(time)
        time = time.split(':')
        time.reverse()
        time = [float(u) for u in time]
        for j in range(len(time)):
            time[j] *= (60 ** j)
        time = sum(time)
        return time

    def convert_fasttime(self, time):
        if not time.isdigit():
            return str(self.convert_time(time))
        else:
            indicies = [i for i in range(len(time)) if i % 2 == len(time) % 2]
            if len(time) % 2 == 1:indicies.insert(0, 0)
            splits = [time[i:j] for i,j in zip(indicies, indicies[1:] + [None])] 
            final_time = ''
            for i, elem in enumerate(splits):
                final_time += elem + ':' if i != len(splits) - 2 else elem + '.'
            return str(self.convert_time(final_time[:-1]))

    def run(self, new_time):
        if(new_time.replace('.', '').replace(':','').isdigit() or new_time == 'DNF'):
            new_time = self.convert_fasttime(new_time)
            self.times.insert(0, new_time)
            current_average = self.convert_time(self.calculate_average(self.average_type))
            if((new_time and not self.PB_single) or float(new_time) <= float(self.PB_single)):
                self.single = True
                self.PB_scramble = self.scramble
                self.PB_single = new_time
            if((current_average != 'NA' and not (self.PB_avg or self.PB_avg == ' ')) or (len(self.times) >= int(self.average_type[2:]) and current_average <= float(self.PB_avg))):
                self.average = True
                self.PB_avg = current_average
            self.write_file()
    
    def write_file(self):
        file = open(self.file, 'w')
        return_str = f'{self.name}\nS: {str(self.PB_single)}\n{self.average_type}: {str(self.PB_avg)}\nPB Scramble: {self.PB_scramble}'
        if(len(self.times) != 0):
            return_str += '\n'
        for i, time in enumerate(self.times):
            time = str(round(self.convert_time(time), 2))
            if(time == 'inf'):
                time = 'DNF'
            if(time.find('.') == len(time) - 2):
                time += '0'
            return_str += time
            if(i == len(self.times) - 1):
                break
            elif(i % 10 == 9):
                return_str += '\n'
            else:
                return_str += ' '
        file.write(str(return_str))
        file.close()