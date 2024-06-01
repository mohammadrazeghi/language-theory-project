import json


class State:
    __counter = 0

    def __init__(self, id: None) -> None:
        if id is None:
            self.id = State._get_next_id()
        else:
            self.id = id
        self.transitions: dict[str, 'State'] = {}

    def add_transition(self, symbol: str, state: 'State') -> None:
        self.transitions[symbol] = state

    @classmethod
    def _get_next_id(cls) -> int:
        current_id = cls.__counter
        cls.__counter += 1
        return current_id


class DFA:
    def __init__(self) -> None:
        self.init_state = None
        self.states: list['State'] = []
        self.alphabet: list['str'] = []
        self.final_states: list['State'] = []

    @staticmethod
    def deserialize_json(json_str: str) -> 'DFA':
        fa = DFA()
        json_fa = json.loads(json_str)

        fa.alphabet = json_fa["alphabet"]

        for state_str in json_fa["states"]:
            fa.add_state(int(state_str[2:]))

        fa.init_state = fa.get_state_by_id(json_fa["initial_state"][2:])

        for final_str in json_fa["final_states"]:
            fa.add_final_state(fa.get_state_by_id(final_str[2:]))

        for state_str in json_fa["states"]:
            for symbol in fa.alphabet:
                fa.add_transition(fa.get_state_by_id(state_str[2:]), fa.get_state_by_id(json_fa[state_str][symbol][2:]),
                                  symbol)

        return fa

    def serialize_json(self) -> str:
        fa = {
            "states": list(map(lambda s: f"q_{s.id}", self.states)),
            "initial_state": f"q_{self.init_state.id}",
            "final_states": list(map(lambda s: f"q_{s.id}", self.final_states)),
            "alphabet": self.alphabet
        }

        for state in self.states:
            fa[f"q_{state.id}"] = {}
            for symbol in self.alphabet:
                fa[f"q_{state.id}"][symbol] = f"q_{state.transitions[symbol].id}"

        return json.dumps(fa)

    def add_state(self, id: int | None = None) -> State:
        new_state = State(id)
        self.states.append(new_state)
        return new_state

    def add_transition(self, from_state: State, to_state: State, input_symbol: str) -> None:
        from_state.add_transition(input_symbol, to_state)

    def assign_initial_state(self, state: State) -> None:
        self.init_state = state

    def add_final_state(self, state: State) -> None:
        self.final_states.append(state)

    def get_state_by_id(self, id) -> State | None:
        for state in self.states:
            if state.id == id:
                return state
        return None

    def is_final(self, state: State) -> bool:
        return state in self.final_states


class NFAState(State):
    def __init__(self, id: int | None = None) -> None:
        super().__init__(id)
        self.epsilon_transitions: list[NFAState] = []

    def add_epsilon_transition(self, state: 'NFAState') -> None:
        self.epsilon_transitions.append(state)


class NFA:
    def __init__(self) -> None:
        self.init_state = None
        self.states: list[NFAState] = []
        self.alphabet: list[str] = []
        self.final_states: list[NFAState] = []

    @staticmethod
    def convert_DFA_instanse_to_NFA_instanse(dfa_machine: 'DFA') -> 'NFA':
        nfa = NFA()

        # Create NFA states from DFA states
        state_mapping = {}
        for dfa_state in dfa_machine.states:
            nfa_state = NFAState(dfa_state.id)
            state_mapping[dfa_state] = nfa_state
            nfa.states.append(nfa_state)
            if dfa_machine.init_state == dfa_state:
                nfa.init_state = nfa_state
            if dfa_machine.is_final(dfa_state):
                nfa.final_states.append(nfa_state)

        # Convert transitions
        for dfa_state in dfa_machine.states:
            for symbol, next_state in dfa_state.transitions.items():
                state_mapping[dfa_state].add_transition(
                    symbol, state_mapping[next_state])

        return nfa

    @staticmethod
    def union(machine1: 'NFA', machine2: 'NFA') -> 'NFA':
        # Create a new NFA
        new_nfa = NFA()

        # Create a new initial state and connect it to the initial states of machine1 and machine2
        new_initial_state = NFAState()
        new_nfa.add_state(new_initial_state)
        new_nfa.init_state = new_initial_state
        new_initial_state.add_epsilon_transition(machine1.init_state)
        new_initial_state.add_epsilon_transition(machine2.init_state)

        # Add all states, transitions, and final states from machine1 and machine2 to the new NFA
        new_nfa.states.extend(machine1.states)
        new_nfa.states.extend(machine2.states)
        new_nfa.final_states.extend(machine1.final_states)
        new_nfa.final_states.extend(machine2.final_states)

        return new_nfa

    @staticmethod
    def concat(machine1: 'NFA', machine2: 'NFA') -> 'NFA':
        # Connect final states of machine1 to initial state of machine2
        for state in machine1.final_states:
            state.add_epsilon_transition(machine2.init_state)

        # Combine states, alphabet, and final states
        new_nfa = NFA()
        new_nfa.states = machine1.states + machine2.states
        new_nfa.alphabet = list(set(machine1.alphabet)
                                | set(machine2.alphabet))
        new_nfa.final_states = machine2.final_states

        # Set initial state
        new_nfa.init_state = machine1.init_state

        return new_nfa

    @staticmethod
    def star(machine: 'NFA') -> 'NFA':
        # Create a new initial state
        new_initial_state = NFAState()
        new_machine = NFA()

        # Connect new initial state to the old initial state and to the final states
        new_initial_state.add_epsilon_transition(machine.init_state)
        for final_state in machine.final_states:
            final_state.add_epsilon_transition(machine.init_state)

        # Add new initial state, initial state, and final states to the new machine
        new_machine.add_state(new_initial_state)
        new_machine.init_state = new_initial_state
        new_machine.states.extend(machine.states)
        new_machine.final_states = machine.final_states

        return new_machine

    def serialize_to_json(self) -> str:
        nfa = {
            "states": list(map(lambda s: f"q_{s.id}", self.states)),
            "initial_state": f"q_{self.init_state.id}",
            "final_states": list(map(lambda s: f"q_{s.id}", self.final_states)),
            "alphabet": self.alphabet
        }

        for state in self.states:
            nfa[f"q_{state.id}"] = {}
            for symbol in self.alphabet:
                if symbol in state.transitions:
                    nfa[f"q_{state.id}"][symbol] = f"q_{state.transitions[symbol].id}"
            if state.epsilon_transitions:
                nfa[f"q_{state.id}"]["ε"] = [
                    f"q_{st.id}" for st in state.epsilon_transitions]

        return json.dumps(nfa)
