from dataclasses import dataclass


@dataclass
class PathPart:
    seq: int
    path_seq: int
    start_vid: int
    end_vid: int
    node_id: int
    edge_id: int
    cost: float
    agg_cost: float

    @classmethod
    def from_pgr(
        cls,
        seq: int,
        path_seq: int,
        start_vid: int,
        end_vid: int,
        node_id: int,
        edge_id: int,
        cost: float,
        agg_cost: float,
    ) -> "PathPart":
        return cls(seq, path_seq, start_vid, end_vid, node_id, edge_id, cost, agg_cost)

    def __str__(self):
        return f"""
            Seq: {self.seq},
            Path Seq: {self.path_seq},
            Start vertex ID: {self.start_vid},
            End vertex ID: {self.end_vid},
            Node ID: {self.node_id},
            Edge ID: {self.edge_id},
            Cost: {self.cost},
            Agg Cost: {self.agg_cost}
        """
