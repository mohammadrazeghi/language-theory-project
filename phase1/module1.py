import FA_class
import utils

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

    # Step 1: i=j=0
    i = j = 0

    # Step 2: Create state 0 and assign u0 = I
    state_0 = automaton.add_state(0)
    automaton.assign_initial_state(state_0)
    states[0] = image

    while True:
        # Step 3: Process state i
        current_image = states[i]
        alpha = len(current_image)
        if alpha == 1:
            break
        state_i = automaton.get_state_by_id(i)
        for k in range(4):
            I_w_k = get_zoomed_part(current_image, k)

            # Check if I_w_k matches with any existing state's image
            found_matching_state = False
            for q, u_q in states.items():
                if I_w_k == u_q:
                    states[len((states))] = I_w_k
                    automaton.add_transition(state_i, automaton.get_state_by_id(q), str(k))
                    found_matching_state = True
                    break

            # If no matching state is found, create a new state
            if not found_matching_state:
                j += 1
                new_state = automaton.add_state(j)
                states[len((states))] = I_w_k
                automaton.add_transition(state_i, new_state, str(k))

        # Step 4: Check if all states have been processed
        if i == j:
            break
        else:
            i += 1

    return automaton


if __name__ == "__main__":
    image = [[1, 1, 1, 1],
             [1, 0, 1, 0],
             [0, 1, 0, 1],
             [1, 1, 1, 1]]

    utils.save_image(image)
    fa = solve(image)
    print(fa.serialize_json())