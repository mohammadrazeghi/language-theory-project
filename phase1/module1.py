import math

import FA_class
import visualizer
import utils
import sys

imageType = list[list[int]]

def solve(image: imageType) -> 'DFA':
    fixed_length = len(image)
    length = fixed_length
    matrix = [['' for _ in range(length)] for _ in range(length)]
    number_of_loop = int(math.sqrt(length))
    ceil = 0
    floor = length/2
    left_wall = 0
    right_wall = length/2

    for i in range(fixed_length):
        for j in range(fixed_length):
            length = fixed_length
            ceil = 0
            floor = length / 2
            left_wall = 0
            right_wall = length / 2
            for k in range(number_of_loop):
                if ceil <= i < floor:
                    if left_wall <= j < right_wall:
                        matrix[i][j] += "0"
                        length = length / 2
                        floor = floor/2
                        right_wall = right_wall/2

                    else:
                        matrix[i][j] += "1"
                        length = length / 2
                        left_wall = right_wall
                        right_wall += right_wall/2
                        floor = floor/2

                else:
                    if j < right_wall:
                        matrix[i][j] += "2"
                        length = length / 2
                        ceil = floor
                        floor = floor + floor/2
                        right_wall = right_wall/2

                    else:
                        matrix[i][j] += "3"
                        length = length / 2
                        left_wall = right_wall
                        ceil = floor
                        right_wall += right_wall/2
                        floor += floor/2

    return matrix









if __name__ == "__main__":
    image = [[1, 1, 1, 1],
             [1, 0, 1, 0],
             [0, 1, 0, 1],
             [1, 1, 1, 1]]

    utils.save_image(image)
    unknown = FA_class.DFA()
    fa = solve(image)
    print(fa)
    print(fa.serialize_json())
