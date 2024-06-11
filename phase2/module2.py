from phase1.FA_class import DFA
from utils import utils
from utils.utils import imageType
import math


percentage = 0

def bit_addressing(image):
    fixed_length = len(image)
    matrix = [['' for _ in range(fixed_length)] for _ in range(fixed_length)]
    number_of_loops = int(math.log2(fixed_length))

    for i in range(fixed_length):
        for j in range(fixed_length):
            bit_address = []
            ceil, floor, left_wall, right_wall = 0, fixed_length, 0, fixed_length

            for _ in range(number_of_loops):
                mid_horizontal = (ceil + floor) // 2
                mid_vertical = (left_wall + right_wall) // 2

                if i < mid_horizontal:
                    floor = mid_horizontal
                    if j < mid_vertical:
                        right_wall = mid_vertical
                        bit_address.append('0')
                    else:
                        left_wall = mid_vertical
                        bit_address.append('1')
                else:
                    ceil = mid_horizontal
                    if j < mid_vertical:
                        right_wall = mid_vertical
                        bit_address.append('2')
                    else:
                        left_wall = mid_vertical
                        bit_address.append('3')

            matrix[i][j] = ''.join(bit_address)

    return matrix

def solve(json_str: str, image: imageType) -> bool:
    fa = DFA.deserialize_json(json_str)
    matrix = bit_addressing(image)
    current_state = fa.init_state
    count = 0
    for i in range(len(image)):
        for j in range(len(image)):
            input_symbol = matrix[i][j]
            for k in range (len(input_symbol)):
                current_state = current_state.transitions[input_symbol[k]]
            if fa.is_final(current_state):
                matrix[i][j] = 1
                if image[i][j] == matrix[i][j]:
                    count += 1
                current_state = fa.init_state
            else:
                matrix[i][j] = 0
                if image[i][j] == matrix[i][j]:
                    count += 1
                current_state = fa.init_state
    #print(matrix)
    global percentage
    percentage = (count / len(matrix)**2) * 100
    if count == (len(matrix)**2):
        return 1
    return 0




if __name__ == "__main__":
    print(
        solve(
            '{"states": ["q_0", "q_1", "q_2", "q_3", "q_4"], "initial_state": "q_0", "final_states": ["q_3"], '
            '"alphabet": ["0", "1", "2", "3"], "q_0": {"0": "q_1", "1": "q_1", "2": "q_2", "3": "q_2"}, "q_1": {"0": '
            '"q_3", "1": "q_3", "2": "q_3", "3": "q_4"}, "q_2": {"0": "q_4", "1": "q_3", "2": "q_3", "3": "q_3"}, '
            '"q_3": {"0": "q_3", "1": "q_3", "2": "q_3", "3": "q_3"}, "q_4": {"0": "q_4", "1": "q_4", "2": "q_4", '
            '"3": "q_4"}}',
            [[1, 1, 1, 1],
             [1, 0, 1, 0],
             [0, 1, 0, 1],
             [1, 1, 1, 1]]
        )
    )