import FA_class
import utils
from collections import defaultdict

imageType = list[list[int]]


def get_zoomed_part(image: imageType, direction: int) -> imageType:
    n = len(image)
    half = n // 2

    if direction == 0:
        return [row[:half] for row in image[:half]]
    elif direction == 1:
        return [row[half:] for row in image[:half]]
    elif direction == 2:
        return [row[:half] for row in image[half:]]
    elif direction == 3:
        return [row[half:] for row in image[half:]]
    else:
        raise ValueError("Invalid direction. Direction must be in range [0, 3].")


def solve(image: imageType) -> 'FA_class.DFA':
    automaton = FA_class.DFA()
    states = {}  # Dictionary to store states and their corresponding images
    unique_states = {}
    count = 0
    # Step 1: i=j=0
    i = j = 0

    directions = ['0', '1', '2', '3']
    automaton.alphabet = directions

    # Step 2: Create state 0 and assign u0 = I
    state_0 = automaton.add_state(0)
    automaton.assign_initial_state(state_0)
    states[0] = image
    unique_states[str(image)] = state_0
    final_state = automaton.add_state(-1)
    automaton.add_final_state(final_state)
    automaton.add_transition(final_state, final_state, "0")
    automaton.add_transition(final_state, final_state, "1")
    automaton.add_transition(final_state, final_state, "2")
    automaton.add_transition(final_state, final_state, "3")

    while True:
        # Step 3: Process state i
        current_image = states[i]
        state_i = unique_states[str(current_image)]

        if len(current_image) == 1:
            for q, u_q in unique_states.items():
                if [[0]] == u_q:
                    fail_state = unique_states[q]
                    automaton.add_transition(fail_state, fail_state, str(0))
                    automaton.add_transition(fail_state, fail_state, str(1))
                    automaton.add_transition(fail_state, fail_state, str(2))
                    automaton.add_transition(fail_state, fail_state, str(3))
            break
        for k in range(4):
            I_w_k = get_zoomed_part(current_image, k)
            found_matching_state = False
            if str(I_w_k) in unique_states:
                target_state = unique_states[str(I_w_k)]
                states[len(states)] = I_w_k
                if len(I_w_k) == 1 and I_w_k == [[1]]:
                    automaton.add_transition(state_i, final_state, str(k))
                automaton.add_transition(state_i, target_state, str(k))
                found_matching_state = True
            if not found_matching_state:
                j += 1
                new_state = automaton.add_state(j)
                states[len(states)] = I_w_k
                unique_states[str(I_w_k)] = new_state
                if len(I_w_k) == 1 and I_w_k == [[1]]:
                    automaton.add_final_state(new_state)
                automaton.add_transition(state_i, new_state, str(k))

        i += 1
    print(automaton.serialize_json())
    return automaton


if __name__ == "__main__":
    image = [[1, 1, 1, 1],
             [1, 0, 1, 0],
             [0, 1, 0, 1],
             [1, 1, 1, 1]]

    utils.save_image(image)
    fa = solve(image)
    print(fa.serialize_json())
