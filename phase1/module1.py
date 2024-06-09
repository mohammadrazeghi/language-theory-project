import FA_class
import utils
from collections import defaultdict

imageType = list[list[int]]


def remove_duplicate(states: dict[int, imageType]) -> dict[int, imageType]:
    unique_states = {}
    seen_images = set()

    for state_id, image in states.items():
        image_tuple = tuple(tuple(row) for row in image)  # Convert the image to a tuple of tuples for hashing
        if image_tuple not in seen_images:
            seen_images.add(image_tuple)
            unique_states[state_id] = image

    # Assign consecutive keys from 0 to n
    new_unique_states = {i: image for i, (state_id, image) in enumerate(unique_states.items())}

    return new_unique_states

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
    count = 0
    # Step 1: i=j=0
    i = j = 0

    directions = ['0', '1', '2', '3']
    automaton.alphabet = directions

    # Step 2: Create state 0 and assign u0 = I
    state_0 = automaton.add_state(0)
    automaton.assign_initial_state(state_0)
    states[0] = image
    final_state = automaton.add_state(-1)
    automaton.add_final_state(final_state)
    while True:
        # Step 3: Process state i
        current_image = states[i]
        alpha = len(current_image)
        if alpha == 1 and count == 0:
            count += 1
        if count == 1:
            break
        state_i = automaton.get_state_by_id(i)
        for k in range(4):
            I_w_k = get_zoomed_part(current_image, k)
            # Check if I_w_k matches with any existing state's image
            found_matching_state = False
            unique_states = remove_duplicate(states)
            for q, u_q in unique_states.items():
                if I_w_k == u_q:
                    states[len((states))] = I_w_k
                    if len(I_w_k) == 1 and I_w_k == [[1]]:
                        automaton.add_transition(automaton.get_state_by_id(q), final_state, str(k))
                    automaton.add_transition(state_i, automaton.get_state_by_id(q), str(k))
                    found_matching_state = True
                    break

            # If no matching state is found, create a new state
            if not found_matching_state:
                j += 1
                new_state = automaton.add_state(j)
                states[len((states))] = I_w_k
                if len(I_w_k) == 1 and I_w_k == [[1]]:
                    automaton.add_transition(new_state, final_state, str(k))
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