import random


class Computer:
    def __init__(self, file, puzzle) -> None:
        self.file: str = file
        self.puzzle: str = puzzle
        self.times: list[str] = []
        self.name: str = ""
        self.pb_single: str = ""
        self.pb_avg: str = ""
        self.pb_scramble: str = ""
        self.single: bool = False
        self.average: bool = False
        self.average_type: str = "AO5"
        self.scramble: str = ""

    def read_file(self) -> None:
        with open(self.file, "r", encoding="utf-8") as file:
            text: str = file.read()
        textlines: list[str] = text.split("\n")
        name = textlines[0]
        average_type = textlines[2][0:3]
        pb_avg, pb_single = textlines[2][5:], textlines[1][3:]
        pb_scramble = textlines[3][13:]
        temp_lst = textlines[4:]
        times_lst = [elem.split(" ") for elem in temp_lst]
        return_lst = [t for lst in times_lst for t in lst]
        return_lst = [elem for elem in return_lst if elem != ""]
        (
            self.times,
            self.name,
            self.pb_single,
            self.pb_avg,
            self.pb_scramble,
            self.average_type,
        ) = (return_lst, name, pb_single, pb_avg, pb_scramble, average_type)

    def set_possible_moves(self) -> tuple:
        moves = []
        rotation_modifiers = []
        layer_modifiers = []
        if self.puzzle.isnumeric():
            moves = ["F", "U", "R", "L", "D", "B"]
            rotation_modifiers = ["", "2", "'"]
            if int(self.puzzle) > 7:
                self.scramble = "Non-WCA. "
                return "Non-WCA. ", None, None, None
            layer_modifiers = [str(x) for x in range(1, ((int(self.puzzle) // 2) + 1))]
            length = 20 * (int(self.puzzle) - 2)
            if self.puzzle == "2":
                moves = ["F", "U", "R"]
                length = 10
        elif self.puzzle[0] == "M":
            moves = ["--", "-+", "+-", "++"]
            rotation_modifiers = [""]
            layer_modifiers = [""]
            length = 42
        else:
            length = 15
            rotation_modifiers = ["", "'"]
            layer_modifiers = [""]
            if self.puzzle[0] == "P":
                moves = ["U", "L", "R", "B", "u", "l", "r", "b"]
            elif self.puzzle[0] == "C":
                moves = [str(i) for i in range(-5, 7)]
                del rotation_modifiers[1]
            elif self.puzzle.find("1") == -1:
                moves = ["U", "L", "R", "B"]
            elif self.puzzle[0] == "S":
                del rotation_modifiers[1]
                top_moves = [0, 1, 3, 4, 6, 7, 10]
                bottom_moves = [0, 2, 3, 5, 6, 8, 9, 11]
                moves = [
                    f"{top},{bottom}" for bottom in bottom_moves for top in top_moves
                ]
                length += random.randint(-5, 5)
            else:
                self.scramble = "Invalid Puzzle. "
                return "Invalid Puzzle. ", None, None, None
        layer_modifiers[0] = ""
        return moves, rotation_modifiers, layer_modifiers, length

    def generate_scramble(self) -> str:
        moves, rotation_modifiers, layer_modifiers, length = self.set_possible_moves()
        if isinstance(moves, str):
            return moves
        scramble: list[tuple] = []
        return_value = ""
        prev_moves: list[str] = []
        while len(scramble) < length:
            new_move = (
                random.choice(moves),
                random.choice(rotation_modifiers),
                random.choice(layer_modifiers),
            )
            if self.puzzle[0] != "M" and self.puzzle[0] != "C":
                try:
                    prev_moves.index(str(new_move[0][0]))
                    continue
                except (ValueError, IndexError):
                    pass
            if new_move[2].isdigit():
                new_move = (f"{new_move[0]}w", new_move[1], new_move[2])
                if new_move[2] == "2":
                    new_move = (new_move[0], new_move[1], "")
            scramble.append(new_move)
            prev_moves.append(str(new_move[0][0]))
            prev_moves = prev_moves[-2:]
            if self.puzzle[0] == "S" and self.puzzle.find("1") != -1:
                top_layer = [1, 2] * 4
                bottom_layer = [2, 1] * 4
                top_moves = [sum(top_layer[:i]) for i in range(len(top_layer))]
                bottom_moves = [sum(bottom_layer[:i]) for i in range(len(bottom_layer))]
                for i, move in enumerate(scramble):
                    top_moves = [sum(top_layer[:i]) for i in range(len(top_layer))]
                    bottom_moves = [
                        sum(bottom_layer[:i]) for i in range(len(bottom_layer))
                    ]
                    split_index = move[0].index(",")
                    top_move = int(move[0][:split_index])
                    bottom_move = int(move[0][split_index + 1 :])
                    top_index = top_moves.index(top_move)
                    bottom_index = bottom_moves.index(bottom_move)
                    u_top_layer = top_layer[top_index:] + top_layer[:top_index]
                    d_bottom_layer = (
                        bottom_layer[bottom_index:] + bottom_layer[:bottom_index]
                    )
                    slice_top_index = (
                        top_moves.index(top_move - 6)
                        if top_move >= 6
                        else top_moves.index(top_move + 6)
                    )
                    slice_top_index -= top_index
                    slice_bottom_index = (
                        bottom_moves.index(bottom_move - 6)
                        if bottom_move >= 6
                        else bottom_moves.index(bottom_move + 6)
                    )
                    slice_bottom_index -= bottom_index
                    top_layer = (
                        d_bottom_layer[slice_bottom_index:]
                        + u_top_layer[slice_top_index:]
                    )
                    bottom_layer = (
                        d_bottom_layer[:slice_bottom_index]
                        + u_top_layer[:slice_top_index]
                    )
                    top_moves = [sum(top_layer[:i]) for i in range(len(top_layer))]
                    bottom_moves = [
                        sum(bottom_layer[:i]) for i in range(len(bottom_layer))
                    ]
                idx = 0
                while idx < len(top_moves):
                    try:
                        if top_moves[idx] < 6:
                            top_moves.index(top_moves[idx] + 6)
                        else:
                            top_moves.index(top_moves[idx] - 6)
                    except ValueError:
                        del top_moves[idx]
                        continue
                    idx += 1
                idx = 0
                while idx < len(bottom_moves):
                    try:
                        if bottom_moves[idx] < 6:
                            bottom_moves.index(bottom_moves[idx] + 6)
                        else:
                            bottom_moves.index(bottom_moves[idx] - 6)
                    except ValueError:
                        del bottom_moves[idx]
                        continue
                    idx += 1
                moves = [
                    f"{top},{bottom}" for bottom in bottom_moves for top in top_moves
                ]
                del moves[0]
        if self.puzzle[0] == "M":
            for i, move in enumerate(scramble):
                if i % 6 == 5:
                    scramble[i] = ("U", random.choice(("", "'")), "")
        if self.puzzle[0] == "C":
            move_order = [
                "UR",
                "DR",
                "DL",
                "UL",
                "U",
                "R",
                "D",
                "L",
                "ALL",
                "y2",
                "U",
                "R",
                "D",
                "L",
                "ALL",
            ]
            for i, move in enumerate(scramble):
                if i == 9:
                    scramble[i] = ("y2", "", "")
                else:
                    if int(move[0]) >= 0:
                        scramble[i] = (move_order[i], f"{move[0]}+", "")
                    else:
                        scramble[i] = (move_order[i], f"{move[0][1]}-", "")
        if self.puzzle[0] == "S" and self.puzzle.find("1") != -1:
            for i, move in enumerate(scramble):
                temp = move[0]
                split_index = temp.index(",")
                top_move = int(temp[:split_index])
                bottom_move = int(temp[split_index + 1 :])
                temp = [top_move, bottom_move]
                if top_move > 6:
                    temp[0] -= 12
                if bottom_move > 6:
                    temp[1] -= 12
                scramble[i] = (
                    (f"{temp[0]},{temp[1]} /", "", "")
                    if i < length
                    else (f"{temp[0]},{temp[1]}", "", "")
                )
        for move in scramble:
            return_value = f"{return_value}{str(move[2])}{str(move[0])}{str(move[1])} "
        self.scramble = return_value
        return return_value

    def prepare_times(self, length) -> list:
        if self.times == []:
            return []
        float_times = [
            float(time) if time != "DNF" else float("inf") for time in self.times
        ]
        lst_copy = list(float_times[:length])
        lst_copy.sort()
        return lst_copy

    def do_mean(self, length) -> float | str:
        lst_copy = self.prepare_times(length)
        if len(lst_copy) < length:
            return "NA"
        mean_time = (sum(lst_copy)) / (len(lst_copy))
        return round(mean_time, 2)

    def do_avg(self, length) -> float | str:
        lst_copy = self.prepare_times(length)
        updated_times_lst = lst_copy[1 : len(lst_copy) - 1]
        if len(updated_times_lst) < length - 2:
            return "NA"
        avg_time = (sum(updated_times_lst)) / (len(updated_times_lst))
        return round(avg_time, 2)

    def calculate_average(self, average) -> float | str:
        length = int(average[2:])
        if str(average[0]).upper() == "A":
            return self.do_avg(length)
        if str(average[0]).upper() == "M":
            return self.do_mean(length)
        return "NA"

    def convert_time(self, time) -> float:
        if time == "DNF":
            return float("inf")
        time = str(time)
        time = time.split(":")
        time.reverse()
        time = [float(u) for u in time]
        for i, elem in enumerate(time):
            time[i] = elem * (60**i)
        time = sum(time)
        return time

    def convert_fasttime(self, time) -> str:
        if time in ("NA", "DNF"):
            return time
        if not time.isdigit():
            time = time.replace(":", "").replace(".", "")
        indicies = [i for i in range(len(time)) if i % 2 == len(time) % 2]
        if len(time) % 2 == 1:
            indicies.insert(0, 0)
        splits = [time[i:j] for i, j in zip(indicies, indicies[1:] + [None])]
        final_time = ""
        for i, elem in enumerate(splits):
            final_time += elem + ":" if i != len(splits) - 2 else elem + "."
        return str(self.convert_time(final_time[:-1]))

    def run(self, new_time, previous_scramble) -> None:
        if new_time.replace(".", "").replace(":", "").isdigit() or new_time == "DNF":
            new_time = self.convert_fasttime(new_time)
            self.times.insert(0, new_time)
            current_average = str(self.calculate_average(self.average_type))
            if (new_time and not self.pb_single) or (
                new_time != "DNF" and float(new_time) <= float(self.pb_single)
            ):
                self.single = True
                self.pb_scramble = previous_scramble
                self.pb_single = new_time
            if (
                current_average != "NA" and not (self.pb_avg or self.pb_avg == " ")
            ) or (
                len(self.times) >= int(self.average_type[2:])
                and float(current_average) <= float(self.pb_avg)
            ):
                self.average = True
                self.pb_avg = str(current_average)
            self.write_file()

    def write_file(self) -> None:
        with open(self.file, "w", encoding="utf-8") as file:
            return_str = (
                f"{self.name}\nS: {str(self.pb_single)}\n"
                + f"{self.average_type}: {str(self.pb_avg)}\n"
                + f"PB Scramble: {self.pb_scramble}"
            )
            if len(self.times) != 0:
                return_str += "\n"
            for i, time in enumerate(self.times):
                time = str(round(self.convert_time(time), 2))
                if time == "inf":
                    time = "DNF"
                if time.find(".") == len(time) - 2:
                    time += "0"
                return_str += time
                if i == len(self.times) - 1:
                    break
                if i % 10 == 9:
                    return_str += "\n"
                else:
                    return_str += " "
            file.write(str(return_str))
