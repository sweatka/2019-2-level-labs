"""
Labour work #2. Levenshtein distance.
"""


def generate_edit_matrix(num_rows: int, num_cols: int) -> list:
    if isinstance(num_rows, int) and isinstance(num_cols, int):
        matrix = []
        for i in range(num_rows):
            matrix.append([])
            for j in range(num_cols):
                matrix[i].append(0)
        return matrix
    else:
        return []


def initialize_edit_matrix(edit_matrix: tuple, add_weight: int, remove_weight: int) -> list:
    edit_matrix_l = list(edit_matrix)
    if edit_matrix_l and len(edit_matrix_l[0]) and isinstance(add_weight, int) and isinstance(remove_weight, int):
        edit_matrix_l[0][0] = 0
        i = 1
        j = 1
        while i < len(edit_matrix_l):
            edit_matrix_l[i][0] = edit_matrix_l[i - 1][0] + remove_weight
            i += 1
        while j < len(edit_matrix_l[0]):
            edit_matrix_l[0][j] = edit_matrix_l[0][j - 1] + add_weight
            j += 1
        return edit_matrix_l
    else:
        return list(edit_matrix)


def minimum_value(numbers: tuple) -> int:
    return min(numbers)


def fill_edit_matrix(edit_matrix: tuple,
                     add_weight: int,
                     remove_weight: int,
                     substitute_weight: int,
                     original_word: str,
                     target_word: str) -> list:
    edit_matrix_l = list(edit_matrix)
    if edit_matrix_l:
        if isinstance(remove_weight, int) and isinstance(add_weight, int) \
                and isinstance(substitute_weight, int) and isinstance(target_word, str) \
                and isinstance(original_word, str):
            for i in range(1, len(edit_matrix_l)):
                for j in range(1, len(edit_matrix_l[0])):
                    insert_number = edit_matrix_l[i][j - 1] + add_weight
                    remove_number = edit_matrix_l[i - 1][j] + remove_weight
                    if original_word[i - 1] == target_word[j - 1]:
                        substitute_number = 0 + edit_matrix_l[i - 1][j - 1]
                    else:
                        substitute_number = edit_matrix_l[i - 1][j - 1] + substitute_weight
                    edit_matrix_l[i][j] = minimum_value((insert_number, remove_number, substitute_number))
    return list(edit_matrix_l)


def find_distance(original_word: str,
                  target_word: str,
                  add_weight: int,
                  remove_weight: int,
                  substitute_weight: int) -> int:
    if isinstance(remove_weight, int) and isinstance(add_weight, int) \
            and isinstance(substitute_weight, int) and isinstance(target_word, str) \
            and isinstance(original_word, str):
        n = len(original_word) + 1
        m = len(target_word) + 1
        zero_matrix = generate_edit_matrix(n, m)
        init_matrix = initialize_edit_matrix(tuple(zero_matrix), add_weight, remove_weight)
        final_matrix = fill_edit_matrix(tuple(init_matrix), add_weight, remove_weight, substitute_weight, original_word,
                                        target_word)
        distance = final_matrix[-1][-1]
        return distance
    else:
        return -1


def save_to_csv(edit_matrix: tuple, path_to_file: str) -> None:
    file = open(path_to_file, 'w')
    for line in edit_matrix:
        for element in line:
            file.write(str(element) + ',')
        file.write('\n')
    file.close()


def load_from_csv(path_to_file: str) -> list:
    numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    with open(path_to_file) as file:
        matrix_future = []
        for row in file:
            line_future = []
            for element in row:
                if element in numbers:
                    line_future.append(int(element))
            matrix_future.append(line_future)
    return matrix_future

