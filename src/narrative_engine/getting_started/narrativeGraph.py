import networkx as nx

class NarrativeGraph:

    def __init__(self):
        self.graph = nx.DiGraph()
        self.next_state_id = 0
        self.state_ids = {}

    def get_state_id(
        self, 
        state
    ):
        state_key = state.model_dump_json()
        return self.state_ids.get(state_key)

    def add_state(
        self,
        state
    ):
        state_key = state.model_dump_json()

        if state_key in self.state_ids:
            return self.state_ids[state_key]

        state_id = self.next_state_id

        self.graph.add_node(
            state_id,
            state = state
        )

        self.state_ids[state_key] = state_id
        self.next_state_id += 1

        return state_id

    def add_transition(
        self,
        source_id,
        target_id,
        action
    ):
        self.graph.add_edge(
            source_id,
            target_id,
            action=action
        )

    def get_state(
        self,
        state_id
    ):
        return self.graph.nodes[state_id]["state"]