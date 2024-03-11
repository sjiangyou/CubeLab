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
    
    def generate_scramble(self):
        moves = ['F', 'U', 'R', 'L', 'D', 'B']
        rotation_modifiers = ['', '2', '\'']
        layer_modifiers = ['', '']
        scramble = []
        if(self.puzzle.isnumeric()):
            layer_modifiers = list(range(1, ((int(self.puzzle) // 2) + 1)))
            length = 30 * (int(self.puzzle) - 2)
            if(self.puzzle == '2'):
                moves = ['F', 'U', 'R']
                length = 20
        elif(self.puzzle[0] == 'M'):
            moves = ['--', '-+', '+-', '++']
            rotation_modifiers = ['', '', '']
            length = 42
        else:
            length = 30
            del rotation_modifiers[1]
            if(self.puzzle[0] == 'P'):
                moves = ['U', 'L', 'R', 'B', 'u', 'l', 'r', 'b']
            elif(self.puzzle[0] == 'C'):
                length = 15
                moves = [str(i) for i in range(-5, 7)]
            elif(self.puzzle.find('1') == -1):
                moves = ['U', 'L', 'R', 'B']
            else:
                self.scramble = 'Square-1 is not supported. '
                return 'Square-1 is not supported. '
        layer_modifiers[0] = ''
        return_value = ''
        prev_moves = []
        while(len(scramble) < length):
            new_move = (random.choice(moves), 
                        random.choice(rotation_modifiers),
                        random.choice(layer_modifiers))
            if(self.puzzle[0] != 'M' and self.puzzle[0] != 'C'):
                try:
                    prev_moves.index(new_move[0][0])
                    continue
                except (ValueError, IndexError):pass
            if type(new_move[2]) == int:
                new_move = (new_move[0] + 'w', new_move[1], new_move[2]) if self.puzzle != '3' else (new_move[0], new_move[1], new_move[2])
                if new_move[2] == 2:
                    new_move = (new_move[0], new_move[1], '')
            scramble.append(new_move)
            prev_moves.append(new_move[0][0])
            prev_moves = prev_moves[-2:]
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
        for move in scramble:
            return_value = f'{return_value}{str(move[2])}{move[0]}{move[1]} '
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